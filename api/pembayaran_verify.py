from http.server import BaseHTTPRequestHandler
import json
import os
from supabase import create_client

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Validate required fields
            if 'nomor_pembayaran' not in data or 'status' not in data:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'nomor_pembayaran and status are required'
                }).encode())
                return
            
            # Validate status
            valid_statuses = ['VERIFIED', 'REJECTED']
            status = data['status'].upper()
            
            if status not in valid_statuses:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
                }).encode())
                return
            
            # Update payment status
            update_data = {
                'status_pembayaran': status,
                'verified_by': data.get('verified_by', 'admin'),
                'catatan_admin': data.get('catatan', '')
            }
            
            result = supabase.table('pembayaran').update(update_data).eq('nomor_pembayaran', data['nomor_pembayaran']).execute()
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'message': f'Pembayaran berhasil di{status.lower()}',
                'nomor_pembayaran': data['nomor_pembayaran'],
                'status': status
            }).encode())
            
        except Exception as e:
            print(f"Error in pembayaran_verify: {str(e)}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': str(e)
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
