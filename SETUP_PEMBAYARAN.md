# 💳 SETUP SISTEM PEMBAYARAN

## 🚀 URL Production

**https://project-python-m23c0ptxq-dewas-projects-d0163f17.vercel.app**

---

## 📋 LANGKAH SETUP DATABASE

### STEP 1: Jalankan SQL di Supabase

1. Buka **Supabase Dashboard**: https://supabase.com/dashboard
2. Pilih project Anda
3. Klik menu **SQL Editor** di sidebar kiri
4. Klik tombol **New Query**
5. Copy semua isi file `sql_pembayaran.sql`
6. Paste ke SQL Editor
7. Klik **Run** atau tekan `Ctrl/Cmd + Enter`

### STEP 2: Verifikasi Database

Jalankan query berikut untuk memastikan setup berhasil:

```sql
-- Cek tabel pembayaran
SELECT * FROM pembayaran LIMIT 5;

-- Cek view pembayaran
SELECT * FROM v_pembayaran_report LIMIT 5;

-- Test generate nomor pembayaran
SELECT generate_nomor_pembayaran();

-- Cek konfigurasi
SELECT * FROM konfigurasi_pembayaran;
```

---

## 🎯 CARA MENGGUNAKAN (User Flow)

### 1. **User Mendaftar**

- Buka: `/daftar.html`
- Isi formulir pendaftaran
- Submit dan dapat nomor registrasi

### 2. **Admin Verifikasi Pendaftaran**

- Login admin: `/login` (atau `/admin.html`)
- Tab "Data Pendaftar"
- Klik tombol "Terima" untuk approve pendaftar
- Status berubah jadi **DITERIMA**

### 3. **User Cek Status**

- Buka: `/cekstatus.html`
- Masukkan nomor registrasi
- Jika status **DITERIMA**, muncul tombol **"Lanjut ke Pembayaran"**

### 4. **User Lakukan Pembayaran**

- Klik tombol "Lanjut ke Pembayaran"
- Diarahkan ke: `/pembayaran.html?nomor=REG-xxx&nama=xxx`
- Lihat informasi rekening BRI:
  - **Bank**: BRI (Bank Rakyat Indonesia)
  - **Nomor Rekening**: 0012-01-123456-78-9
  - **Atas Nama**: Yayasan Pondok Pesantren
  - **Jumlah**: Rp 500.000

### 5. **User Upload Bukti Pembayaran**

- Transfer sesuai nominal ke rekening BRI yang tertera
- Upload bukti transfer (JPG/PNG/PDF, max 2MB)
- Tambahkan catatan jika diperlukan (opsional)
- Klik **"Kirim Bukti Pembayaran"**
- Tunggu verifikasi dari admin (maksimal 2x24 jam)

### 6. **Admin Verifikasi Pembayaran**

- Login admin
- Tab "Pembayaran" (akan ditambahkan)
- Lihat list pembayaran pending
- Klik tombol "Verifikasi" atau "Tolak"
- Status berubah: VERIFIED atau REJECTED

---

## 📊 DATABASE STRUCTURE

### Tabel: `pembayaran`

```sql
Column                  | Type           | Description
------------------------|----------------|----------------------------------
id                      | SERIAL         | Primary key
nomor_pembayaran        | VARCHAR(50)    | PAY-YYYYMMDD-XXXXX (unique, auto-generated)
nomor_registrasi        | VARCHAR(50)    | FK ke pendaftar (cascade delete)
nama_lengkap            | VARCHAR(255)   | Nama pendaftar
jumlah                  | DECIMAL(15,2)  | Default: 500000.00
metode_pembayaran       | VARCHAR(50)    | Default: 'Transfer Bank BRI'
bukti_pembayaran        | TEXT           | URL file bukti (Supabase Storage)
status_pembayaran       | VARCHAR(20)    | PENDING/VERIFIED/REJECTED
tanggal_upload          | TIMESTAMP      | Auto set saat insert
tanggal_verifikasi      | TIMESTAMP      | Auto set saat status berubah
verified_by             | VARCHAR(255)   | Email admin yang verifikasi
catatan_admin           | TEXT           | Catatan dari admin/user
created_at              | TIMESTAMP      | Auto timestamp
updated_at              | TIMESTAMP      | Auto update saat edit
```

### View: `v_pembayaran_report`

Join pembayaran + pendaftar untuk reporting:

- Nomor pembayaran
- Status pembayaran + pendaftaran
- Data lengkap pendaftar
- Keterangan status (Lunas/Menunggu/Ditolak)

### Function: `generate_nomor_pembayaran()`

Generate unique payment number:

- Format: `PAY-YYYYMMDD-XXXXX`
- Contoh: `PAY-20251014-12345`
- Random 5 digit number
- Loop sampai dapat nomor unique

### Triggers:

1. **update_pembayaran_timestamp**: Auto update `updated_at`
2. **set_pembayaran_verified_timestamp**: Auto set `tanggal_verifikasi` saat status jadi VERIFIED/REJECTED

---

## 🔌 API ENDPOINTS

### 1. POST `/api/pembayaran_submit`

Submit pembayaran baru atau update existing

**Request Body:**

```json
{
  "nomor_registrasi": "REG-20251014-00001",
  "nama_lengkap": "John Doe",
  "bukti_pembayaran": "https://storage.url/file.jpg",
  "catatan": "Transfer via BRI Mobile Banking"
}
```

**Response Success:**

```json
{
  "message": "Pembayaran berhasil disubmit",
  "nomor_pembayaran": "PAY-20251014-12345",
  "status": "created"
}
```

### 2. GET `/api/pembayaran_list`

Get semua pembayaran (untuk admin)

**Response:**

```json
{
  "data": [
    {
      "nomor_pembayaran": "PAY-20251014-12345",
      "nomor_registrasi": "REG-20251014-00001",
      "nama_lengkap": "John Doe",
      "jumlah": 500000.00,
      "status_pembayaran": "PENDING",
      "tanggal_upload": "2025-10-14T10:30:00",
      "status_pendaftaran": "DITERIMA",
      ...
    }
  ],
  "count": 1
}
```

### 3. POST `/api/pembayaran_verify`

Verifikasi atau tolak pembayaran (admin only)

**Request Body:**

```json
{
  "nomor_pembayaran": "PAY-20251014-12345",
  "status": "VERIFIED",
  "verified_by": "admin@email.com",
  "catatan": "Pembayaran telah diverifikasi"
}
```

**Response:**

```json
{
  "message": "Pembayaran berhasil diverified",
  "nomor_pembayaran": "PAY-20251014-12345",
  "status": "VERIFIED"
}
```

---

## 🎨 HALAMAN YANG DIBUAT

### 1. `/pembayaran.html`

**Fitur:**

- ✅ Step indicator (Cek Status → Pembayaran → Selesai)
- ✅ Info pendaftar (nomor registrasi, nama)
- ✅ Informasi pembayaran (biaya Rp 500.000)
- ✅ Detail rekening BRI dengan tombol copy
- ✅ Upload area drag & drop
- ✅ Preview image untuk bukti pembayaran
- ✅ Validasi file (max 2MB, format JPG/PNG/PDF)
- ✅ Field catatan opsional
- ✅ Responsive design

**Teknologi:**

- Bootstrap 5.3.0
- Bootstrap Icons
- Vanilla JavaScript
- File to Base64 conversion
- Drag & Drop upload

### 2. `/cekstatus.html` (Updated)

**Perubahan:**

- ✅ Tambah tombol "Lanjut ke Pembayaran"
- ✅ Tombol muncul jika status = DITERIMA
- ✅ Pass parameter nomor & nama via URL
- ✅ Green button with credit card icon

---

## ⚙️ KONFIGURASI PEMBAYARAN

Bisa diubah via tabel `konfigurasi_pembayaran`:

```sql
-- Ubah biaya pendaftaran
UPDATE konfigurasi_pembayaran
SET nilai = '750000'
WHERE nama_setting = 'biaya_pendaftaran';

-- Ubah nomor rekening
UPDATE konfigurasi_pembayaran
SET nilai = '1234-56-789012-3'
WHERE nama_setting = 'bank_nomor_rekening';

-- Nonaktifkan sistem pembayaran
UPDATE konfigurasi_pembayaran
SET nilai = 'false'
WHERE nama_setting = 'pembayaran_aktif';
```

---

## 🧪 TESTING CHECKLIST

### Manual Testing:

- [ ] 1. Daftar user baru → dapat nomor registrasi
- [ ] 2. Login admin → approve pendaftaran
- [ ] 3. Cek status → lihat tombol "Lanjut Pembayaran"
- [ ] 4. Klik tombol → redirect ke halaman pembayaran
- [ ] 5. Upload bukti → submit berhasil
- [ ] 6. Cek database → data masuk tabel pembayaran
- [ ] 7. Admin verifikasi → status jadi VERIFIED

### Database Testing:

```sql
-- Test 1: Generate nomor
SELECT generate_nomor_pembayaran();

-- Test 2: Insert pembayaran
INSERT INTO pembayaran (
  nomor_pembayaran, nomor_registrasi,
  nama_lengkap, jumlah
) VALUES (
  generate_nomor_pembayaran(),
  'REG-20251014-00001',
  'Test User',
  500000.00
);

-- Test 3: View report
SELECT * FROM v_pembayaran_report;

-- Test 4: Verify payment
UPDATE pembayaran
SET status_pembayaran = 'VERIFIED',
    verified_by = 'admin@test.com'
WHERE nomor_pembayaran = 'PAY-20251014-12345';
```

---

## 🔧 TROUBLESHOOTING

### Error: "Nomor registrasi tidak ditemukan"

**Solusi:** Pastikan user sudah mendaftar dan nomor registrasi benar

### Error: "Upload file gagal"

**Solusi:**

1. Cek storage bucket sudah dibuat (lihat SETUP_STORAGE.txt)
2. Pastikan file < 2MB
3. Format harus JPG/PNG/PDF

### Error: "Function generate_nomor_pembayaran() does not exist"

**Solusi:** Jalankan ulang sql_pembayaran.sql di Supabase

### Pembayaran tidak muncul di list

**Solusi:**

1. Cek API response: `/api/pembayaran_list`
2. Verifikasi data di database: `SELECT * FROM pembayaran;`
3. Cek view: `SELECT * FROM v_pembayaran_report;`

---

## 📝 TODO: Admin Dashboard Tab Pembayaran

**Next step yang perlu ditambahkan:**

1. **Tab Pembayaran di admin.html**

   - List semua pembayaran
   - Filter by status (Pending/Verified/Rejected)
   - Lihat detail + bukti pembayaran
   - Tombol Verifikasi/Tolak
   - Export CSV pembayaran

2. **Notifikasi**

   - Email notification saat status berubah
   - Badge count pending payments

3. **Dashboard Stats**
   - Total pembayaran hari ini
   - Total revenue
   - Pending count

---

## 📸 PREVIEW FITUR

### Halaman Pembayaran:

1. **Step Indicator**: Visual progress (Cek Status → Pembayaran → Selesai)
2. **Info Box**: Nomor registrasi dan nama pendaftar
3. **Alert Info**: Detail biaya dan syarat pembayaran
4. **Bank Card**: Detail rekening BRI dengan tombol copy
5. **Upload Area**: Drag & drop atau klik untuk upload
6. **Preview**: Tampil preview gambar bukti transfer
7. **Field Catatan**: Input catatan opsional
8. **Submit Button**: Kirim data ke API

### Flow:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Cek Status │────▶│  Pembayaran  │────▶│  Verifikasi │
│  (DITERIMA) │     │  (Upload)    │     │   (Admin)   │
└─────────────┘     └──────────────┘     └─────────────┘
      ▲                                          │
      │                                          │
      └──────────── Notifikasi ◀─────────────────┘
```

---

## 🎉 FITUR LENGKAP

✅ **Database Schema** - Tabel, triggers, functions, view
✅ **Payment Page** - Responsive design dengan step indicator
✅ **Bank Info** - BRI account dengan copy button
✅ **File Upload** - Drag & drop + validation
✅ **API Endpoints** - Submit, list, verify
✅ **Auto Generate** - Nomor pembayaran unique
✅ **Status Tracking** - PENDING/VERIFIED/REJECTED
✅ **Timestamps** - Auto create/update/verify dates
✅ **Reporting** - View untuk join data
✅ **Configuration** - Table untuk settings pembayaran
✅ **User Flow** - Dari cek status sampai upload bukti

---

## 🔗 Links Penting

- **Production**: https://project-python-m23c0ptxq-dewas-projects-d0163f17.vercel.app
- **Pembayaran**: https://project-python-m23c0ptxq-dewas-projects-d0163f17.vercel.app/pembayaran.html
- **Cek Status**: https://project-python-m23c0ptxq-dewas-projects-d0163f17.vercel.app/cekstatus.html
- **Admin**: https://project-python-m23c0ptxq-dewas-projects-d0163f17.vercel.app/admin.html

**File Documentation:**

- `sql_pembayaran.sql` - Database schema
- `SETUP_PEMBAYARAN.md` - Setup guide (file ini)
- `SETUP_STORAGE.txt` - Storage bucket setup

**API Files:**

- `api/pembayaran_submit.py` - Submit payment
- `api/pembayaran_list.py` - List payments
- `api/pembayaran_verify.py` - Verify payment

---

**Status:** ✅ READY TO USE (Tinggal jalankan SQL di Supabase!)
