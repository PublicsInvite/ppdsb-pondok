from http.server import BaseHTTPRequestHandler
import json
import re
from ._supabase import supabase_client

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """
        POST /api/pendaftar_create
        Body: Comprehensive registration data with NIK, family info, education, etc.
        Response: { ok: true, id: ..., nomorRegistrasi: ... }
        """
        try:
            # Parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            # Prepare payload with all required fields
            payload = {
                "nikCalon": data.get("nikCalon", "").strip(),
                "kkNo": data.get("kkNo", "").strip(),
                "nisn": (data.get("nisn") or "").strip() or None,
                "namaLengkap": data["namaLengkap"].strip(),
                "tempatLahir": data["tempatLahir"].strip(),
                "tanggalLahir": data["tanggalLahir"],  # "YYYY-MM-DD"
                "jenisKelamin": data["jenisKelamin"],  # 'L' / 'P'
                "alamatJalan": data["alamatJalan"].strip(),
                "desa": data["desa"].strip(),
                "kecamatan": data["kecamatan"].strip(),
                "kotaKabupaten": data["kotaKabupaten"].strip(),
                "provinsi": data["provinsi"].strip(),
                "ijazahFormalTerakhir": data["ijazahFormalTerakhir"].strip(),
                "rencanaDomisili": data["rencanaDomisili"].strip(),
                "rencanaTingkat": data["rencanaTingkat"].strip(),
                "rencanaKelas": data["rencanaKelas"].strip(),
                "namaAyah": data["namaAyah"].strip(),
                "nikAyah": data["nikAyah"].strip(),
                "namaIbu": data["namaIbu"].strip(),
                "nikIbu": data["nikIbu"].strip()
            }
            
            # Validasi jenisKelamin
            if not re.fullmatch(r"[LP]", payload["jenisKelamin"]):
                self.send_response(422)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "ok": False,
                    "error": "jenisKelamin invalid (must be 'L' or 'P')"
                }).encode())
                return
            
            # Insert ke Supabase (tabel: pendaftar)
            supa = supabase_client(service_role=False)
            res = supa.table("pendaftar").insert(payload).execute()
            
            if not res.data:
                raise Exception("Failed to create pendaftar")
            
            result_data = res.data[0]
            
            # Response success
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": True,
                "id": result_data["id"],
                "nomorRegistrasi": result_data["nomorRegistrasi"]
            }).encode())
            
        except KeyError as e:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": False,
                "error": f"Missing required field: {str(e)}"
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
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
