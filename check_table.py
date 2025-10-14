#!/usr/bin/env python3
"""
Script untuk cek struktur tabel di Supabase
"""
import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print("🔍 Cek struktur database Supabase...")
print()

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

try:
    # Try simple query
    result = supabase.table("pendaftar").select("*").limit(1).execute()
    print("✅ Tabel 'pendaftar' ditemukan!")
    print(f"📊 Total columns yang tersedia: {len(result.data[0].keys()) if result.data else 'N/A'}")
    
    if result.data:
        print("\n📋 Kolom yang tersedia:")
        for key in sorted(result.data[0].keys()):
            print(f"   • {key}")
    else:
        print("\n⚠️  Tabel kosong, tapi struktur sudah ada")
    
    print("\n✅ Database Supabase siap digunakan!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print()
    print("💡 Kemungkinan penyebab:")
    print("   1. Schema belum selesai diimport")
    print("   2. Supabase perlu restart/refresh")
    print("   3. Nama kolom tidak sesuai")
    print()
    print("🔧 Solusi:")
    print("   1. Buka Supabase Dashboard > Table Editor")
    print("   2. Cek apakah tabel 'pendaftar' ada")
    print("   3. Jika tidak ada, re-run SQL schema")
    print("   4. Jika ada tapi kosong, coba restart Supabase project")
