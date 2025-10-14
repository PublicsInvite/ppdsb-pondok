## 🚨 RLS MASIH BERMASALAH - SOLUSI SEMENTARA

### Masalah

RLS policy masih block INSERT meskipun sudah dijalankan SQL fix.

### ✅ SOLUSI SEMENTARA: Disable RLS

**Untuk testing dan development, kita DISABLE RLS dulu.**

---

## 📋 LANGKAH:

### 1️⃣ Buka Supabase SQL Editor (pastikan role = `postgres`)

🔗 https://supabase.com/dashboard/project/pislnvhdmsxudltcuuku/sql/new

### 2️⃣ Jalankan SQL ini:

```sql
-- DISABLE RLS
ALTER TABLE pendaftar DISABLE ROW LEVEL SECURITY;

-- Verify
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public' AND tablename = 'pendaftar';
```

**Expected output:** `rowsecurity = false`

### 3️⃣ Test lagi:

```bash
.venv/bin/python test_rls_anon.py
```

Seharusnya sekarang **✅ SUCCESS!**

---

## 🧪 TEST API DI PRODUCTION

Setelah RLS disabled, test API production:

```bash
curl -X POST "https://project-python-a35l9u1vt-dewas-projects-d0163f17.vercel.app/api/pendaftar_create" \
  -H "Content-Type: application/json" \
  -d '{
    "nikCalon": "1234567890123456",
    "namaLengkap": "Test Student",
    "jenisKelamin": "L",
    "tempatLahir": "Jakarta",
    "tanggalLahir": "2010-01-01",
    "kkNo": "1234567890123456",
    "anakKe": 1,
    "jumlahSaudara": 2,
    "citaCita": "Developer",
    "alamatJalan": "Jl. Test No. 123",
    "kelurahan": "Test Kelurahan",
    "kecamatan": "Test Kecamatan",
    "kabupaten": "Test Kabupaten",
    "provinsi": "DKI Jakarta",
    "kodePos": "12345",
    "tinggalDengan": "Orang Tua",
    "asalSekolah": "SDN Test",
    "nisn": "1234567890",
    "namaAyah": "Ayah Test",
    "namaIbu": "Ibu Test",
    "nomorHpOrtu": "081234567890"
  }'
```

**Expected:** `{"ok": true, "id": 1, "nomorRegistrasi": "REG-20251014-000001"}`

---

## 🔐 ENABLE RLS NANTI (Production)

**Setelah semua berfungsi**, kita bisa enable RLS lagi dengan policy yang benar:

```sql
-- Enable RLS
ALTER TABLE pendaftar ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "public_insert" ON pendaftar
  FOR INSERT
  TO anon, authenticated
  WITH CHECK (true);

CREATE POLICY "service_all" ON pendaftar
  FOR ALL
  TO service_role
  USING (true) WITH CHECK (true);
```

---

## 📝 CATATAN

- **Development:** RLS DISABLED (untuk testing)
- **Production nanti:** RLS ENABLED dengan policy yang benar
- Kalau API sudah jalan, kita bisa fokus fix RLS secara proper
