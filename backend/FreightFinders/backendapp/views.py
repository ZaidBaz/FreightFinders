from logging import Logger
import time
from django.shortcuts import render
from django.http import JsonResponse
from .supabase_client import get_supabase_client
from datetime import datetime
from .models import LoadStop
from .models import LoadPosting
from django.db.models import Max, OuterRef, Subquery, F, Q
from django.db import connection
from concurrent.futures import ThreadPoolExecutor

def search_locations(request):
    # Get origin input
    origin_city_input = request.GET.get('origin_city', '').lower()
    origin_state_input = request.GET.get('origin_state', '').lower()
    origin_postal_code_input = request.GET.get('origin_postal_code', '').lower()

    # Get destination input
    destination_city_input = request.GET.get('destination_city', '').lower()
    destination_state_input = request.GET.get('destination_state', '').lower()
    destination_postal_code_input = request.GET.get('destination_postal_code', '').lower()

    # Query for origin stops using Django ORM
    origin_query = LoadStop.objects.all()
    origin_query = origin_query.filter(stop_sequence=1)
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
    if destination_city_input:
        destination_query = destination_query.filter(city__iexact=destination_city_input)
    if destination_state_input:
        destination_query = destination_query.filter(state__iexact=destination_state_input)
    if destination_postal_code_input:
        destination_query = destination_query.filter(postal_code__iexact=destination_postal_code_input)

    # Convert QuerySet to list of dictionaries
    origin_data = list(origin_query.values())
    destination_data = list(destination_query.values())

    origin_load_ids = {item['load_id'] for item in origin_data}
    destination_load_ids = {item['load_id'] for item in destination_data}

    # Find common load_ids
    common_load_ids = origin_load_ids.intersection(destination_load_ids)
    # Return the result as JSON

    # print('search-locations: ', common_load_ids)

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

    origin_dates_data = list(origin_dates_query.values())
    destination_dates_data = list(destination_dates_query.values())

    origin_load_ids = {item['load_id'] for item in origin_dates_data}
    destination_load_ids = {item['load_id'] for item in destination_dates_data}

    # Find common load_ids
    common_load_ids = origin_load_ids.intersection(destination_load_ids)


    return common_load_ids

def multi_capacity_type(request):

    multi_capacities = request.GET.get('transport_modes', '').lower()

    if(multi_capacities == ''):

        all_postings = LoadPosting.objects.all()

        all_postings_data = list(all_postings.values())

        return {item['load_id'] for item in all_postings_data}

    capacity_list = multi_capacities.split(',')

    query = Q()
    for capacity in capacity_list:
        query |= Q(transport_mode__iexact=capacity)

    capacities_query = LoadPosting.objects.filter(query)

    capacities_data = set(capacities_query.values())

    capacities_load_ids = {item['load_id'] for item in capacities_data}

    return capacities_load_ids

def filter_loads(request):

    def get_load_ids_locations():
        return search_locations(request)
    
    def get_load_ids_dates():
        return search_dates(request)
    
    def get_load_ids_capacity_types():
        return multi_capacity_type(request)

    # Execute functions in parallel
    with ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        future_locations = executor.submit(get_load_ids_locations)
        future_dates = executor.submit(get_load_ids_dates)
        future_capacity_types = executor.submit(get_load_ids_capacity_types)

        # Retrieve results
        load_ids_locations = future_locations.result()
        load_ids_dates = future_dates.result()
        load_ids_capacity_types = future_capacity_types.result()

    load_ids_locations_dates = load_ids_locations.intersection(load_ids_dates)

    all_load_ids = load_ids_capacity_types.intersection(load_ids_locations_dates)

    return JsonResponse(list(all_load_ids), safe = False )

    # multi_capacity_type

def home(request):
    return JsonResponse("Welcome to the homepage!", safe = False)