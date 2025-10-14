from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
from ._supabase import supabase_client

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        GET /api/pendaftar_list?page=1&pageSize=10&q=&status=
        Response: { ok: true, rows: [...], page: 1, pageSize: 10 }
        
        Filter by:
        - q: search in namaLengkap
        - status: statusBerkas (MENUNGGU_VERIFIKASI, DITERIMA, DITOLAK)
        """
        try:
            # Parse query parameters
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            
            q = params.get('q', [''])[0].strip()
            status = params.get('status', [''])[0].strip()
            page = int(params.get('page', ['1'])[0])
            page_size = min(50, int(params.get('pageSize', ['10'])[0]))
            
            # Calculate range
            from_ = (page - 1) * page_size
            to_ = from_ + page_size - 1
            
            # Query Supabase with service-role for admin operations
            supa = supabase_client(service_role=True)
            query = supa.table("pendaftar").select("*").order("createdat", desc=True)
            
            # Apply filters
            if status:
                query = query.eq("statusBerkas", status)
            
            if q:
                # Search in namaLengkap (case-insensitive)
                query = query.ilike("namaLengkap", f"%{q}%")
            
            # Apply pagination
            res = query.range(from_, to_).execute()
            
            # Get total count
            count_res = supa.table("pendaftar").select("*", count="exact").execute()
            total = count_res.count if hasattr(count_res, 'count') else len(res.data)
            
            # Transform data untuk admin dashboard
            transformed_data = []
            for row in res.data:
                transformed_data.append({
                    "id": row.get("id"),
                    "nama": row.get("namalengkap", ""),
                    "email": row.get("emailcalon", "-"),
                    "no_hp": row.get("nomorhportu", "-"),
                    "alamat": f"{row.get('alamatjalan', '')}, {row.get('desa', '')}, {row.get('kecamatan', '')}",
                    "status": row.get("statusberkas", "pending").lower(),
                    "created_at": row.get("createdat", ""),
                    "alasan": row.get("alasan", "-"),
                    # Include original data for detail view
                    **row
                })
            
            # Response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "data": transformed_data,
                "total": total,
                "page": page,
                "limit": page_size
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
