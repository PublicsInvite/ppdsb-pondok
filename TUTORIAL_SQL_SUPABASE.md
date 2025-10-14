# 📚 TUTORIAL: Menjalankan SQL di Supabase Dashboard

## 🎯 Tujuan

Tutorial ini akan memandu Anda langkah demi langkah untuk menjalankan SQL migration sistem pembayaran di Supabase Dashboard.

---

## 📋 Persiapan

### Yang Anda Butuhkan:

1. ✅ Akun Supabase (sudah login)
2. ✅ Project Supabase yang sudah dibuat
3. ✅ File `sql_pembayaran.sql` (sudah ada di project)
4. ✅ Browser (Chrome/Firefox/Safari)

### Waktu yang Dibutuhkan:

⏱️ **5-10 menit**

---

## 🚀 LANGKAH-LANGKAH DETAIL

### **STEP 1: Buka Supabase Dashboard**

1. Buka browser Anda
2. Pergi ke: **https://supabase.com**
3. Klik tombol **"Sign In"** di pojok kanan atas
4. Login dengan akun Anda (email/password atau GitHub)

```
┌─────────────────────────────────────────┐
│  🌐 https://supabase.com                │
│                                         │
│  ┌──────────────────┐                  │
│  │   SUPABASE       │    [Sign In]     │
│  └──────────────────┘                  │
└─────────────────────────────────────────┘
```

---

### **STEP 2: Pilih Project Anda**

1. Setelah login, Anda akan melihat **Dashboard** dengan list project
2. Cari project yang Anda gunakan untuk aplikasi ini
3. Klik nama project tersebut untuk membukanya

**Contoh tampilan:**

```
┌───────────────────────────────────────────────┐
│  Your Projects                                │
│                                               │
│  ┌─────────────────────────────────────┐     │
│  │  📁 project-pondok-pesantren        │  ◀── Klik ini!
│  │  Created: 2 days ago                │     │
│  │  Region: Singapore                  │     │
│  └─────────────────────────────────────┘     │
│                                               │
└───────────────────────────────────────────────┘
```

**Tips:**

- Jika Anda lupa nama project, cek file `.env` atau `vercel.json`
- Biasanya URL Supabase ada di environment variables

---

### **STEP 3: Buka SQL Editor**

1. Setelah masuk ke project, lihat **sidebar kiri**
2. Scroll ke bawah sampai menemukan menu **"SQL Editor"**
3. Klik menu **"SQL Editor"**

**Lokasi menu:**

```
Sidebar Kiri:
┌──────────────────────┐
│ 🏠 Home              │
│ 🗄️  Table Editor     │
│ 🔐 Authentication    │
│ 📦 Storage           │
│ 📊 Database          │
│ ⚡ Edge Functions    │
│ 📝 SQL Editor        │  ◀── Klik ini!
│ 📈 Reports           │
│ ⚙️  Settings         │
└──────────────────────┘
```

---

### **STEP 4: Buat Query Baru**

1. Di halaman SQL Editor, klik tombol **"New query"**
2. Atau klik tombol **"+"** jika sudah ada query sebelumnya
3. Akan muncul editor kosong di sebelah kanan

**Tampilan SQL Editor:**

```
┌────────────────────────────────────────────────────────┐
│  SQL Editor                          [+ New query]     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Query 1  Query 2  [+ Untitled Query] ◀── Tab baru    │
│                                                        │
│  ┌──────────────────────────────────────────────┐     │
│  │  -- Write your SQL query here                │     │
│  │                                              │     │
│  │                                              │     │
│  │                                              │     │
│  └──────────────────────────────────────────────┘     │
│                                                        │
│  [▶ Run]  [Save]                                      │
└────────────────────────────────────────────────────────┘
```

---

### **STEP 5: Copy SQL dari File**

1. Buka file **`sql_pembayaran.sql`** di VS Code atau text editor
2. Tekan **Ctrl+A** (Windows/Linux) atau **Cmd+A** (Mac) untuk select all
3. Tekan **Ctrl+C** atau **Cmd+C** untuk copy
4. Atau klik kanan → Copy

**Isi file sql_pembayaran.sql:**

```sql
-- ============================================
-- SQL MIGRATION: SISTEM PEMBAYARAN PENDAFTARAN
-- ============================================
-- Tanggal: 14 Oktober 2025
-- Deskripsi: Menambahkan tabel pembayaran...

CREATE TABLE IF NOT EXISTS pembayaran (
    id SERIAL PRIMARY KEY,
    nomor_pembayaran VARCHAR(50) UNIQUE NOT NULL,
    ...
```

**PENTING:** Copy **SEMUA ISI FILE** dari baris pertama sampai terakhir!

---

### **STEP 6: Paste SQL ke Editor**

1. Kembali ke Supabase SQL Editor
2. Klik di dalam area editor (kotak putih besar)
3. Tekan **Ctrl+V** (Windows/Linux) atau **Cmd+V** (Mac) untuk paste
4. Pastikan semua SQL ter-paste dengan benar

**Setelah paste:**

```
┌────────────────────────────────────────────────────────┐
│  Untitled Query                      [Rename] [Delete] │
├────────────────────────────────────────────────────────┤
│  1  -- ========================================         │
│  2  -- SQL MIGRATION: SISTEM PEMBAYARAN                │
│  3  -- ========================================         │
│  4  -- Tanggal: 14 Oktober 2025                        │
│  5                                                     │
│  6  CREATE TABLE IF NOT EXISTS pembayaran (            │
│  7      id SERIAL PRIMARY KEY,                         │
│  8      nomor_pembayaran VARCHAR(50) UNIQUE NOT NULL,  │
│  9      ...                                            │
│     [Scroll untuk lihat lebih]                         │
│                                                        │
│  [▶ Run]  [Save]                                      │
└────────────────────────────────────────────────────────┘
```

**Checklist Sebelum Run:**

- ☐ Semua kode SQL sudah ter-paste
- ☐ Scroll ke bawah untuk cek tidak ada yang terpotong
- ☐ Tidak ada error syntax (garis merah di editor)

---

### **STEP 7: Jalankan SQL**

1. Klik tombol **"Run"** (tombol hijau dengan icon play ▶)
2. Atau tekan **Ctrl+Enter** (Windows/Linux) atau **Cmd+Enter** (Mac)
3. Tunggu proses eksekusi (biasanya 5-10 detik)

**Proses Running:**

```
┌────────────────────────────────────────────────────────┐
│  [▶ Run]  [Save]                                      │
│                                                        │
│  ⏳ Running query...                                   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

### **STEP 8: Verifikasi Hasil**

#### **✅ Jika SUKSES:**

Anda akan melihat pesan seperti ini di bagian bawah:

```
┌────────────────────────────────────────────────────────┐
│  Results                                               │
├────────────────────────────────────────────────────────┤
│  ✅ Success. No rows returned                          │
│  Rows: 0                                               │
│  Time: 1.23s                                           │
└────────────────────────────────────────────────────────┘
```

**Pesan sukses bisa berupa:**

- ✅ "Success. No rows returned"
- ✅ "CREATE TABLE"
- ✅ "CREATE INDEX"
- ✅ "CREATE FUNCTION"
- ✅ "CREATE TRIGGER"
- ✅ "INSERT 6" (untuk konfigurasi_pembayaran)

#### **❌ Jika ADA ERROR:**

Anda akan melihat pesan error seperti:

```
┌────────────────────────────────────────────────────────┐
│  Results                                               │
├────────────────────────────────────────────────────────┤
│  ❌ Error: relation "pembayaran" already exists        │
│  Line: 9                                               │
└────────────────────────────────────────────────────────┘
```

**Solusi untuk error umum:**

| Error                     | Penyebab                      | Solusi                                     |
| ------------------------- | ----------------------------- | ------------------------------------------ |
| "relation already exists" | Tabel sudah dibuat sebelumnya | ✅ SKIP - Sudah OK!                        |
| "function already exists" | Function sudah ada            | ✅ Ganti `CREATE` jadi `CREATE OR REPLACE` |
| "syntax error"            | Ada typo di SQL               | ❌ Cek kembali SQL yang di-paste           |
| "permission denied"       | User tidak punya akses        | ❌ Login sebagai owner project             |

---

### **STEP 9: Cek Tabel di Database**

Untuk memastikan tabel berhasil dibuat:

1. Klik menu **"Table Editor"** di sidebar kiri
2. Atau klik **"Database"** → **"Tables"**
3. Cari tabel baru yang dibuat:
   - ✅ `pembayaran`
   - ✅ `konfigurasi_pembayaran`

**Tampilan Table Editor:**

```
┌────────────────────────────────────────────────────────┐
│  Tables                                   [+ New table] │
├────────────────────────────────────────────────────────┤
│  📋 pendaftar                    ✅ (existing)          │
│  💳 pembayaran                   ✅ (NEW!)              │
│  ⚙️  konfigurasi_pembayaran      ✅ (NEW!)              │
└────────────────────────────────────────────────────────┘
```

---

### **STEP 10: Test dengan Query**

Untuk test apakah setup berhasil, jalankan query test:

1. Buka SQL Editor lagi
2. Buat **New query**
3. Copy-paste query test berikut:

```sql
-- Test 1: Cek tabel pembayaran
SELECT * FROM pembayaran LIMIT 5;

-- Test 2: Cek view
SELECT * FROM v_pembayaran_report LIMIT 5;

-- Test 3: Test function generate nomor
SELECT generate_nomor_pembayaran();

-- Test 4: Cek konfigurasi
SELECT * FROM konfigurasi_pembayaran;
```

4. Klik **Run**
5. Lihat hasil di bagian **Results**

**Hasil yang diharapkan:**

**Test 1 & 2:** (Kosong karena belum ada data)

```
┌─────────────────────────────────────┐
│  Results: 0 rows                    │
│  (Empty table - This is normal!)    │
└─────────────────────────────────────┘
```

**Test 3:** (Generate nomor pembayaran)

```
┌─────────────────────────────────────┐
│  generate_nomor_pembayaran          │
├─────────────────────────────────────┤
│  PAY-20251014-12345                 │
└─────────────────────────────────────┘
```

**Test 4:** (Konfigurasi pembayaran)

```
┌─────────────────────────────────────────────────────────┐
│  nama_setting          │  nilai                         │
├────────────────────────┼────────────────────────────────┤
│  biaya_pendaftaran     │  500000                        │
│  bank_nama             │  BRI (Bank Rakyat Indonesia)   │
│  bank_nomor_rekening   │  0012-01-123456-78-9           │
│  bank_atas_nama        │  Yayasan Pondok Pesantren      │
│  bank_cabang           │  Cabang Utama                  │
│  pembayaran_aktif      │  true                          │
└────────────────────────┴────────────────────────────────┘
```

---

## ✅ CHECKLIST FINAL

Pastikan semua ini sudah OK:

- [ ] **Login ke Supabase** - Berhasil masuk dashboard
- [ ] **Pilih project** - Project yang benar sudah dipilih
- [ ] **Buka SQL Editor** - Menu SQL Editor terbuka
- [ ] **Paste SQL** - Semua isi `sql_pembayaran.sql` ter-paste
- [ ] **Run query** - Klik Run dan tidak ada error
- [ ] **Tabel pembayaran** - Terlihat di Table Editor
- [ ] **Tabel konfigurasi** - Terlihat di Table Editor
- [ ] **Test query** - Semua test query berhasil
- [ ] **Function generate** - Generate nomor pembayaran work
- [ ] **View report** - View v_pembayaran_report ada

---

## 🎉 SELESAI!

Jika semua checklist di atas ✅, maka setup database **BERHASIL!**

### Yang Sudah Dibuat:

1. ✅ Tabel `pembayaran` dengan 16 kolom
2. ✅ Tabel `konfigurasi_pembayaran` dengan 6 data default
3. ✅ 3 Index untuk performa (nomor_registrasi, status, tanggal)
4. ✅ 2 Triggers (auto timestamp & verified timestamp)
5. ✅ 3 Functions (update timestamp, set verified, generate nomor)
6. ✅ 1 View `v_pembayaran_report` untuk reporting

### Next Steps:

1. ✅ Test aplikasi: https://project-python-m23c0ptxq-dewas-projects-d0163f17.vercel.app
2. ✅ Daftar user baru
3. ✅ Admin approve pendaftaran
4. ✅ User cek status → klik "Lanjut Pembayaran"
5. ✅ Upload bukti pembayaran
6. ✅ Cek data di tabel pembayaran

---

## 🆘 TROUBLESHOOTING

### Problem: "Tidak bisa login ke Supabase"

**Solusi:**

1. Reset password via "Forgot Password"
2. Atau daftar akun baru (free tier)
3. Cek email untuk verifikasi

### Problem: "Project tidak muncul"

**Solusi:**

1. Pastikan login dengan akun yang benar
2. Cek organization (klik dropdown organization di atas)
3. Mungkin project di organization lain

### Problem: "SQL Editor tidak ada"

**Solusi:**

1. Scroll sidebar ke bawah
2. Atau gunakan search: tekan `Ctrl+K` dan ketik "SQL"
3. Update browser ke versi terbaru

### Problem: "Run button tidak bisa diklik"

**Solusi:**

1. Pastikan ada SQL di editor (tidak kosong)
2. Refresh halaman browser
3. Clear cache browser

### Problem: "Error: permission denied"

**Solusi:**

1. Pastikan Anda owner/admin project
2. Cek Settings → Database → Connection pooling
3. Contact team member yang punya akses

### Problem: "Tabel tidak muncul di Table Editor"

**Solusi:**

1. Refresh halaman browser (F5 atau Cmd+R)
2. Klik ikon refresh di Table Editor
3. Tunggu 10-20 detik, database sedang sync

---

## 📞 Butuh Bantuan?

### Official Resources:

- 📖 Supabase Docs: https://supabase.com/docs
- 💬 Discord Community: https://discord.supabase.com
- 🐛 GitHub Issues: https://github.com/supabase/supabase/issues

### Video Tutorial (Alternative):

- YouTube: Search "Supabase SQL Editor tutorial"
- Channel resmi: Supabase Official Channel

---

## 💡 TIPS PRO

1. **Save query Anda**: Klik "Save" untuk menyimpan query yang sudah run
2. **Rename query**: Klik "Rename" untuk memberi nama yang jelas (misalnya: "Setup Pembayaran")
3. **Favorite query**: Star query yang sering dipakai
4. **History**: Supabase menyimpan history query, bisa diakses via dropdown
5. **Keyboard shortcuts**:
   - `Ctrl/Cmd + Enter` = Run query
   - `Ctrl/Cmd + S` = Save query
   - `Ctrl/Cmd + K` = Search menu

---

**Status:** ✅ Tutorial Lengkap - Siap Digunakan!
**Dibuat:** 14 Oktober 2025
**Update terakhir:** 14 Oktober 2025
