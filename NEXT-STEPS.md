# 🚀 LANGKAH SELANJUTNYA

## ✅ Database Sudah Siap!

Tabel `pendaftar` sudah berhasil dibuat di Supabase dengan struktur lengkap.

---

## 📋 Langkah-langkah Deployment:

### 1️⃣ Install Vercel CLI (jika belum)

```bash
npm install -g vercel
```

### 2️⃣ Login ke Vercel

```bash
vercel login
```

### 3️⃣ Deploy Project

Dari direktori project, jalankan:

```bash
cd "/Users/dewasatriaaa/Downloads/KULIAH/PROJECT CODE/project python"
vercel
```

Ikuti instruksi:

- **Set up and deploy?** → Yes
- **Which scope?** → Pilih account Anda
- **Link to existing project?** → No
- **What's your project's name?** → pondok-pesantren (atau nama lain)
- **In which directory is your code located?** → ./
- **Override settings?** → No

### 4️⃣ Set Environment Variables di Vercel

Setelah deploy, set environment variables:

```bash
vercel env add SUPABASE_URL production
# Paste: https://pislnvhdmsxudltcuuku.supabase.co

vercel env add SUPABASE_ANON_KEY production
# Paste: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

vercel env add SUPABASE_SERVICE_ROLE_KEY production
# Paste: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 5️⃣ Deploy Production

```bash
vercel --prod
```

---

## 🧪 Atau Test Lokal Dulu:

### Opsi A: Vercel Dev (Recommended)

```bash
vercel dev
```

Lalu buka: http://localhost:3000

### Opsi B: Python HTTP Server (Simple)

```bash
# Serve static files
python3 -m http.server 8000
```

Lalu buka: http://localhost:8000

⚠️ **Catatan:** API endpoints tidak akan berfungsi dengan Python HTTP server biasa. Gunakan `vercel dev` untuk test API.

---

## 🎨 Test Frontend:

### 1. Test Landing Page

- Buka: `index.html`
- Cek apakah tampilan hijau sudah muncul
- Cek animasi AOS dan GSAP

### 2. Test Form Pendaftaran

- Buka: `daftar.html`
- Isi semua field form
- Submit dan lihat apakah muncul nomor registrasi

### 3. Test Admin Dashboard

- Buka: `admin.html`
- Cek apakah list pendaftar muncul
- Test filter dan search
- Test update status

---

## 🔧 Troubleshooting:

### API tidak berfungsi?

1. Pastikan menggunakan `vercel dev` (bukan Python HTTP server)
2. Cek file `.env` sudah benar
3. Cek kredensial Supabase

### CORS Error?

- Sudah ditangani di `vercel.json` dengan headers

### Data tidak muncul?

1. Buka Supabase Dashboard
2. Masuk ke Table Editor
3. Cek apakah ada data di tabel `pendaftar`

---

## 📱 URL Production Nanti:

Setelah deploy, Anda akan mendapat URL seperti:

- Production: `https://pondok-pesantren-xxx.vercel.app`
- Landing: `https://pondok-pesantren-xxx.vercel.app/index.html`
- Form: `https://pondok-pesantren-xxx.vercel.app/daftar.html`
- Admin: `https://pondok-pesantren-xxx.vercel.app/admin.html`

---

## 🎯 Checklist:

- [x] ✅ Database schema imported
- [x] ✅ Tabel pendaftar created
- [x] ✅ Environment variables configured
- [x] ✅ Frontend files ready (index, daftar, admin)
- [x] ✅ API endpoints ready (create, list, status)
- [ ] ⏳ Deploy to Vercel
- [ ] ⏳ Test live endpoints
- [ ] ⏳ Share production URL

---

## 💡 Tips:

1. **Untuk Development:** Gunakan `vercel dev`
2. **Untuk Production:** Gunakan `vercel --prod`
3. **Update Code:** Deploy ulang dengan `vercel --prod`
4. **Rollback:** Gunakan Vercel Dashboard

---

## 🆘 Butuh Bantuan?

Jalankan command ini untuk melihat info:

```bash
vercel --help
```

Atau screenshot error dan kirim ke sini! 😊
