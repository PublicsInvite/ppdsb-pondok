from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import parse_qs
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
            
            # Validate required fields (nomor_rekening dan nama_rekening optional)
            required_fields = ['nomor_registrasi', 'nama_lengkap', 'bukti_pembayaran']
            for field in required_fields:
                if field not in data or not data[field]:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        'error': f'Field {field} is required'
                    }).encode())
                    return
            
            # Check if pendaftar exists (kolom sudah diubah jadi nomor_registrasi)
            pendaftar = supabase.table('pendaftar').select('*').eq('nomor_registrasi', data['nomor_registrasi']).execute()
            
            pendaftar_data = getattr(pendaftar, 'data', None)
            if not pendaftar_data:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'Nomor registrasi tidak ditemukan'
                }).encode())
                return
            
            # Check if payment already exists
            existing_payment = supabase.table('pembayaran').select('*').eq('nomor_registrasi', data['nomor_registrasi']).execute()
            
            existing_data = getattr(existing_payment, 'data', None)
            if existing_data:
                # Update existing payment
                result = supabase.table('pembayaran').update({
                    'bukti_pembayaran': data['bukti_pembayaran'],
                    'status_pembayaran': 'PENDING',
                    'catatan_admin': data.get('catatan', '')
                }).eq('nomor_registrasi', data['nomor_registrasi']).execute()
                
                response_data = {
                    'message': 'Pembayaran berhasil diupdate',
                    'nomor_pembayaran': existing_data[0]['nomor_pembayaran'],
                    'status': 'updated'
                }
            else:
                # Generate nomor pembayaran using database function
                nomor_result = supabase.rpc('generate_nomor_pembayaran').execute()
                nomor_pembayaran = nomor_result.data
                
                # Insert new payment
                payment_data = {
                    'nomor_pembayaran': nomor_pembayaran,
                    'nomor_registrasi': data['nomor_registrasi'],
                    'nama_lengkap': data['nama_lengkap'],
                    'jumlah': 500000.00,
                    'metode_pembayaran': 'Transfer Bank BRI',
                    'bukti_pembayaran': data['bukti_pembayaran'],
                    'status_pembayaran': 'PENDING',
                    'catatan_admin': data.get('catatan', '')
                }
                
                result = supabase.table('pembayaran').insert(payment_data).execute()
                
                response_data = {
                    'message': 'Pembayaran berhasil disubmit',
                    'nomor_pembayaran': nomor_pembayaran,
                    'status': 'created'
                }
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            print(f"Error in pembayaran_submit: {str(e)}")
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
