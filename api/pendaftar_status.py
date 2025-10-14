from http.server import BaseHTTPRequestHandler
import json
from ._supabase import supabase_client

class handler(BaseHTTPRequestHandler):
    def do_PATCH(self):
        """
        PATCH /api/pendaftar_status
        Body: { id: 123, status: "DITERIMA" | "DITOLAK" | "MENUNGGU_VERIFIKASI", alasan?: "..." }
        Response: { ok: true }
        
        Calls Supabase RPC: pendaftar_set_status(p_id, p_status, p_deskripsi)
        """
        try:
            # Parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            # Validasi input
            if not data.get('id') or not data.get('status'):
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "ok": False,
                    "error": "id and status are required"
                }).encode())
                return
            
            p_id = data["id"]
            p_status = data["status"]
            p_deskripsi = data.get("alasan", None)
            
            # Validasi status value
            valid_statuses = ['MENUNGGU_VERIFIKASI', 'DITERIMA', 'DITOLAK']
            if p_status not in valid_statuses:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "ok": False,
                    "error": f"status must be one of: {', '.join(valid_statuses)}"
                }).encode())
                return
            
            # Call Supabase RPC with service-role
            supa = supabase_client(service_role=True)
            rpc_result = supa.rpc("pendaftar_set_status", {
                "p_id": p_id,
                "p_status": p_status,
                "p_deskripsi": p_deskripsi
            }).execute()
            
            # Response success
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": True
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": False,
                "error": str(e)
            }).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'PATCH, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
