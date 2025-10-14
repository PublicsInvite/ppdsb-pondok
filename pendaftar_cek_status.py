from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
from ._supabase import supabase_client
from typing import Any, Dict

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        GET /api/pendaftar_cek_status?nomor=REG-20241014-000001
        Response: { success: true, data: {...} }
        """
        try:
            # Parse query parameters
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            
            nomor = params.get('nomor', [''])[0].strip()
            
            if not nomor:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": False,
                    "error": "Nomor registrasi harus diisi"
                }).encode())
                return
            
            # Query Supabase (menggunakan ANON key karena public access)
            supa = supabase_client(service_role=False)
            result = supa.table("pendaftar").select("*").eq("nomor_registrasi", nomor).execute()
            
            if not result.data:  # type: ignore
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": False,
                    "error": "Nomor registrasi tidak ditemukan"
                }).encode())
                return
            
            row: Dict[str, Any] = result.data[0]  # type: ignore
            
            # Transform data
            data = {
                "nomorRegistrasi": row.get("nomor_registrasi", ""),
                "nama": row.get("namalengkap", ""),
                "nik": row.get("nikcalon", ""),
                "tanggalLahir": row.get("tanggallahir", ""),
                "status": str(row.get("statusberkas", "pending")).lower(),
                "alasan": row.get("alasan") or "",
                "created_at": row.get("createdat", "")
            }
            
            # Response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "data": data
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": False,
                "error": str(e)
            }).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
