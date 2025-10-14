from http.server import BaseHTTPRequestHandler
import json
import os
from supabase import create_client

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get all pembayaran from pembayaran table, ordered by newest first
            result = supabase.table('pembayaran').select('*').order('created_at', desc=True).execute()
            
            # Get data safely
            result_data = getattr(result, 'data', [])
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = {
                'data': result_data if result_data else [],
                'count': len(result_data) if result_data else 0
            }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            print(f"Error in pembayaran_list: {str(e)}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': str(e),
                'data': [],
                'count': 0
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
