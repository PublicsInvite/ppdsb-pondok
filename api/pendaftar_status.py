from http.server import BaseHTTPRequestHandler
import json
from typing import Any, Dict
from ._supabase import supabase_client

class handler(BaseHTTPRequestHandler):
    def do_PATCH(self):
        """
        PATCH /api/pendaftar_status
        Body: { id: 123, status: "diterima" | "ditolak" | "pending" | "revisi", alasan?: "...", verifiedBy?: "admin@email.com" }
        Response: { success: true }
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
                    "success": False,
                    "error": "id and status are required"
                }).encode())
                return
            
            p_id = data["id"]
            p_status = data["status"].upper()  # Convert to uppercase
            p_alasan = data.get("alasan", None)
            p_verified_by = data.get("verifiedBy", "admin")
            
            # Map lowercase status to uppercase for database
            status_map = {
                'PENDING': 'PENDING',
                'REVISI': 'REVISI',
                'DITERIMA': 'DITERIMA',
                'DITOLAK': 'DITOLAK'
            }
            
            p_status = status_map.get(p_status, p_status)
            
            # Validasi status value
            valid_statuses = ['PENDING', 'REVISI', 'DITERIMA', 'DITOLAK']
            if p_status not in valid_statuses:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": False,
                    "error": f"status must be one of: pending, revisi, diterima, ditolak"
                }).encode())
                return
            
            # Update dengan service-role
            supa = supabase_client(service_role=True)
            
            # Prepare update payload
            update_payload: Dict[str, Any] = {
                "statusberkas": p_status,
            }
            
            # Add alasan if provided
            if p_alasan:
                update_payload["alasan"] = p_alasan
            
            # Add verifiedby for non-pending status
            if p_status != 'PENDING':
                update_payload["verifiedby"] = p_verified_by
            
            # Execute update
            result = supa.table("pendaftar").update(update_payload).eq("id", p_id).execute()
            
            # Response success
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True
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
        self.send_header('Access-Control-Allow-Methods', 'PATCH, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
