# Pondok Pesantren - Sistema Pendaftaran

Aplikasi web untuk sistem pendaftaran pondok pesantren dengan backend Python serverless di Vercel dan database Supabase.

## 🚀 Fitur

- **Landing Page**: Halaman utama dengan animasi Bootstrap dan AOS
- **Form Pendaftaran**: Formulir pendaftaran santri baru dengan data lengkap
  - Data pribadi calon santri (NIK, NISN, tempat/tanggal lahir)
  - Alamat lengkap
  - Data orang tua (ayah & ibu)
  - Rencana pendidikan
  - Auto-generate nomor registrasi
- **Dashboard Admin**: Panel admin untuk mengelola pendaftar
  - View semua pendaftar dengan detail lengkap
  - Filter dan search berdasarkan nama
  - Update status (MENUNGGU_VERIFIKASI / DITERIMA / DITOLAK)
  - Pagination

## 📁 Struktur Proyek

```
pondok-python-vercel/
├─ index.html              # Landing page
├─ daftar.html            # Form pendaftaran
├─ admin.html             # Dashboard admin
├─ assets/
│  ├─ css/styles.css      # Custom styles
│  └─ js/app.js          # Helper functions & animations
├─ api/                   # Vercel Python Serverless Functions
│  ├─ _supabase.py       # Supabase client helper
│  ├─ pendaftar_create.py # POST: Create pendaftar (comprehensive)
│  ├─ pendaftar_list.py   # GET: List/search/paginate
│  └─ pendaftar_status.py # PATCH: Update status via RPC
├─ supabase-schema.sql    # Complete database schema
├─ API-DOCUMENTATION.md   # Detailed API docs
├─ requirements.txt
├─ vercel.json
├─ .env.example
└─ README.md
```

## 🛠️ Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd pondok-python-vercel
```

### 2. Setup Supabase

1. Buat project baru di [Supabase](https://supabase.com)
2. Jalankan SQL schema dari file `supabase-schema.sql`:

   - Buka SQL Editor di Supabase Dashboard
   - Copy paste isi file `supabase-schema.sql`
   - Execute script

   **Schema ini mencakup:**

   - Tabel `pendaftar` dengan field lengkap (NIK, KK, NISN, dll)
   - Auto-generate `nomorRegistrasi` (format: REG-YYYYMMDD-000001)
   - Trigger untuk auto-update `updatedAt`
   - RPC function `pendaftar_set_status` untuk update status
   - Row Level Security (RLS) policies
   - Indexes untuk performa optimal

3. Dapatkan credentials dari Settings → API:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`

### 3. Setup Environment Variables

**Lokal (untuk testing):**

```bash
cp .env.example .env
# Edit .env dan isi dengan credentials Supabase Anda
```

**Di Vercel:**

1. Go to Project Settings → Environment Variables
2. Tambahkan:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`

### 4. Deploy ke Vercel

#### Via Vercel CLI:

```bash
npm i -g vercel
vercel login
vercel
```

#### Via GitHub:

1. Push ke GitHub
2. Import project di [vercel.com](https://vercel.com)
3. Tambahkan environment variables
4. Deploy!

## 📚 API Endpoints

### 1. Create Pendaftar (Public)

```
POST /api/pendaftar_create
Content-Type: application/json

Body:
{
  "nikCalon": "3201234567890123",
  "kkNo": "3201234567890001",
  "nisn": "0012345678",
  "namaLengkap": "Ahmad Fauzi",
  "tempatLahir": "Jakarta",
  "tanggalLahir": "2008-05-15",
  "jenisKelamin": "L",
  "alamatJalan": "Jl. Raya Pondok No. 123",
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
}

Response:
{
  "ok": true,
  "id": 1,
  "nomorRegistrasi": "REG-20251014-000001"
}
```

### 2. List Pendaftar (Admin)

```
GET /api/pendaftar_list?page=1&pageSize=10&q=ahmad&status=MENUNGGU_VERIFIKASI

Response:
{
  "ok": true,
  "rows": [ ... ],
  "page": 1,
  "pageSize": 10
}
```

### 3. Update Status (Admin)

```
PATCH /api/pendaftar_status
Content-Type: application/json

Body:
{
  "id": 1,
  "status": "DITERIMA",  // atau "DITOLAK" / "MENUNGGU_VERIFIKASI"
  "alasan": "Memenuhi semua persyaratan"
}

Response:
{
  "ok": true
}
```

**📖 Lihat [API-DOCUMENTATION.md](./API-DOCUMENTATION.md) untuk dokumentasi lengkap**

## � Database Schema

### Tabel: pendaftar

| Field                | Type        | Description                           |
| -------------------- | ----------- | ------------------------------------- |
| id                   | BIGSERIAL   | Primary key                           |
| nomorRegistrasi      | TEXT        | Auto-generated (REG-YYYYMMDD-000001)  |
| nikCalon             | TEXT        | NIK calon santri                      |
| kkNo                 | TEXT        | Nomor Kartu Keluarga                  |
| nisn                 | TEXT        | NISN (optional)                       |
| namaLengkap          | TEXT        | Nama lengkap                          |
| tempatLahir          | TEXT        | Tempat lahir                          |
| tanggalLahir         | DATE        | Tanggal lahir                         |
| jenisKelamin         | CHAR(1)     | L/P                                   |
| alamatJalan          | TEXT        | Alamat jalan                          |
| desa                 | TEXT        | Desa                                  |
| kecamatan            | TEXT        | Kecamatan                             |
| kotaKabupaten        | TEXT        | Kota/Kabupaten                        |
| provinsi             | TEXT        | Provinsi                              |
| ijazahFormalTerakhir | TEXT        | Ijazah terakhir                       |
| rencanaDomisili      | TEXT        | Rencana domisili                      |
| rencanaTingkat       | TEXT        | Rencana tingkat                       |
| rencanaKelas         | TEXT        | Rencana kelas                         |
| namaAyah             | TEXT        | Nama ayah                             |
| nikAyah              | TEXT        | NIK ayah                              |
| namaIbu              | TEXT        | Nama ibu                              |
| nikIbu               | TEXT        | NIK ibu                               |
| statusBerkas         | TEXT        | Status (default: MENUNGGU_VERIFIKASI) |
| deskripsiStatus      | TEXT        | Deskripsi status                      |
| createdAt            | TIMESTAMPTZ | Waktu dibuat                          |
| updatedAt            | TIMESTAMPTZ | Waktu update                          |

### RPC Functions

- `pendaftar_set_status(p_id, p_status, p_deskripsi)` - Update status dengan validasi

## �🔒 Security Notes

- ⚠️ **JANGAN** commit file `.env` ke git
- ⚠️ **JANGAN** expose `SUPABASE_SERVICE_ROLE_KEY` ke browser
- ✅ `ANON_KEY` untuk operasi public (create pendaftar)
- ✅ `SERVICE_ROLE_KEY` hanya di server-side (admin operations)
- ✅ Row Level Security (RLS) enabled untuk keamanan data
- ✅ Field validation di level API dan database

## 🎨 Teknologi

**Frontend:**

- HTML5
- Bootstrap 5
- AOS (Animate On Scroll)
- Vanilla JavaScript

**Backend:**

- Python 3.11
- Vercel Serverless Functions
- Supabase (PostgreSQL)

**Deployment:**

- Vercel

## 📝 Development

### Local Development

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run local server:

```bash
vercel dev
```

3. Open http://localhost:3000

## 🐛 Troubleshooting

### Error: Module not found

- Pastikan `requirements.txt` sudah di-deploy
- Vercel otomatis install packages saat deploy

### Error: Environment variable not found

- Cek di Vercel Project Settings → Environment Variables
- Redeploy setelah menambahkan env vars

### CORS Error

- API sudah include CORS headers
- Check browser console untuk detail error

## 📄 License

MIT License

## 👤 Author

Dewa Satria

---

**Happy Coding! 🚀**
