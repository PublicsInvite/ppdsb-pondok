from http.server import BaseHTTPRequestHandler
import json
import re
from typing import Any, Dict
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
            
            # Prepare payload with all required fields (use lowercase for PostgreSQL)
            payload = {
                "nikcalon": data.get("nikCalon", "").strip(),
                "kkno": data.get("kkNo", "").strip(),
                "nisn": (data.get("nisn") or "").strip() or None,
                "namalengkap": data["namaLengkap"].strip(),
                "tempatlahir": data["tempatLahir"].strip(),
                "tanggallahir": data["tanggalLahir"],  # "YYYY-MM-DD"
                "jeniskelamin": data["jenisKelamin"],  # 'L' / 'P'
                "alamatjalan": data["alamatJalan"].strip(),
                "desa": data["desa"].strip(),
                "kecamatan": data["kecamatan"].strip(),
                "kotakabupaten": data["kotaKabupaten"].strip(),
                "provinsi": data["provinsi"].strip(),
                "ijazahformalterakhir": data["ijazahFormalTerakhir"].strip(),
                "rencanadomisili": data["rencanaDomisili"].strip(),
                "rencanatingkat": data["rencanaTingkat"].strip(),
                "rencanakelas": data["rencanaKelas"].strip(),
                "namaayah": data["namaAyah"].strip(),
                "nikayah": data["nikAyah"].strip(),
                "namaibu": data["namaIbu"].strip(),
                "nikibu": data["nikIbu"].strip(),
                "teleponortu": data.get("teleponOrtu", "").strip(),
                "statusberkas": "PENDING"  # Set default status UPPERCASE
            }
            
            # Validasi jenisKelamin
            if not re.fullmatch(r"[LP]", payload["jeniskelamin"]):
                self.send_response(422)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "ok": False,
                    "error": "jenisKelamin invalid (must be 'L' or 'P')"
                }).encode())
                return
            
                        
            # Insert to Supabase using ANON_KEY (public registration, allowed by RLS)
            supa = supabase_client(service_role=False)  # Use ANON_KEY
            result = supa.table("pendaftar").insert(payload).execute()
            
            if not result.data:  # type: ignore
                raise Exception("Failed to create pendaftar")
            
            result_data: Dict[str, Any] = result.data[0]  # type: ignore
            
            # Response success
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": True,
                "id": result_data["id"],
                "nomorRegistrasi": result_data.get("nomor_registrasi") or result_data.get("nomorRegistrasi")
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
