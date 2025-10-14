#!/usr/bin/env python3
"""
Test RLS policy dengan ANON key
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

print("🧪 Testing RLS with ANON_KEY...")
print()

# Create client with ANON_KEY (public role)
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

test_data = {
    "nikcalon": "3201234567890555",
    "kkno": "3201234567890444",
    "nisn": "0055443322",
    "namalengkap": "Test RLS ANON",
    "tempatlahir": "Jakarta",
    "tanggallahir": "2008-05-15",
    "jeniskelamin": "L",
    "alamatjalan": "Jl. RLS Test",
    "desa": "Test Desa",
    "kecamatan": "Test Kec",
    "kotakabupaten": "Test Kota",
    "provinsi": "Test Prov",
    "ijazahformalterakhir": "SMP",
    "rencanadomisili": "Mukim",
    "rencanatingkat": "MTs",
    "rencanakelas": "Kelas 1",
    "namaayah": "Ayah Test",
    "nikayah": "3201234567890333",
    "namaibu": "Ibu Test",
    "nikibu": "3201234567890222"
}

try:
    print("Attempting INSERT with ANON_KEY...")
    result = supabase.table("pendaftar").insert(test_data).execute()
    
    if result.data:
        print("✅ SUCCESS! RLS policy is working correctly!")
        print(f"📋 ID: {result.data[0]['id']}")
        print(f"📋 Nomor: {result.data[0]['nomorregistrasi']}")
        print()
        print("🎉 API should work now!")
    else:
        print("❌ No data returned")
        
except Exception as e:
    error_str = str(e)
    print(f"❌ ERROR: {error_str}")
    print()
    
    if "row-level security policy" in error_str:
        print("🔧 RLS Policy Problem!")
        print()
        print("Anda perlu run SQL ini di Supabase SQL Editor:")
        print()
        print("-- Drop existing policy")
        print("DROP POLICY IF EXISTS \"Allow public insert\" ON pendaftar;")
        print()
        print("-- Create new policy for anon role")
        print("CREATE POLICY \"Allow public insert\" ON pendaftar")
        print("  FOR INSERT")
        print("  TO anon")
        print("  WITH CHECK (true);")
        print()
        print("-- Verify RLS is enabled")
        print("ALTER TABLE pendaftar ENABLE ROW LEVEL SECURITY;")
        print()
        print("Link: https://supabase.com/dashboard/project/pislnvhdmsxudltcuuku/editor")
