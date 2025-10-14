# Sistem Pendaftaran Pondok Pesantren

Web application untuk pendaftaran santri baru dengan sistem pembayaran online.

## 🚀 Fitur

- ✅ Pendaftaran Santri Online
- ✅ Upload Dokumen (KTP, KK, Foto, dll)
- ✅ Cek Status Pendaftaran
- ✅ Sistem Pembayaran dengan Upload Bukti
- ✅ Dashboard Admin untuk Verifikasi
- ✅ Export Data ke CSV
- ✅ Responsive Design

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, Bootstrap 5
- **Backend**: Python (Vercel Serverless)
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage
- **Deployment**: Vercel

## 📁 Struktur Folder

```
project python/
├── api/              # API endpoints (Python)
├── public/           # Frontend files (HTML)
├── sql/              # Database schema & migrations
└── assets/           # Static assets (CSS, images)
```

## 🔧 Setup Database

Jalankan file SQL di folder `sql/` sesuai urutan:

1. `supabase-schema.sql` - Schema awal
2. `sql_alter_pendaftar.sql` - Alter table pendaftar
3. `sql_pembayaran_simple.sql` - Tabel pembayaran
4. `supabase_storage_setup.sql` - Setup storage

## 🌐 Deployment

Deploy otomatis via Vercel setiap push ke repository.

## 📝 Environment Variables

Perlu setup di Vercel:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`

---

**Developed with ❤️ for Pondok Pesantren**
# ppdsb-pondok
