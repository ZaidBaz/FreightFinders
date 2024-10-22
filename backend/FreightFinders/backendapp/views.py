from django.shortcuts import render
from django.http import JsonResponse
from .supabase_client import get_supabase_client

# Create your views here.
def search_locations(request):
    # origin input
    origin_city_input = request.GET.get('origin_city', '').lower()
    origin_state_input = request.GET.get('origin_state', '').lower()
    origin_postal_code_input = request.GET.get('origin_postal_code', '').lower()

    # destination input
    destination_city_input = request.GET.get('destination_city', '').lower()
    destination_state_input = request.GET.get('destination_state', '').lower()
    destination_postal_code_input = request.GET.get('destination_postal_code', '').lower()

    supabase = get_supabase_client() # supabase client

    # query for origin
    origin_query = supabase.table('load_stop').select('*')
    if origin_city_input:
        origin_query = origin_query.ilike('city', f'%{origin_city_input}%')
    if origin_state_input:
        origin_query = origin_query.ilike('state', f'%{origin_state_input}%')
    if origin_postal_code_input:
        origin_query = origin_query.ilike('postal_code', f'%{origin_postal_code_input}%')

    # query for destination
    destination_query = supabase.table('load_stop').select('*')
    if destination_city_input:
        destination_query = destination_query.ilike('city', f'%{destination_city_input}%')
    if destination_state_input:
        destination_query = destination_query.ilike('state', f'%{destination_state_input}%')
    if destination_postal_code_input:
        destination_query = destination_query.ilike('postal_code', f'%{destination_postal_code_input}%')

    origin_response = origin_query.execute()
    destination_response = destination_query.execute()

    # combine data
    origin_data = origin_response.data
    destination_data = destination_response.data

    return JsonResponse({'origin_results': origin_data, 'destination_results': destination_data}, safe=False)
