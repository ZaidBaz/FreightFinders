import os
import django
import requests
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreightFinders.settings')  
django.setup()

# Define base URLs for different types of searches
BASE_SINGLE_SEARCH_URL = 'https://singlesearch.alk.com/NA/api/search'
BASE_GEOCODING_URL = 'https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/locations'
BASE_REVERSE_GEOCODING_URL = 'https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/locations/reverse'
BASE_RADIUS_SEARCH_URL = 'https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/poi'

def single_search(query):
    """
    Single search for either zip code or city name.
    :param query: The search query (zip code or city name)
    :return: JSON response from the single search API
    """
    params = {
        'authToken': settings.PC_MILER_API_KEY,
        'query': query
    }
    response = requests.get(BASE_SINGLE_SEARCH_URL, params=params)
    return handle_response(response)

def geocode_search(street=None, city=None, state=None, country='US', postcode=None):
    """
    Geocode search using street, city, state, country, and postcode.
    :return: JSON response from the geocoding API
    """
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
    """
    Reverse geocode search by coordinates.
    :param latitude: Latitude of the location
    :param longitude: Longitude of the location
    :return: JSON response from the reverse geocoding API
    """
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
    """
    Radius search for points of interest.
    :param center_lat: Latitude of the center point
    :param center_lon: Longitude of the center point
    :param radius: Search radius in miles
    :return: JSON response from the radius search API
    """
    params = {
        'authToken': settings.PC_MILER_API_KEY,
        'center': f"{center_lon},{center_lat}",
        'radius': radius,
        'radiusUnits': 'Miles',
        'poiCategories': 'All',
        'region': 'NA',
        'dataset': 'Current'
    }

    response = requests.get(BASE_RADIUS_SEARCH_URL, params=params)
    return handle_response(response)

def test_radius_search():
    city_name = "Madison"
    radius = 1  
    # Get the latitude and longitude for the city
    single_search_data = single_search(city_name)
    locations = single_search_data.get("Locations", [])
    if locations:
        selected_coords = locations[0]["Coords"]
        center_lat = selected_coords["Lat"]
        center_lon = selected_coords["Lon"]
        # Now, call radius_search with the obtained coordinates
        print(radius_search(center_lat=center_lat, center_lon=center_lon, radius=radius))
    else:
        print("City not found.")

def handle_response(response):
    """
    Utility function to handle API responses.
    :param response: The HTTP response object
    :return: Parsed JSON or error message
    """
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            return {'error': 'Failed to parse JSON.'}
    else:
        return {'error': f'{response.status_code} - {response.text}'}

#  uncomment these as needed
if __name__ == "__main__":
   # print(single_search(query='53713'))  # Zip code search
  #  print(single_search(query='Madison'))  # City name search
   # print(geocode_search(street='1 Independence Way', city='Princeton', state='NJ', postcode='08540'))
   # print(reverse_geocode_search(latitude=40.958188, longitude=-75.163244))
    
   
    test_radius_search()