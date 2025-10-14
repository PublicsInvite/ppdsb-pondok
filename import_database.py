#!/usr/bin/env python3
"""
Script untuk mengimport database schema ke Supabase
"""
import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print("❌ Error: SUPABASE_URL dan SUPABASE_SERVICE_ROLE_KEY harus diisi di .env")
    exit(1)

# Read SQL file
with open("supabase-schema.sql", "r") as f:
    sql_content = f.read()

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

print("🔄 Mengimport database schema ke Supabase...")
print(f"📍 URL: {SUPABASE_URL}")
print()

try:
    # Execute SQL
    result = supabase.rpc('exec_sql', {'sql': sql_content}).execute()
    print("✅ Database schema berhasil diimport!")
    print()
    print("📋 Tabel 'pendaftar' telah dibuat dengan:")
    print("   - 20+ kolom (NIK, KK, NISN, dll)")
    print("   - Auto-generate nomorRegistrasi")
    print("   - Trigger untuk updatedAt")
    print("   - RPC function: pendaftar_set_status")
    print("   - Row Level Security (RLS)")
    print("   - Indexes untuk performa")
    
except Exception as e:
    print(f"❌ Error saat import: {str(e)}")
    print()
    print("💡 Solusi:")
    print("   1. Pastikan SERVICE_ROLE_KEY sudah benar di .env")
    print("   2. Import manual via Supabase Dashboard > SQL Editor")
    print("   3. Copy-paste isi supabase-schema.sql ke SQL Editor")
    exit(1)
