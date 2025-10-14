#!/usr/bin/env python3
"""
Script untuk cek nama kolom exact di Supabase
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

print("🔍 Checking exact column names in Supabase...")
print()

try:
    # Try to get schema info by selecting with limit 0
    result = supabase.table("pendaftar").select("*").limit(0).execute()
    print("✅ Table exists!")
    print()
    
    # Insert test data with all lowercase column names
    test_data_lowercase = {
        "nikcalon": "3201234567890999",
        "kkno": "3201234567890888",
        "nisn": "0099887766",
        "namalengkap": "Test Lowercase",
        "tempatlahir": "Jakarta",
        "tanggallahir": "2008-05-15",
        "jeniskelamin": "L",
        "alamatjalan": "Jl. Test",
        "desa": "Test Desa",
        "kecamatan": "Test Kec",
        "kotakabupaten": "Test Kota",
        "provinsi": "Test Prov",
        "ijazahformalterakhir": "SMP",
        "rencanadomisili": "Mukim",
        "rencanatingkat": "MTs",
        "rencanakelas": "Kelas 1",
        "namaayah": "Ayah Test",
        "nikayah": "3201234567890777",
        "namaibu": "Ibu Test",
        "nikibu": "3201234567890666"
    }
    
    print("Testing with all lowercase column names...")
    result = supabase.table("pendaftar").insert(test_data_lowercase).execute()
    
    if result.data:
        print("✅ INSERT SUCCESS with lowercase!")
        print(f"📋 ID: {result.data[0]['id']}")
        print(f"📋 Nomor: {result.data[0].get('nomorregistrasi') or result.data[0].get('nomorRegistrasi')}")
        print()
        print("💡 Gunakan LOWERCASE untuk semua nama kolom!")
        
        # Get inserted data to see exact column names
        print()
        print("📋 Exact column names returned:")
        for key in sorted(result.data[0].keys()):
            print(f"   • {key}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
