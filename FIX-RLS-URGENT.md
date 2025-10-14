# 🔧 FIX RLS POLICY - URGENT!

## Masalah:

API `/api/pendaftar_create` error dengan pesan:

```
new row violates row-level security policy for table "pendaftar"
```

Ini berarti RLS (Row Level Security) policy memblock INSERT dari ANON key.

---

## ✅ SOLUSI - Run SQL ini di Supabase:

### **Langkah 1: Buka SQL Editor**

👉 https://supabase.com/dashboard/project/pislnvhdmsxudltcuuku/sql

### **Langkah 2: Copy & Paste SQL berikut**

```sql
-- Drop existing policies
DROP POLICY IF EXISTS "Allow public insert" ON pendaftar;
DROP POLICY IF EXISTS "Allow service role all" ON pendaftar;

-- Policy 1: Allow INSERT for anon and authenticated
CREATE POLICY "Allow public insert"
  ON pendaftar
  FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

-- Policy 2: Allow ALL for service_role (admin)
CREATE POLICY "Allow service role all"
  ON pendaftar
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);
```

### **Langkah 3: Run SQL**

Klik tombol **"Run"** atau tekan `Ctrl/Cmd + Enter`

### **Langkah 4: Test API lagi**

```bash
curl -X POST "https://project-python-89svr23gq-dewas-projects-d0163f17.vercel.app/api/pendaftar_create" \
  -H "Content-Type: application/json" \
  -d '{
    "nikCalon": "3201234567890999",
    "kkNo": "3201234567891111",
    "namaLengkap": "Test RLS",
    "tempatLahir": "Jakarta",
    "tanggalLahir": "2008-05-15",
    "jenisKelamin": "L",
    "alamatJalan": "Jl. Test",
    "desa": "Test",
    "kecamatan": "Test",
    "kotaKabupaten": "Test",
    "provinsi": "Test",
    "ijazahFormalTerakhir": "SMP",
    "rencanaDomisili": "Mukim",
    "rencanaTingkat": "MTs",
    "rencanaKelas": "Kelas 1",
    "namaAyah": "Test Ayah",
    "nikAyah": "3201234567892222",
    "namaIbu": "Test Ibu",
    "nikIbu": "3201234567893333"
  }'
```

---

## 📋 File SQL:

Sudah dibuat di: **`fix-rls-policy.sql`**

---

## ✅ Setelah Fix RLS:

API akan berfungsi normal:

- ✅ `/api/pendaftar_create` - Public registration
- ✅ `/api/pendaftar_list` - Admin list
- ✅ `/api/pendaftar_status` - Admin update status

---

## 🎯 PRODUCTION URL:

https://project-python-89svr23gq-dewas-projects-d0163f17.vercel.app

**SILAKAN FIX RLS POLICY SEKARANG!** 🚨
