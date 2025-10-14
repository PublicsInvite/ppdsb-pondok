from http.server import BaseHTTPRequestHandler
import json
import os
import base64
from datetime import datetime
from supabase import create_client, Client

# Supabase setup
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

supabase: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))

            file_base64 = data.get("file")
            file_name = data.get("fileName")
            file_type = data.get("fileType")
            nomor_registrasi = data.get("nomorRegistrasi")

            if not all([file_base64, file_name, nomor_registrasi]):
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"ok": False, "error": "Missing required fields"}).encode()
                )
                return

            # Decode base64 file
            file_data = base64.b64decode(file_base64)

            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_ext = file_name.split(".")[-1]
            unique_filename = f"{nomor_registrasi}/{file_type}_{timestamp}.{file_ext}"

            # Upload to Supabase Storage
            response = supabase.storage.from_("pendaftar-files").upload(
                path=unique_filename,
                file=file_data,
                file_options={"content-type": data.get("mimeType", "application/octet-stream")}
            )

            # Get public URL
            public_url = supabase.storage.from_("pendaftar-files").get_public_url(unique_filename)

            # Return success
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(
                json.dumps({"ok": True, "url": public_url}).encode()
            )

        except Exception as e:
            error_msg = str(e)
            
            # Check if bucket not found error
            if "Bucket not found" in error_msg or "404" in error_msg:
                error_msg = "Storage bucket 'pendaftar-files' belum dibuat. Silakan buat bucket terlebih dahulu di Supabase Dashboard > Storage. Lihat file SETUP_STORAGE.txt untuk panduan lengkap."
            
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(
                json.dumps({"ok": False, "error": error_msg}).encode()
            )

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
