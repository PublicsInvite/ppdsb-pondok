from http.server import BaseHTTPRequestHandler
import json
import os
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

            pendaftar_id = data.get("id")
            if not pendaftar_id:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"ok": False, "error": "ID required"}).encode()
                )
                return

            # Prepare update data
            update_data = {}
            if data.get("file_ijazah"):
                update_data["file_ijazah"] = data["file_ijazah"]
            if data.get("file_kk"):
                update_data["file_kk"] = data["file_kk"]
            if data.get("file_akta"):
                update_data["file_akta"] = data["file_akta"]
            if data.get("file_foto"):
                update_data["file_foto"] = data["file_foto"]

            if not update_data:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"ok": False, "error": "No files to update"}).encode()
                )
                return

            # Update in Supabase
            response = (
                supabase.table("pendaftar")
                .update(update_data)
                .eq("id", pendaftar_id)
                .execute()
            )

            # Return success
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"ok": False, "error": str(e)}).encode()
            )

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
