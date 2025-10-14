# 📋 PANDUAN IMPORT DATABASE KE SUPABASE

## ✅ Langkah-langkah Import Database:

### 1️⃣ Buka SQL Editor

- Buka browser dan kunjungi: https://supabase.com/dashboard/project/pislnvhdmsxudltcuuku/sql
- Atau dari dashboard Supabase Anda, klik menu **"SQL Editor"** di sidebar kiri

### 2️⃣ Buat Query Baru

- Klik tombol **"+ New query"** di pojok kanan atas
- Atau klik **"New blank query"**

### 3️⃣ Copy SQL Schema

- Buka file `supabase-schema.sql` di project ini
- Copy SELURUH isi file (Ctrl/Cmd + A, lalu Ctrl/Cmd + C)

### 4️⃣ Paste dan Run

- Paste ke SQL Editor (Ctrl/Cmd + V)
- Klik tombol **"Run"** atau tekan **Ctrl/Cmd + Enter**
- Tunggu hingga muncul pesan sukses

### 5️⃣ Verifikasi Import

- Klik menu **"Table Editor"** di sidebar
- Anda harus melihat tabel baru: **"pendaftar"**
- Klik tabel tersebut untuk melihat struktur kolom

---

## 📊 Yang Akan Dibuat:

### Tabel: `pendaftar`

- ✅ 20+ kolom (NIK, KK, NISN, nama, alamat, dll)
- ✅ Auto-generate `nomorRegistrasi` (format: REG-YYYYMMDD-000001)
- ✅ Status: MENUNGGU_VERIFIKASI, DITERIMA, DITOLAK
- ✅ Timestamps otomatis (createdAt, updatedAt)

### Functions & Triggers:

- ✅ `generate_nomor_registrasi()` - Auto-generate nomor registrasi
- ✅ `update_timestamp()` - Auto-update updatedAt
- ✅ `pendaftar_set_status()` - RPC untuk update status

### Security:

- ✅ Row Level Security (RLS) enabled
- ✅ Public dapat INSERT (form pendaftaran)
- ✅ Service role dapat SELECT/UPDATE/DELETE (admin)

### Indexes:

- ✅ Index pada statusBerkas
- ✅ Index pada createdAt (descending)
- ✅ Index pada namaLengkap
- ✅ Index pada nomorRegistrasi

---

## ⚠️ Troubleshooting:

### Jika ada error "relation already exists":

Artinya tabel sudah ada. Anda bisa:

1. Drop tabel dulu: `DROP TABLE IF EXISTS pendaftar CASCADE;`
2. Lalu run lagi schema SQL

### Jika ada error permission:

Pastikan Anda login sebagai owner project di Supabase Dashboard

---

## 🧪 Test Database (Opsional):

Setelah import berhasil, Anda bisa insert data test:

```sql
-- Test insert data
INSERT INTO pendaftar (
  nikCalon, kkNo, nisn, namaLengkap, tempatLahir, tanggalLahir, jenisKelamin,
  alamatJalan, desa, kecamatan, kotaKabupaten, provinsi,
  ijazahFormalTerakhir, rencanaDomisili, rencanaTingkat, rencanaKelas,
  namaAyah, nikAyah, namaIbu, nikIbu
) VALUES (
  '3201234567890123', '3201234567890001', '0012345678', 'Ahmad Fauzi',
  'Jakarta', '2008-05-15', 'L',
  'Jl. Raya Pondok No. 123', 'Ciputat', 'Ciputat Timur', 'Tangerang Selatan', 'Banten',
  'SMP', 'Mukim', 'MTs', 'Kelas 1',
  'Budi Santoso', '3201234567890100', 'Siti Aminah', '3201234567890101'
);

-- Test select data
SELECT id, nomorRegistrasi, namaLengkap, statusBerkas, createdAt
FROM pendaftar
ORDER BY createdAt DESC;
```

---

## ✅ Setelah Import Berhasil:

1. **Test API Create**: Buka `daftar.html` dan coba submit form
2. **Test API List**: Buka `admin.html` dan lihat daftar pendaftar
3. **Deploy ke Vercel**: Jalankan `vercel` atau `vercel --prod`

---

## 📞 Butuh Bantuan?

Jika ada masalah saat import, screenshot error-nya dan kirim ke sini!
