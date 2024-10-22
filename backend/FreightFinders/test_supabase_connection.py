import os
from supabase import create_client

# Supabase connection details
url = 'https://nzgwfdbdzvjwrwbnvuyz.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im56Z3dmZGJkenZqd3J3Ym52dXl6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjg3OTU4MDMsImV4cCI6MjA0NDM3MTgwM30.mray0Yy0FonLxFG6J_mkr1lBXs_YLdzcRImXoj2kfXI'  #  actual API key

# Create a Supabase client
supabase = create_client(url, key)

# Fetch 10 records from the "load_posting" table
#response = supabase.table("load_posting").select("*").limit(10).execute()
response = supabase.table("load_stop").select("*").limit(10).execute()

# Print the result
print(response)
