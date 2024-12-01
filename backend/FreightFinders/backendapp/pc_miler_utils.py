import requests
import random
from django.conf import settings
import asyncio
import aiohttp

BASE_SINGLE_SEARCH_URL = 'https://singlesearch.alk.com/NA/api/search'
BASE_GEOCODING_URL = 'https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/locations'
BASE_REVERSE_GEOCODING_URL = 'https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/locations/reverse'
BASE_RADIUS_SEARCH_URL = 'https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/poi'
BASE_ROUTE_DISTANCE_URL = 'https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/route/routeReports'


def single_search(query):
    params = {
        'authToken': settings.PC_MILER_API_KEY,
        'query': query,
        'includeOnly': 'City'
    }
    response = requests.get(BASE_SINGLE_SEARCH_URL, params=params)
    return handle_response(response)

def geocode_search(street=None, city=None, state=None, country='US', postcode=None):
    params = {
        'authToken': settings.PC_MILER_API_KEY,
        'country': country,
        'region': 'NA',
        'dataset': 'Current'
    }
    if street:
        params['street'] = street
    if city:
        params['city'] = city
    if state:
        params['state'] = state
    if postcode:
        params['postcode'] = postcode

    response = requests.get(BASE_GEOCODING_URL, params=params)
    return handle_response(response)

def reverse_geocode_search(latitude, longitude):
    params = {
        'authToken': settings.PC_MILER_API_KEY,
        'Coords': f"{longitude},{latitude}",
        'matchNamedRoadsOnly': 'true',
        'maxCleanupMiles': 20,
        'region': 'NA',
        'dataset': 'Current',
        'includeTrimblePlaceIds': 'true'
    }

    response = requests.get(BASE_REVERSE_GEOCODING_URL, params=params)
    return handle_response(response)

def radius_search(center_lat, center_lon, radius=5):
    params = {
        'authToken': settings.PC_MILER_API_KEY,
        'center': f"{center_lon},{center_lat}",
        'radius': radius,
        'radiusUnits': 'Miles',
        'poiCategories': '2',
        'region': 'NA',
        'dataset': 'Current'
    }

    response = requests.get(BASE_RADIUS_SEARCH_URL, params=params)
    return handle_response(response)

def check_road_miles(lat_1, lon_1, lat_2, lon_2):
    """
    Check the road miles between two sets of coordinates using PC Miler API.
    :param lat_1, lon_1: Coordinates of the origin.
    :param lat_2, lon_2: Coordinates of the destination.
    :return: Road miles distance.
    """
    stops = f"{lon_1},{lat_1};{lon_2},{lat_2}"
    params = {
        'authToken': settings.PC_MILER_API_KEY,
        'stops': stops,
        'reports': 'CalcMiles'
    }
    response = requests.get(BASE_ROUTE_DISTANCE_URL, params=params)
    return handle_response(response)


def handle_response(response):
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            return {'error': 'Failed to parse JSON.'}
    else:
        return {'error': f'{response.status_code} - {response.text}'}
    
def fetch_coordinates_from_zip(zip_code):
    """
    Fetch coordinates (latitude, longitude) for a given zip code using geocoding.
    :param zip_code: The zip code to geocode.
    :return: Latitude and longitude of the zip code.
    """
    result = geocode_search(postcode=zip_code)
    if 'error' in result:
        return None
    # Assuming the result contains latitude and longitude.
    if 'Locations' in result and result['Locations']:
        location = result['Locations'][0]
        return location.get('Latitude'), location.get('Longitude')
    return None

async def fetch_route_distance(session, origin_lat, origin_lon, dest_lat, dest_lon, zip, radius, lock, result_list):
    """
    Fetch road miles asynchronously between the origin and destination.
    If the road miles are within the radius, append the zip code to the result list.
    """
    url = 'https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/route/routeReports'
    stops = f"{origin_lon},{origin_lat};{dest_lon},{dest_lat}"
    params = {
        'authToken': settings.PC_MILER_API_KEY,
        'stops': stops,
        'reports': 'CalcMiles'
    }
    async with session.get(url, params=params) as response:
        if response.status == 200:
            try:
                data = await response.json()
                print(data)
                if data and 'TMiles' in data[0] and data[0]['TMiles'] < radius:
                    async with lock:
                        result_list.append(zip)
            except ValueError:
                pass  # Handle JSON parsing errors if needed

async def fetch_nearby_zipcodes_with_road_check(lat, lon, radius, valid_zip_codes):
    """
    Fetch nearby zip codes within the given radius and validate them using road miles.
    :param lat: Latitude of the center location.
    :param lon: Longitude of the center location.
    :param radius: Radius to search within (in miles).
    :param valid_zip_codes: List of zip codes to validate.
    :return: List of valid zip codes within the radius and with valid road miles.
    """
    # Fetch nearby locations based on air miles search.
    air_mile_results = radius_search(lat, lon, radius)
    if 'error' in air_mile_results:
        return []

    filtered_results = list(filter(lambda x: x['POILocation']['Address']['Zip'][:5] in valid_zip_codes, air_mile_results))
    unique_zip_coords = set(
    (
        item['POILocation']['Address']['Zip'], 
        item['POILocation']['Coords']['Lat'], 
        item['POILocation']['Coords']['Lon']
    )
    for item in filtered_results)

    valid_zip_codes_with_road_miles = []

    # for location in unique_zip_coords:

    #     ##############

    #     stops = f"{lon},{lat};{location[2]},{location[1]}"
    #     params = {
    #         'authToken': settings.PC_MILER_API_KEY,
    #         'stops': stops,
    #         'reports': 'CalcMiles'
    #     }
    #     response = requests.get(BASE_ROUTE_DISTANCE_URL, params=params)
    #     response = handle_response(response)

    #     ############

    #     print(road_distance_result[0]['TMiles'])
        
    lock = asyncio.Lock()  # Lock to manage access to the shared list

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_route_distance(session, lat, lon, dest_lat, dest_lon, zip, radius, lock, valid_zip_codes_with_road_miles)
            for zip, dest_lat, dest_lon in unique_zip_coords
        ]
        await asyncio.gather(*tasks)

    return valid_zip_codes_with_road_miles















# Function to fetch nearby zip codes with road miles check
# def fetch_nearby_zipcodes_with_road_check(lat, lon, radius, valid_zip_codes):
#     """
#     Fetch nearby zip codes within the given radius and validate them using road miles.
#     :param lat: Latitude of the center location.
#     :param lon: Longitude of the center location.
#     :param radius: Radius to search within (in miles).
#     :param valid_zip_codes: List of zip codes to validate.
#     :return: List of valid zip codes within the radius and with valid road miles.
#     """
#     # Fetch nearby locations based on air miles search.
#     air_mile_results = radius_search(lat, lon, radius)
#     if 'error' in air_mile_results:
#         return []

#     filtered_results = list(filter(lambda x: x['POILocation']['Address']['Zip'][:5] in valid_zip_codes, air_mile_results))
#     valid_zip_codes_with_road_miles = []

#     print(filtered_results)

#     for location in filtered_results:

#         destination_coords = location['POILocation']['Coords']


#         road_distance_result = check_road_miles(lat, lon, destination_coords['Lat'], destination_coords['Lon'])
#         print(road_distance_result)

#         # if(radius >= 100):
            
#         #     if(zip_code != '' and zip_code[:3] in visited):
#         #         visited[zip_code[:3]].append((zip_code, destination_coords))
#         #     elif(zip_code != ''):
#         #         visited[zip_code[:3]] = [(zip_code, destination_coords)]

#         # else:
            
#         #     if(zip_code != '' and zip_code[:4] in visited):
#         #         visited[zip_code[:4]].append((zip_code, destination_coords))
#         #     elif(zip_code != ''):
#         #         visited[zip_code[:4]] = [(zip_code, destination_coords)]


#     # for zip_group in visited:
#     #     num_zips_in_group = len(visited[zip_group])
#     #     random_zip = random.randint(0, num_zips_in_group - 1)

#     #     road_distance_result = check_road_miles(lat, lon, visited[zip_group][random_zip][1]['Lat'], visited[zip_group][random_zip][1]['Lon'])
#         # print(random_number)
#     # print(visited)

#     # for location in air_mile_results:
#     #     zip_code = location['POILocation']['Address']['Zip']
#     #     destination_coords = location['POILocation']['Coords']
#     #     # destination_coords = fetch_coordinates_from_zip(zip_code)
#     #     if destination_coords:
#     #         # print(lat, lon)
#     #         # print(destination_coords['Lat'], destination_coords['Lon'])
#     #         # Calculate the road miles between the origin and destination coordinates
#     #         road_distance_result = check_road_miles(lat, lon, destination_coords['Lat'], destination_coords['Lon'])
#     #         # print(road_distance_result)
#     #         if(counter > 1):
#     #             break
#     #         counter+= 1
#     #         # print(counter)
#     #         # if 'CalcMiles' in road_distance_result:
#     #         #     road_miles = road_distance_result['CalcMiles']
#     #         #     if road_miles <= radius:
#     #         #         valid_zip_codes_with_road_miles.append(zip_code)
    
#     print("DONE")
#     return valid_zip_codes_with_road_miles