from logging import Logger
from django.shortcuts import render
from django.http import JsonResponse
from .supabase_client import get_supabase_client
from datetime import datetime
from .models import LoadStop

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
    if origin_city_input:
        origin_query = origin_query.filter(city__iexact=origin_city_input)
    if origin_state_input:
        origin_query = origin_query.filter(state__iexact=origin_state_input)
    if origin_postal_code_input:
        origin_query = origin_query.filter(postal_code__iexact=origin_postal_code_input)
    origin_query = origin_query.filter(stop_sequence=1)

    # Query for destination stops using Django ORM
    destination_query = LoadStop.objects.all()
    if destination_city_input:
        destination_query = destination_query.filter(city__iexact=destination_city_input)
    if destination_state_input:
        destination_query = destination_query.filter(state__iexact=destination_state_input)
    if destination_postal_code_input:
        destination_query = destination_query.filter(postal_code__iexact=destination_postal_code_input)

    # Convert QuerySet to list of dictionaries
    origin_data = list(origin_query.values())
    destination_data = list(destination_query.values())

    # Return the result as JSON
    return JsonResponse({'origin_results': origin_data, 'destination_results': destination_data}, safe=False)
# # Create your views here.
# def search_locations(request):
#     # origin input
#     origin_city_input = request.GET.get('origin_city', '').lower()
#     origin_state_input = request.GET.get('origin_state', '').lower()
#     origin_postal_code_input = request.GET.get('origin_postal_code', '').lower()

#     # destination input
#     destination_city_input = request.GET.get('destination_city', '').lower()
#     destination_state_input = request.GET.get('destination_state', '').lower()
#     destination_postal_code_input = request.GET.get('destination_postal_code', '').lower()

#     supabase = get_supabase_client() # supabase client

#     # query for origin
#     origin_query = supabase.table('load_stop').select('*')
#     if origin_city_input:
#         origin_query = origin_query.ilike('city', f'%{origin_city_input}%')
#     if origin_state_input:
#         origin_query = origin_query.ilike('state', f'%{origin_state_input}%')
#     if origin_postal_code_input:
#         origin_query = origin_query.ilike('postal_code', f'%{origin_postal_code_input}%')

#     # query for destination
#     destination_query = supabase.table('load_stop').select('*')
#     if destination_city_input:
#         destination_query = destination_query.ilike('city', f'%{destination_city_input}%')
#     if destination_state_input:
#         destination_query = destination_query.ilike('state', f'%{destination_state_input}%')
#     if destination_postal_code_input:
#         destination_query = destination_query.ilike('postal_code', f'%{destination_postal_code_input}%')

#     origin_response = origin_query.execute()
#     destination_response = destination_query.execute()

#     # combine data
#     origin_data = origin_response.data
#     destination_data = destination_response.data

#     return JsonResponse({'origin_results': origin_data, 'destination_results': destination_data}, safe=False)

def multi_capacity_type(request):
    multi_capacities = request.GET.get('transport_modes', '').lower()
    capacity_list = multi_capacities.split(',')

    supabase = get_supabase_client()

    capacities_query = supabase.table('load_posting').select('*')
    if multi_capacities:

        if len(capacity_list) > 0:

            for capacity in capacity_list:
        
                capacities_query = capacities_query.ilike('transport_mode', f'%{capacity}')

    capacities_response = capacities_query.execute()

    capacities_data = capacities_response.data

    return JsonResponse(capacities_data, safe=False)


def search_dates(request):

    start_date_earliest = request.GET.get('earliest_start_date', '').lower()
    start_date_latest = request.GET.get('latest_start_date', '').lower()
    end_date_earliest = request.GET.get('earliest_end_date', '').lower()
    end_date_latest = request.GET.get('latest_end_date', '').lower()

    supabase = get_supabase_client()

    origin_dates_query = supabase.table('load_stop').select('*')
    last_stops = []
    if(start_date_earliest and start_date_latest):
        
        start_date_earliest = datetime.strptime(start_date_earliest, '%Y-%m-%d')
        start_date_latest = datetime.strptime(start_date_latest, '%Y-%m-%d')
        start_date_latest = start_date_latest.replace(hour = 23, minute = 59, second = 59)

        origin_dates_query = origin_dates_query.eq('stop_sequence', 1) \
            .gte('appointment_to', start_date_earliest) \
            .lte('appointment_from', start_date_latest)

    if(end_date_earliest and end_date_latest):
        
        end_date_earliest = datetime.strptime(end_date_earliest, '%Y-%m-%d')
        end_date_latest = datetime.strptime(end_date_latest, '%Y-%m-%d')
        end_date_latest = end_date_latest.replace(hour = 23, minute = 59, second = 59)

        max_sequences = supabase.table('load_stop') \
            .select('load_id, MAX(stop_sequence)', count='exact') \
            .group('load_id') \
            .execute()

        max_sequence_data = max_sequences.data

        for item in max_sequence_data:
            load_id = item['load_id']
            max_stop_sequence = item['max']

            # Fetch the stop details for each load_id and its max stop_sequence
            stop_response = supabase.table('load_stop') \
                .select('*') \
                .eq('load_id', load_id) \
                .eq('stop_sequence', max_stop_sequence) \
                .gte('appointment_to', end_date_earliest) \
                .lte('appointment_from', end_date_latest) \
                .execute()

            last_stops.extend(stop_response.data)


    origin_dates_response = origin_dates_query.execute()

    origin_dates_data = origin_dates_response.data

    # return JsonResponse({'origin_results': origin_dates_data, 'destination_results': dest}, safe=False)
    return JsonResponse(origin_dates_data, safe=False)

def home(request):
    return JsonResponse("Welcome to the homepage!", safe = False)