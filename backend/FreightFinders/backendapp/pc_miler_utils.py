import requests
from django.conf import settings

BASE_SINGLE_SEARCH_URL = 'https://singlesearch.alk.com/NA/api/search'
BASE_GEOCODING_URL = 'https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/locations'
BASE_REVERSE_GEOCODING_URL = 'https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/locations/reverse'
BASE_RADIUS_SEARCH_URL = 'https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/poi'

def single_search(query):
    params = {
        'authToken': settings.PC_MILER_API_KEY,
        'query': query
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
        'poiCategories': 'All',
        'region': 'NA',
        'dataset': 'Current'
    }

    response = requests.get(BASE_RADIUS_SEARCH_URL, params=params)
    return handle_response(response)

def handle_response(response):
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            return {'error': 'Failed to parse JSON.'}
    else:
        return {'error': f'{response.status_code} - {response.text}'}