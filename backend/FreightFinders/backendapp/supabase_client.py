from supabase import create_client
from django.conf import settings

def get_supabase_client():
    """
    Returns a Supabase client using the settings defined in settings.py
    """
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY
    return create_client(url, key)