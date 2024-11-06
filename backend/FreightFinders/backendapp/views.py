from logging import Logger
import time
from django.shortcuts import render
from django.http import JsonResponse
from .supabase_client import get_supabase_client
from datetime import datetime
from .models import LoadStop, LoadPosting
from django.db.models import Max, OuterRef, Subquery, F, Q, Prefetch
from concurrent.futures import ThreadPoolExecutor
from .pc_miler_utils import single_search, geocode_search, reverse_geocode_search, radius_search


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
    city_name = request.GET.get('city_name')
    radius = request.GET.get('radius', 5)  # Default radius if not provided
    
    # If city_name is provided, use it to get the coordinates first
    if city_name:
        try:
            # Get coordinates using single_search
            single_search_data = single_search(city_name)
            
            # Select the first location in the list (if available)
            locations = single_search_data.get("Locations", [])
            if locations:
                selected_coords = locations[0]["Coords"]
            else:
                return JsonResponse({"error": "No location found for the specified city"}, status=500)

            center_lat = selected_coords["Lat"]
            center_lon = selected_coords["Lon"]

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=500)

    # If city_name is not provided, get latitude and longitude from request parameters
    else:
        center_lat = request.GET.get('center_lat')
        center_lon = request.GET.get('center_lon')

        # Check if latitude and longitude are provided
        if not center_lat or not center_lon:
            return JsonResponse({"error": "Either city name or center coordinates are required"}, status=400)

    # Perform the radius search with the obtained or provided coordinates
    data = radius_search(center_lat=center_lat, center_lon=center_lon, radius=radius)
     # Wrap the result in a dictionary with a key, for example 'locations'
    return JsonResponse({"locations": data})
# PC MILER VIEWS END HERE


def search_locations(request):
    # Get origin and destination input
    origin_city_input = request.GET.get('origin_city', '').lower()
    origin_state_input = request.GET.get('origin_state', '').lower()
    origin_postal_code_input = request.GET.get('origin_postal_code', '').lower()
    destination_city_input = request.GET.get('destination_city', '').lower()
    destination_state_input = request.GET.get('destination_state', '').lower()
    destination_postal_code_input = request.GET.get('destination_postal_code', '').lower()


    # Check for 'anywhere' input
    origin_anywhere = origin_city_input == "anywhere" or origin_state_input == "anywhere" or origin_postal_code_input == "anywhere"
    destination_anywhere = destination_city_input == "anywhere" or destination_state_input == "anywhere" or destination_postal_code_input == "anywhere"

    if origin_anywhere and destination_anywhere:
        return JsonResponse({"error": "Either destination or origin can be anywhere, but not both."}, status=400)

    # Query for origin stops using Django ORM
    origin_query = LoadStop.objects.all().filter(stop_sequence=1)
    if not origin_anywhere:
        if origin_city_input:
            origin_query = origin_query.filter(city__iexact=origin_city_input)
        if origin_state_input:
            origin_query = origin_query.filter(state__iexact=origin_state_input)
        if origin_postal_code_input:
            origin_query = origin_query.filter(postal_code__iexact=origin_postal_code_input)


    max_sequence_subquery = (
        LoadStop.objects
        .filter(load_id=OuterRef('load_id'))
        .values('load_id')
        .annotate(max_sequence=Max('stop_sequence'))
        .values('max_sequence'))

    # Filter main LoadStop query using the subquery
    destination_query = (
        LoadStop.objects
        .annotate(max_sequence=Subquery(max_sequence_subquery))
        .filter(stop_sequence=F('max_sequence'))
        .defer('max_sequence')
    )

    # Query for destination stops using Django ORM
    if not destination_anywhere:
        if destination_city_input:
            destination_query = destination_query.filter(city__iexact=destination_city_input)
        if destination_state_input:
            destination_query = destination_query.filter(state__iexact=destination_state_input)
        if destination_postal_code_input:
            destination_query = destination_query.filter(postal_code__iexact=destination_postal_code_input)

     
     
    origin_data = list(origin_query.values())
    destination_data = list(destination_query.values())
    origin_load_ids = {item['load_id'] for item in origin_data}
    destination_load_ids = {item['load_id'] for item in destination_data}

    if origin_anywhere:
        common_load_ids = destination_load_ids
    elif destination_anywhere:
        common_load_ids = origin_load_ids
    else:
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