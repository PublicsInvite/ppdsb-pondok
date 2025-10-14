# 🚀 Deployment Guide - Pondok Pesantren Project

## ⚠️ PENTING: Struktur Folder

Vercel akan **PRIORITASKAN** folder `public/` jika ada. Jadi pastikan file di folder `public/` selalu ter-update!

### Struktur Folder:
```
project python/
├── public/              ← VERCEL DEPLOY DARI SINI!
│   ├── admin.html       ← File yang benar-benar di-deploy
│   ├── index.html       ← File yang benar-benar di-deploy
│   ├── daftar.html
│   ├── login.html
│   └── cekstatus.html
│
├── admin.html           ← File development (root)
├── index.html           ← File development (root)
└── vercel.json          ← Config routing
```

## 📝 Workflow Deployment

### 1. Edit File (di ROOT folder)
```bash
# Edit file di root folder seperti biasa
nano admin.html
nano index.html
```

### 2. Copy ke Folder Public
```bash
# WAJIB copy file terbaru ke public/
cp admin.html public/admin.html
cp index.html public/index.html
cp daftar.html public/daftar.html
cp login.html public/login.html
cp cekstatus.html public/cekstatus.html
```

### 3. Commit & Deploy
```bash
# Add semua perubahan
git add -A

# Commit
git commit -m "update: your message here"

# Deploy ke production
vercel --prod
```

## 🔧 Script Helper (RECOMMENDED)

Buat script untuk otomatis sync file:

### sync-to-public.sh
```bash
#!/bin/bash
echo "Syncing files to public folder..."
cp admin.html public/admin.html
cp index.html public/index.html
cp daftar.html public/daftar.html
cp login.html public/login.html
cp cekstatus.html public/cekstatus.html
echo "✅ Files synced successfully!"
```

Cara pakai:
```bash
chmod +x sync-to-public.sh
./sync-to-public.sh
```

## 🚨 Troubleshooting

### Problem: File tidak terupdate di Vercel
**Solusi:**
1. Pastikan file sudah di-copy ke `public/` folder
2. Check ukuran file: `ls -lh public/admin.html`
3. Compare dengan file root: `ls -lh admin.html`
4. Jika beda, copy ulang: `cp admin.html public/admin.html`

### Problem: Deployment lama/cache
**Solusi:**
```bash
# Clear cache Vercel lokal
rm -rf .vercel

# Deploy dengan force
vercel --prod --force
```

### Problem: File masih tidak update
**Solusi:**
```bash
# 1. Pastikan sudah commit
git status
git add public/
git commit -m "update public files"

# 2. Deploy
vercel --prod

# 3. Verifikasi
curl -s https://your-url.vercel.app/admin | wc -c
```

## ✅ Checklist Deploy

- [ ] Edit file di root folder
- [ ] Copy file ke `public/` folder
- [ ] `git add -A`
- [ ] `git commit -m "message"`
- [ ] `vercel --prod`
- [ ] Test di browser / curl untuk verifikasi

## 📊 Verifikasi Deployment

### Cek ukuran file yang ter-deploy:
```bash
# File lokal
wc -c public/admin.html

# File production
curl -s https://your-url.vercel.app/admin | wc -c

# Harus sama!
```

### Cek fitur spesifik:
```bash
# Cek modal verifikasi
curl -s https://your-url.vercel.app/admin | grep -c "verifikasiModal"

# Cek status Revisi
curl -s https://your-url.vercel.app/admin | grep -o "Revisi" | head -3
```

## 🔗 Production URL

**Latest**: https://project-python-osz06qsv4-dewas-projects-d0163f17.vercel.app/

### Pages:
- Homepage: `/`
- Pendaftaran: `/daftar`
- Cek Status: `/cek-status`
- Login Admin: `/login`
- Dashboard Admin: `/admin`

## 📌 Notes

1. **SELALU** copy file ke `public/` sebelum deploy
2. Vercel prioritaskan `public/` folder jika ada
3. File di root hanya untuk development/backup
4. Git commit both (root & public) untuk consistency
