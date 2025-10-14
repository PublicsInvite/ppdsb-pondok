#!/usr/bin/env python3
"""
Test RLS policy untuk ANON key
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

print("🔍 Testing RLS with ANON_KEY...")
print()

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

test_data = {
    "nikcalon": "3201234567899999",
    "kkno": "3201234567899998",
    "nisn": "0099999999",
    "namalengkap": "Test RLS",
    "tempatlahir": "Test",
    "tanggallahir": "2008-01-01",
    "jeniskelamin": "L",
    "alamatjalan": "Test",
    "desa": "Test",
    "kecamatan": "Test",
    "kotakabupaten": "Test",
    "provinsi": "Test",
    "ijazahformalterakhir": "SMP",
    "rencanadomisili": "Test",
    "rencanatingkat": "Test",
    "rencanakelas": "Test",
    "namaayah": "Test",
    "nikayah": "3201234567899997",
    "namaibu": "Test",
    "nikibu": "3201234567899996"
}

try:
    result = supabase.table("pendaftar").insert(test_data).execute()
    print("✅ INSERT BERHASIL dengan ANON_KEY!")
    print(f"📋 ID: {result.data[0]['id']}")
    print(f"📋 Nomor: {result.data[0]['nomorregistrasi']}")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print()
    print("💡 RLS policy mungkin perlu diperbaiki di Supabase!")
    print("   Run this SQL in Supabase SQL Editor:")
    print()
    print("   DROP POLICY IF EXISTS \"Allow public insert\" ON pendaftar;")
    print("   CREATE POLICY \"Allow public insert\" ON pendaftar")
    print("     FOR INSERT TO anon, authenticated")
    print("     WITH CHECK (true);")
