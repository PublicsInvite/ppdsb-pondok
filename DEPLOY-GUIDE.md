# 🚀 PANDUAN DEPLOY KE VERCEL

## ✅ Git Repository Sudah Siap!

Repository Git sudah di-initialize dengan commit pertama.

---

## 📋 Langkah Deploy ke Vercel:

### 1️⃣ Install Vercel CLI (jika belum)

```bash
npm install -g vercel
```

### 2️⃣ Login ke Vercel

```bash
vercel login
```

Pilih metode login (GitHub, GitLab, Email, dll)

### 3️⃣ Deploy Project

```bash
cd "/Users/dewasatriaaa/Downloads/KULIAH/PROJECT CODE/project python"
vercel
```

Jawab pertanyaan berikut:

- **Set up and deploy?** → `Y` (Yes)
- **Which scope?** → Pilih account Anda
- **Link to existing project?** → `N` (No)
- **What's your project's name?** → `pondok-pesantren` (atau nama lain)
- **In which directory is your code located?** → `./` (tekan Enter)
- **Override settings?** → `N` (No)

### 4️⃣ Set Environment Variables

Setelah deployment selesai, set environment variables:

```bash
# Set SUPABASE_URL
vercel env add SUPABASE_URL

# Saat diminta, paste:
https://pislnvhdmsxudltcuuku.supabase.co

# Pilih environment: Production, Preview, Development (pilih semua dengan spasi)
```

```bash
# Set SUPABASE_ANON_KEY
vercel env add SUPABASE_ANON_KEY

# Saat diminta, paste ANON_KEY dari .env Anda
```

```bash
# Set SUPABASE_SERVICE_ROLE_KEY
vercel env add SUPABASE_SERVICE_ROLE_KEY

# Saat diminta, paste SERVICE_ROLE_KEY dari .env Anda
```

### 5️⃣ Redeploy dengan Environment Variables

```bash
vercel --prod
```

---

## 🎯 Alternatif: Deploy via Vercel Dashboard

### Opsi A: Import dari Git Repository

1. **Buka**: https://vercel.com/new
2. **Klik**: "Import Git Repository"
3. **Connect** dengan GitHub/GitLab/Bitbucket
4. **Push** repository Anda ke Git hosting
5. **Import** project dari Vercel dashboard
6. **Add Environment Variables** di settings
7. **Deploy**

### Opsi B: Deploy Langsung (Tanpa Git Remote)

Cukup jalankan `vercel --prod` dari terminal, dan Vercel akan handle semuanya!

---

## 📝 Environment Variables yang Perlu Di-Set:

| Variable                    | Value                                      |
| --------------------------- | ------------------------------------------ |
| `SUPABASE_URL`              | `https://pislnvhdmsxudltcuuku.supabase.co` |
| `SUPABASE_ANON_KEY`         | Dari file `.env` Anda                      |
| `SUPABASE_SERVICE_ROLE_KEY` | Dari file `.env` Anda                      |

---

## ✅ Verifikasi Deployment:

Setelah deploy berhasil, Anda akan mendapat URL seperti:

```
https://pondok-pesantren-xxx.vercel.app
```

### Test URL berikut:

1. **Landing Page**: `https://your-project.vercel.app/`
2. **Form Daftar**: `https://your-project.vercel.app/daftar`
3. **Admin Dashboard**: `https://your-project.vercel.app/admin`
4. **API Create**: `https://your-project.vercel.app/api/pendaftar_create`
5. **API List**: `https://your-project.vercel.app/api/pendaftar_list`

---

## 🔧 Troubleshooting:

### Error: "Missing environment variables"

- Set environment variables dengan `vercel env add`
- Atau tambahkan di Vercel Dashboard → Settings → Environment Variables

### Error: "Build failed"

- Cek `requirements.txt` sudah benar
- Cek Python version di `vercel.json`

### API Error 500

- Cek environment variables sudah di-set
- Cek Supabase credentials benar
- Lihat logs: `vercel logs`

---

## 📊 Commands Reference:

```bash
# Deploy preview
vercel

# Deploy production
vercel --prod

# View logs
vercel logs

# List deployments
vercel ls

# View environment variables
vercel env ls

# Remove deployment
vercel rm [deployment-url]
```

---

## 🎉 Setelah Deploy Berhasil:

1. ✅ Share URL ke user/stakeholder
2. ✅ Test semua fitur (daftar, list, update status)
3. ✅ Monitor logs untuk debugging
4. ✅ Setup custom domain (opsional)

---

## 💡 Tips:

- **Automatic Deployment**: Connect dengan GitHub untuk auto-deploy setiap push
- **Preview Deployments**: Setiap branch/PR akan dapat preview URL
- **Rollback**: Bisa rollback ke deployment sebelumnya via dashboard
- **Custom Domain**: Tambahkan domain custom di Settings → Domains

---

## 🆘 Need Help?

Run: `vercel --help`

Atau buka: https://vercel.com/docs
