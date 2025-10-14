# 🚨 URGENT: FIX RLS POLICY

## Masalah:

API `pendaftar_create` mendapat error:

```
new row violates row-level security policy for table "pendaftar"
```

Ini karena RLS policy tidak mengizinkan role `anon` untuk INSERT.

---

## ✅ SOLUSI - Langkah demi Langkah:

### 1️⃣ Buka Supabase SQL Editor

👉 **https://supabase.com/dashboard/project/pislnvhdmsxudltcuuku/editor**

### 2️⃣ Klik "+ New query"

### 3️⃣ Copy-Paste SQL ini:

```sql
-- Disable RLS temporarily
ALTER TABLE pendaftar DISABLE ROW LEVEL SECURITY;

-- Drop ALL existing policies
DROP POLICY IF EXISTS "Allow public insert" ON pendaftar;
DROP POLICY IF EXISTS "Allow service role all" ON pendaftar;
DROP POLICY IF EXISTS "Enable insert for anon users" ON pendaftar;
DROP POLICY IF EXISTS "Enable insert for authenticated users" ON pendaftar;

-- Re-enable RLS
ALTER TABLE pendaftar ENABLE ROW LEVEL SECURITY;

-- Create NEW policy for INSERT (public/anon)
CREATE POLICY "public_insert_policy"
ON pendaftar
FOR INSERT
TO anon, authenticated
WITH CHECK (true);

-- Create policy for ALL operations (service_role only)
CREATE POLICY "service_role_all_policy"
ON pendaftar
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- Grant permissions
GRANT INSERT ON pendaftar TO anon, authenticated;
GRANT ALL ON pendaftar TO service_role;
```

### 4️⃣ Klik "Run" atau tekan `Ctrl/Cmd + Enter`

### 5️⃣ Verify - Run query ini untuk cek:

```sql
SELECT
    policyname,
    roles,
    cmd
FROM pg_policies
WHERE tablename = 'pendaftar';
```

**Expected result:**

```
policyname              | roles                    | cmd
------------------------|--------------------------|-------
public_insert_policy    | {anon,authenticated}     | INSERT
service_role_all_policy | {service_role}           | ALL
```

---

## 🧪 Test Setelah Fix:

### Test 1: Via Python Script

```bash
cd "/Users/dewasatriaaa/Downloads/KULIAH/PROJECT CODE/project python"
.venv/bin/python test_rls_anon.py
```

**Expected output:**

```
✅ SUCCESS! RLS policy is working correctly!
📋 ID: [number]
📋 Nomor: REG-20251014-00000X
```

### Test 2: Via API Production

```bash
curl -X POST "https://project-python-a35l9u1vt-dewas-projects-d0163f17.vercel.app/api/pendaftar_create" \
-H "Content-Type: application/json" \
-d '{
  "nikCalon": "3201234567890123",
  "kkNo": "3201234567890001",
  "nisn": "0012345678",
  "namaLengkap": "Test Success",
  "tempatLahir": "Jakarta",
  "tanggalLahir": "2008-05-15",
  "jenisKelamin": "L",
  "alamatJalan": "Jl. Test",
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
}'
```

**Expected output:**

```json
{
  "ok": true,
  "id": [number],
  "nomorRegistrasi": "REG-20251014-00000X"
}
```

---

## 📋 File SQL:

Saya sudah buatkan file `fix-rls-policy.sql` yang bisa langsung di-copy.

---

## ⚠️ Troubleshooting:

### Jika masih error setelah run SQL:

1. Pastikan SQL dijalankan tanpa error
2. Refresh browser Supabase Dashboard
3. Tunggu 30 detik untuk schema cache refresh
4. Test lagi dengan script Python

### Jika policy tidak muncul:

1. Cek apakah tabel `pendaftar` ada
2. Run query: `SELECT * FROM pg_policies WHERE tablename = 'pendaftar';`
3. Jika kosong, run ulang SQL fix

---

## 🎯 Setelah Success:

Website akan berfungsi penuh:

- ✅ Form pendaftaran bisa submit
- ✅ Data masuk ke database
- ✅ Auto-generate nomor registrasi
- ✅ Admin bisa lihat list pendaftar
- ✅ Admin bisa update status

---

**Silakan run SQL di atas dan kabari saya hasilnya!** 🚀
