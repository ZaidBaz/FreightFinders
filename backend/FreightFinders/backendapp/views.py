from logging import Logger
import time
from django.shortcuts import render
from django.http import JsonResponse
from .supabase_client import get_supabase_client
from datetime import datetime
from .models import LoadStop, LoadPosting
from django.db.models import Max, OuterRef, Subquery, F, Q, Prefetch
from concurrent.futures import ThreadPoolExecutor
from .pc_miler_utils import single_search, geocode_search, reverse_geocode_search, radius_search, fetch_nearby_zipcodes_with_road_check, check_road_miles, fetch_coordinates_from_zip
import asyncio
import json

# PC MILER VIEWS START HERE
def single_search_view(request):
    query = request.GET.get('query', '54115')  # Default zip code as provided by PC Miler doc
    data = single_search(query=query)
    return JsonResponse(data)

def geocode_search_view(request):
    street = request.GET.get('street')
    city = request.GET.get('city')
    state = request.GET.get('state')
    postcode = request.GET.get('postcode')
    data = geocode_search(street=street, city=city, state=state, postcode=postcode)
    return JsonResponse(data)

def reverse_geocode_view(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    data = reverse_geocode_search(latitude=latitude, longitude=longitude)
    return JsonResponse(data)

def radius_search_view(request):
    center_lat = request.GET.get('center_lat')
    center_lon = request.GET.get('center_lon')
    radius = request.GET.get('radius', 5)  # Default radius is 5 miles
    if not center_lat or not center_lon:
        return JsonResponse({"error": "Center latitude and longitude parameters are required."}, status=400)
    
    try:
        center_lat = float(center_lat)
        center_lon = float(center_lon)
        radius = float(radius)
    except ValueError:
        return JsonResponse({"error": "Latitude, longitude, and radius must be valid numbers."}, status=400)
    
    data = radius_search(center_lat=center_lat, center_lon=center_lon, radius=radius)
    return JsonResponse(data, safe=False)

def search_locations(request):

    # Get origin and destination input
    origin_input = request.GET.get('origin', '').lower()  
    full_origin_input = request.GET.get('origin_full_addr', '')
    destination_input = request.GET.get('destination', '').lower()
    full_destination_input = request.GET.get('destination_full_addr', '')

    # Trim extra spaces
    origin_city_input = None
    origin_state_input = None
    destination_city_input = None
    destination_state_input = None

    #Check for origin radius and destination radius
    origin_radius = request.GET.get('origin_radius', None) 
    destination_radius = request.GET.get('destination_radius', None)

    origin_zip = None
    destination_zip = None

    # Check for 'anywhere' input
    origin_anywhere = origin_input == "anywhere"
    destination_anywhere = destination_input == "anywhere"

    if(origin_anywhere is False and full_origin_input != 'null'):
        
        json_full_origin_input = json.loads(full_origin_input)
        origin_zip = str(json_full_origin_input["Address"]["Zip"]).strip()

    if(destination_anywhere is False and full_destination_input != 'null'):

        json_full_destination_input = json.loads(full_destination_input)
        destination_zip = str(json_full_destination_input["Address"]["Zip"]).strip()

    if(origin_anywhere is False):
        origin_city_input, origin_state_input = origin_input.split(',') if origin_input else ('', '')
        origin_city_input = origin_city_input.strip()
        origin_state_input = origin_state_input.strip()

    if(destination_anywhere is False):
        destination_city_input, destination_state_input = destination_input.split(',') if destination_input else ('', '')
        destination_city_input = destination_city_input.strip()
        destination_state_input = destination_state_input.strip()

    if (origin_anywhere and destination_anywhere) or (origin_input == '' and destination_input == ''):
        return JsonResponse({"error": "Either destination or origin can be anywhere, but not both."}, status=400)

    ########

    if origin_anywhere or origin_input == '':
        
        max_sequence_subquery = (
            LoadStop.objects
            .filter(load_id=OuterRef('load_id'))
            .values('load_id')
            .annotate(max_sequence=Max('stop_sequence'))
            .values('max_sequence'))

        destination_query = (
            LoadStop.objects
            .annotate(max_sequence=Subquery(max_sequence_subquery))
            .filter(stop_sequence=F('max_sequence'))
            .defer('max_sequence')
        )

        destination_geocode = geocode_search(postcode=destination_zip)
        if 'error' not in destination_geocode:
            existing_destinations = (LoadStop.objects
                .filter(Q(stop_sequence=2) | Q(stop_sequence=3) | Q(stop_sequence=4) | Q(stop_sequence=5))
                .values('city', 'state', 'postal_code').distinct())
            destination_lat = destination_geocode[0]['Coords']['Lat']
            destination_lon = destination_geocode[0]['Coords']['Lon']
            destination_valid_zip_codes = asyncio.run(fetch_nearby_zipcodes_with_road_check(destination_lat, destination_lon, float(destination_radius), {entry['postal_code'][:5] for entry in existing_destinations}))
            destination_query = destination_query.filter(Q(postal_code__in=destination_valid_zip_codes) | ( Q(city__iexact=destination_city_input) & Q(state__iexact=destination_state_input)))

        destination_data = list(destination_query.values())
        destination_load_ids = {item['load_id'] for item in destination_data}
        return destination_load_ids

    elif destination_anywhere or destination_input == '':

        origin_query = LoadStop.objects.all().filter(stop_sequence=1)
        origin_geocode = geocode_search(postcode=origin_zip)
        if 'error' not in origin_geocode:
            existing_origins = LoadStop.objects.filter(stop_sequence=1).values('city', 'state', 'postal_code').distinct()
            origin_lat = origin_geocode[0]['Coords']['Lat']
            origin_lon = origin_geocode[0]['Coords']['Lon']
            origin_valid_zip_codes = asyncio.run(fetch_nearby_zipcodes_with_road_check(origin_lat, origin_lon, float(origin_radius), {entry['postal_code'][:5] for entry in existing_origins}))
            origin_query = origin_query.filter(Q(postal_code__in=origin_valid_zip_codes) | ( Q(city__iexact=origin_city_input) & Q(state__iexact=origin_state_input)))
        
        origin_data = list(origin_query.values())
        origin_load_ids = {item['load_id'] for item in origin_data}
        return origin_load_ids

    origin_query = LoadStop.objects.all().filter(stop_sequence=1)
    origin_geocode = geocode_search(postcode=origin_zip)
    if 'error' not in origin_geocode:
        existing_origins = LoadStop.objects.filter(stop_sequence=1).values('city', 'state', 'postal_code').distinct()
        origin_lat = origin_geocode[0]['Coords']['Lat']
        origin_lon = origin_geocode[0]['Coords']['Lon']
        origin_valid_zip_codes = asyncio.run(fetch_nearby_zipcodes_with_road_check(origin_lat, origin_lon, float(origin_radius), {entry['postal_code'][:5] for entry in existing_origins}))
        origin_query = origin_query.filter(Q(postal_code__in=origin_valid_zip_codes) | ( Q(city__iexact=origin_city_input) & Q(state__iexact=origin_state_input)))
        
    origin_data = list(origin_query.values())
    origin_load_ids = {item['load_id'] for item in origin_data}

    max_sequence_subquery = (
        LoadStop.objects
        .filter(load_id=OuterRef('load_id'))
        .values('load_id')
        .annotate(max_sequence=Max('stop_sequence'))
        .values('max_sequence'))

    destination_query = (
        LoadStop.objects
        .annotate(max_sequence=Subquery(max_sequence_subquery))
        .filter(stop_sequence=F('max_sequence'))
        .defer('max_sequence')
    )

    destination_geocode = geocode_search(postcode=destination_zip)
    if 'error' not in destination_geocode:
        existing_destinations = (LoadStop.objects
            .filter(Q(stop_sequence=2) | Q(stop_sequence=3) | Q(stop_sequence=4) | Q(stop_sequence=5))
            .values('city', 'state', 'postal_code').distinct())
        destination_lat = destination_geocode[0]['Coords']['Lat']
        destination_lon = destination_geocode[0]['Coords']['Lon']
        destination_valid_zip_codes = asyncio.run(fetch_nearby_zipcodes_with_road_check(destination_lat, destination_lon, float(destination_radius), {entry['postal_code'][:5] for entry in existing_destinations}))
        destination_query = destination_query.filter(Q(postal_code__in=destination_valid_zip_codes) | ( Q(city__iexact=destination_city_input) & Q(state__iexact=destination_state_input)))

    destination_data = list(destination_query.values())
    destination_load_ids = {item['load_id'] for item in destination_data}
    
    common_load_ids = origin_load_ids.intersection(destination_load_ids)
    return common_load_ids


def search_dates(request):
    start_date_earliest = request.GET.get('earliest_start_date', '').lower()
    start_date_latest = request.GET.get('latest_start_date', '').lower()
    end_date_earliest = request.GET.get('earliest_end_date', '').lower()
    end_date_latest = request.GET.get('latest_end_date', '').lower()

    origin_dates_query = LoadStop.objects.all()
    if(start_date_earliest and start_date_latest):

        start_date_earliest = datetime.strptime(start_date_earliest, '%Y-%m-%d')
        start_date_latest = datetime.strptime(start_date_latest, '%Y-%m-%d')
        start_date_latest = start_date_latest.replace(hour = 23, minute = 59, second = 59)

        origin_dates_query = LoadStop.objects.filter(
            stop_sequence=1,
            appointment_to__gte=start_date_earliest,
            appointment_from__lte=start_date_latest
        )

    elif(start_date_earliest):

        start_date_earliest = datetime.strptime(start_date_earliest, '%Y-%m-%d')

        origin_dates_query = LoadStop.objects.filter(
            stop_sequence=1,
            appointment_to__gte=start_date_earliest
        )

    elif(start_date_latest):

        start_date_latest = datetime.strptime(start_date_latest, '%Y-%m-%d')
        start_date_latest = start_date_latest.replace(hour = 23, minute = 59, second = 59)

        origin_dates_query = LoadStop.objects.filter(
            stop_sequence=1,
            appointment_from__lte=start_date_latest
        )

    max_sequence_subquery = (
        LoadStop.objects
        .filter(load_id=OuterRef('load_id'))
        .values('load_id')
        .annotate(max_sequence=Max('stop_sequence'))
        .values('max_sequence')
    )

    # Filter main LoadStop query using the subquery
    destination_dates_query = (
        LoadStop.objects
        .annotate(max_sequence=Subquery(max_sequence_subquery))
        .filter(stop_sequence=F('max_sequence'))
        .defer('max_sequence')
    )

    if(end_date_earliest and end_date_latest):

        end_date_earliest = datetime.strptime(end_date_earliest, '%Y-%m-%d')
        end_date_latest = datetime.strptime(end_date_latest, '%Y-%m-%d')
        end_date_latest = end_date_latest.replace(hour = 23, minute = 59, second = 59)

        destination_dates_query = LoadStop.objects.filter(
            appointment_to__gte=end_date_earliest,
            appointment_from__lte=end_date_latest
        )

    elif(end_date_earliest):

        end_date_earliest = datetime.strptime(end_date_earliest, '%Y-%m-%d')
        destination_dates_query = LoadStop.objects.filter(
            appointment_to__gte=end_date_earliest
        )
    
    elif(end_date_latest):

        end_date_latest = datetime.strptime(end_date_latest, '%Y-%m-%d')
        end_date_latest = end_date_latest.replace(hour = 23, minute = 59, second = 59)

        destination_dates_query = LoadStop.objects.filter(
            appointment_from__lte=end_date_latest
        )

    origin_dates_data = list(origin_dates_query.values())
    destination_dates_data = list(destination_dates_query.values())
    origin_load_ids = {item['load_id'] for item in origin_dates_data}
    destination_load_ids = {item['load_id'] for item in destination_dates_data}
    
    # Find common load_ids
    common_load_ids = origin_load_ids.intersection(destination_load_ids)
    return common_load_ids


def multi_capacity_type(request):
    multi_capacities = request.GET.get('transport_modes', '').lower()

    if multi_capacities == '':
        all_postings = LoadPosting.objects.all()
        all_postings_data = {item['load_id'] for item in all_postings.values('load_id')}
        return all_postings_data

    capacity_list = multi_capacities.split(',')

    query = Q()
    for capacity in capacity_list:
        
        query |= Q(transport_mode__iexact=capacity)

    capacities_query = LoadPosting.objects.filter(query)

    capacities_data = {item['load_id'] for item in capacities_query.values('load_id')}

    return capacities_data


def filter_loads(request):
    # get range for miles to be travelled
    min_distance = float(request.GET.get('min_distance', 0))
    max_distance = float(request.GET.get('max_distance', float('inf')))

    def get_load_ids_locations():
        return search_locations(request)
    
    def get_load_ids_dates():
        return search_dates(request)
    
    def get_load_ids_capacity_types():
        return multi_capacity_type(request)

    with ThreadPoolExecutor() as executor:
        future_locations = executor.submit(get_load_ids_locations)
        future_dates = executor.submit(get_load_ids_dates)
        future_capacity_types = executor.submit(get_load_ids_capacity_types)

        load_ids_locations = future_locations.result()
        load_ids_dates = future_dates.result()
        load_ids_capacity_types = future_capacity_types.result()

    load_ids_locations_dates = load_ids_locations.intersection(load_ids_dates)
    all_load_ids = load_ids_capacity_types.intersection(load_ids_locations_dates)

    load_stops_prefetch = Prefetch(
        'loadid_stops',
        queryset=LoadStop.objects.filter(load_id__in=all_load_ids),
        to_attr='stops'
    )

    load_postings = LoadPosting.objects.filter(
        load_id__in=all_load_ids,
        total_distance__gte=min_distance,
        total_distance__lte=max_distance
    ).prefetch_related(load_stops_prefetch)

    result = []
    for load_posting in load_postings:
        load_stops = [
            {
                'stop_sequence': stop.stop_sequence,
                'stop_type': stop.stop_type,
                'appointment_from': stop.appointment_from,
                'appointment_to': stop.appointment_to,
                'city': stop.city,
                'state': stop.state,
                'postal_code': stop.postal_code,
            }
            for stop in load_posting.stops
        ]
        result.append({
            'load_id': load_posting.load_id,
            'total_distance': load_posting.total_distance,
            'distance_uom': load_posting.distance_uom,
            'transport_mode': load_posting.transport_mode,
            'total_weight': load_posting.total_weight,
            'weight_uom': load_posting.weight_uom,
            'load_stops': load_stops
        })

    return JsonResponse(result, safe=False)

def home(request):
    return JsonResponse("Welcome to the homepage!", safe=False)