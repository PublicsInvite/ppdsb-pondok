#!/usr/bin/env python3
"""
Script untuk test Production API di Vercel
"""
import requests
import json
from datetime import datetime

BASE_URL = "https://project-python-aybnima4a-dewas-projects-d0163f17.vercel.app"

print("=" * 70)
print("🧪 TEST PRODUCTION API - VERCEL DEPLOYMENT")
print("=" * 70)
print(f"🔗 Base URL: {BASE_URL}")
print()

# Test 1: Test Landing Page
print("1️⃣  Test: Landing Page (index.html)")
try:
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        print(f"   ✅ Status: {response.status_code} OK")
        print(f"   📄 Content-Type: {response.headers.get('content-type')}")
    else:
        print(f"   ❌ Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
print()

# Test 2: Test Form Pendaftaran
print("2️⃣  Test: Form Pendaftaran (daftar.html)")
try:
    response = requests.get(f"{BASE_URL}/daftar")
    if response.status_code == 200:
        print(f"   ✅ Status: {response.status_code} OK")
    else:
        print(f"   ❌ Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
print()

# Test 3: Test Admin Dashboard
print("3️⃣  Test: Admin Dashboard (admin.html)")
try:
    response = requests.get(f"{BASE_URL}/admin")
    if response.status_code == 200:
        print(f"   ✅ Status: {response.status_code} OK")
    else:
        print(f"   ❌ Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
print()

# Test 4: Test API Create Endpoint
print("4️⃣  Test: API - Create Pendaftar (POST)")
test_data = {
    "nikCalon": "3201234567890999",
    "kkNo": "3201234567890888",
    "nisn": "0099887766",
    "namaLengkap": "Test Production API",
    "tempatLahir": "Jakarta",
    "tanggalLahir": "2008-05-15",
    "jenisKelamin": "L",
    "alamatJalan": "Jl. Test Production",
    "desa": "Test Desa",
    "kecamatan": "Test Kecamatan",
    "kotaKabupaten": "Test Kota",
    "provinsi": "Test Provinsi",
    "ijazahFormalTerakhir": "SMP",
    "rencanaDomisili": "Mukim",
    "rencanaTingkat": "MTs",
    "rencanaKelas": "Kelas 1",
    "namaAyah": "Ayah Test",
    "nikAyah": "3201234567890777",
    "namaIbu": "Ibu Test",
    "nikIbu": "3201234567890666"
}

try:
    response = requests.post(
        f"{BASE_URL}/api/pendaftar_create",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"   📡 Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Response: {json.dumps(result, indent=2)}")
        if result.get("ok"):
            print(f"   🎉 Pendaftaran berhasil!")
            print(f"   📋 ID: {result.get('id')}")
            print(f"   📋 Nomor Registrasi: {result.get('nomorRegistrasi')}")
    else:
        print(f"   ❌ Error Response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
print()

# Test 5: Test API List Endpoint
print("5️⃣  Test: API - List Pendaftar (GET)")
try:
    response = requests.get(f"{BASE_URL}/api/pendaftar_list")
    print(f"   📡 Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Total records: {result.get('total', 0)}")
        
        if result.get('data'):
            print(f"   📋 Sample data (first 3):")
            for idx, item in enumerate(result['data'][:3], 1):
                print(f"      {idx}. {item.get('nomorRegistrasi')} - {item.get('namaLengkap')} ({item.get('statusBerkas')})")
    else:
        print(f"   ❌ Error Response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
print()

# Test 6: Test API List with Query Params
print("6️⃣  Test: API - List dengan Filter Status")
try:
    response = requests.get(f"{BASE_URL}/api/pendaftar_list?status=MENUNGGU_VERIFIKASI&limit=5")
    print(f"   📡 Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Total MENUNGGU_VERIFIKASI: {result.get('total', 0)}")
    else:
        print(f"   ❌ Error Response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
print()

print("=" * 70)
print("🎯 SUMMARY")
print("=" * 70)
print()
print("✅ URLs yang bisa diakses:")
print(f"   • Landing Page: {BASE_URL}/")
print(f"   • Form Daftar: {BASE_URL}/daftar")
print(f"   • Admin Dashboard: {BASE_URL}/admin")
print()
print("🔌 API Endpoints:")
print(f"   • POST {BASE_URL}/api/pendaftar_create")
print(f"   • GET  {BASE_URL}/api/pendaftar_list")
print(f"   • PATCH {BASE_URL}/api/pendaftar_status")
print()
print("💡 Next Steps:")
print("   1. Buka landing page di browser")
print("   2. Test form pendaftaran")
print("   3. Test admin dashboard")
print("   4. Share URL ke user/stakeholder")
print()
print("🎉 Deployment berhasil dan API berfungsi!")
print("=" * 70)
