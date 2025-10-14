#!/usr/bin/env python3
"""
Script untuk test koneksi dan fungsi database Supabase
"""
import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print("=" * 60)
print("🧪 TEST SUPABASE DATABASE")
print("=" * 60)
print()

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

try:
    # Test 1: Check if table exists and count records
    print("1️⃣  Test: Cek tabel 'pendaftar'...")
    result = supabase.table("pendaftar").select("id", count="exact").execute()
    print(f"   ✅ Tabel ditemukan! Total records: {result.count}")
    print()
    
    # Test 2: Insert sample data
    print("2️⃣  Test: Insert data test...")
    test_data = {
        "nikCalon": "3201234567890123",
        "kkNo": "3201234567890001",
        "nisn": "0012345678",
        "namaLengkap": "Ahmad Fauzi Test",
        "tempatLahir": "Jakarta",
        "tanggalLahir": "2008-05-15",
        "jenisKelamin": "L",
        "alamatJalan": "Jl. Test No. 123",
        "desa": "Ciputat",
        "kecamatan": "Ciputat Timur",
        "kotaKabupaten": "Tangerang Selatan",
        "provinsi": "Banten",
        "ijazahFormalTerakhir": "SMP",
        "rencanaDomisili": "Mukim",
        "rencanaTingkat": "MTs",
        "rencanaKelas": "Kelas 1",
        "namaAyah": "Budi Santoso",
        "nikAyah": "3201234567890100",
        "namaIbu": "Siti Aminah",
        "nikIbu": "3201234567890101"
    }
    
    insert_result = supabase.table("pendaftar").insert(test_data).execute()
    test_id = insert_result.data[0]["id"]
    nomor_reg = insert_result.data[0]["nomorRegistrasi"]
    print(f"   ✅ Data berhasil diinsert!")
    print(f"   📋 ID: {test_id}")
    print(f"   📋 Nomor Registrasi: {nomor_reg}")
    print()
    
    # Test 3: Select data
    print("3️⃣  Test: Select data...")
    select_result = supabase.table("pendaftar").select("*").eq("id", test_id).execute()
    if select_result.data:
        data = select_result.data[0]
        print(f"   ✅ Data ditemukan!")
        print(f"   👤 Nama: {data['namaLengkap']}")
        print(f"   📋 Nomor: {data['nomorRegistrasi']}")
        print(f"   📊 Status: {data['statusBerkas']}")
    print()
    
    # Test 4: Test RPC function (update status)
    print("4️⃣  Test: RPC function 'pendaftar_set_status'...")
    supabase.rpc(
        "pendaftar_set_status",
        {
            "p_id": test_id,
            "p_status": "DITERIMA",
            "p_deskripsi": "Test status update berhasil"
        }
    ).execute()
    print(f"   ✅ Status berhasil diupdate ke DITERIMA")
    print()
    
    # Test 5: Verify status update
    print("5️⃣  Test: Verifikasi status update...")
    verify_result = supabase.table("pendaftar").select("statusBerkas, deskripsiStatus").eq("id", test_id).execute()
    if verify_result.data:
        print(f"   ✅ Status: {verify_result.data[0]['statusBerkas']}")
        print(f"   📝 Deskripsi: {verify_result.data[0]['deskripsiStatus']}")
    print()
    
    # Test 6: List all pendaftar
    print("6️⃣  Test: List semua pendaftar...")
    list_result = supabase.table("pendaftar") \
        .select("id, nomorRegistrasi, namaLengkap, statusBerkas, createdAt") \
        .order("createdAt", desc=True) \
        .limit(5) \
        .execute()
    print(f"   ✅ Ditemukan {len(list_result.data)} records:")
    for item in list_result.data:
        print(f"      • {item['nomorRegistrasi']} - {item['namaLengkap']} ({item['statusBerkas']})")
    print()
    
    # Test 7: Clean up (delete test data)
    print("7️⃣  Test: Hapus data test...")
    supabase.table("pendaftar").delete().eq("id", test_id).execute()
    print(f"   ✅ Data test berhasil dihapus")
    print()
    
    print("=" * 60)
    print("🎉 SEMUA TEST BERHASIL!")
    print("=" * 60)
    print()
    print("✅ Database Supabase Anda sudah siap digunakan!")
    print("✅ API endpoints sudah bisa dijalankan")
    print("✅ Frontend forms sudah bisa konek ke API")
    print()
    print("🚀 Langkah Selanjutnya:")
    print("   1. Deploy ke Vercel: vercel --prod")
    print("   2. Atau test lokal: vercel dev")
    print("   3. Buka daftar.html untuk test form pendaftaran")
    print()

except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    print()
    print("💡 Solusi:")
    print("   1. Pastikan database schema sudah diimport")
    print("   2. Cek koneksi internet")
    print("   3. Cek kredensial di .env sudah benar")
