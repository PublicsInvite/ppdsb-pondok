import os
from supabase import create_client, Client

def supabase_client(service_role: bool = False) -> Client:
    """
    Create a Supabase client instance.
    
    Args:
        service_role: If True, uses SERVICE_ROLE_KEY (for admin operations)
                     If False, uses ANON_KEY (for public operations)
    """
    url = "https://pislnvhdmsxudltcuuku.supabase.co"
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"] if service_role else os.environ["SUPABASE_ANON_KEY"]
    return create_client(url, key)
