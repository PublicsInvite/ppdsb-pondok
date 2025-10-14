# Quick Start Guide - Pondok Pesantren Registration System

## 🚀 Setup in 5 Minutes

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "New Project"
3. Fill in project details and wait for setup to complete

### Step 2: Setup Database

1. Open SQL Editor in Supabase Dashboard
2. Copy entire content from `supabase-schema.sql`
3. Paste and click "RUN"
4. Verify tables created successfully

### Step 3: Get Credentials

1. Go to Project Settings → API
2. Copy these values:
   - `Project URL` → SUPABASE_URL
   - `anon public` → SUPABASE_ANON_KEY
   - `service_role` → SUPABASE_SERVICE_ROLE_KEY (⚠️ Keep secret!)

### Step 4: Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy (from project root)
vercel

# Follow prompts and add environment variables when asked:
# - SUPABASE_URL
# - SUPABASE_ANON_KEY
# - SUPABASE_SERVICE_ROLE_KEY
```

### Step 5: Test Your API

```bash
# Test registration endpoint
curl -X POST https://your-app.vercel.app/api/pendaftar_create \
  -H "Content-Type: application/json" \
  -d '{
    "nikCalon": "3201234567890123",
    "kkNo": "3201234567890001",
    "namaLengkap": "Test User",
    "tempatLahir": "Jakarta",
    "tanggalLahir": "2008-05-15",
    "jenisKelamin": "L",
    "alamatJalan": "Jl. Test No. 1",
    "desa": "Test Desa",
    "kecamatan": "Test Kecamatan",
    "kotaKabupaten": "Jakarta",
    "provinsi": "DKI Jakarta",
    "ijazahFormalTerakhir": "SMP",
    "rencanaDomisili": "Mukim",
    "rencanaTingkat": "MTs",
    "rencanaKelas": "Kelas 1",
    "namaAyah": "Ayah Test",
    "nikAyah": "3201234567890100",
    "namaIbu": "Ibu Test",
    "nikIbu": "3201234567890101"
  }'
```

Expected response:

```json
{
  "ok": true,
  "id": 1,
  "nomorRegistrasi": "REG-20251014-000001"
}
```

---

## 📱 Testing the Frontend

### 1. Landing Page

Visit: `https://your-app.vercel.app/`

### 2. Registration Form

Visit: `https://your-app.vercel.app/daftar`

- Fill out the form
- Submit
- Check Supabase dashboard for new record

### 3. Admin Dashboard

Visit: `https://your-app.vercel.app/admin`

- View all registrations
- Filter by status
- Search by name
- Update status (Accept/Reject)

---

## 🔧 Local Development

### Setup

```bash
# 1. Create .env file
cp .env.example .env

# 2. Edit .env with your Supabase credentials
nano .env

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Run local development server
vercel dev

# 5. Open browser
open http://localhost:3000
```

---

## 📊 Database Schema Reference

### Main Table: pendaftar

**Required Fields:**

- nikCalon (NIK 16 digit)
- kkNo (Nomor KK)
- namaLengkap
- tempatLahir
- tanggalLahir (YYYY-MM-DD)
- jenisKelamin (L/P)
- alamatJalan, desa, kecamatan, kotaKabupaten, provinsi
- ijazahFormalTerakhir
- rencanaDomisili, rencanaTingkat, rencanaKelas
- namaAyah, nikAyah
- namaIbu, nikIbu

**Optional Fields:**

- nisn (can be null)

**Auto-Generated:**

- id (BIGSERIAL)
- nomorRegistrasi (REG-YYYYMMDD-000001)
- statusBerkas (default: MENUNGGU_VERIFIKASI)
- createdAt, updatedAt

---

## 🎯 API Endpoints Quick Reference

### Public Endpoint

- `POST /api/pendaftar_create` - Create new registration

### Admin Endpoints (Requires SERVICE_ROLE_KEY)

- `GET /api/pendaftar_list` - List registrations
- `PATCH /api/pendaftar_status` - Update status

**Status Values:**

- `MENUNGGU_VERIFIKASI` (default)
- `DITERIMA` (accepted)
- `DITOLAK` (rejected)

---

## 🐛 Troubleshooting

### Error: "Import supabase could not be resolved"

- **Solution**: This is expected locally. Vercel will install dependencies from `requirements.txt` during deployment.

### Error: "SUPABASE_URL not found"

- **Solution**: Add environment variables in Vercel dashboard (Settings → Environment Variables)
- Redeploy after adding env vars

### Database Error: "relation pendaftar does not exist"

- **Solution**: Run the complete SQL schema from `supabase-schema.sql`

### CORS Error in Browser

- **Solution**: APIs already include CORS headers. Check browser console for actual error details.

### RPC Function Error: "function pendaftar_set_status does not exist"

- **Solution**: Make sure you ran the complete SQL schema including the RPC function definition

---

## 📝 Environment Variables Checklist

### Supabase Dashboard (Settings → API)

- [ ] SUPABASE_URL
- [ ] SUPABASE_ANON_KEY (for public operations)
- [ ] SUPABASE_SERVICE_ROLE_KEY (for admin operations)

### Vercel Dashboard (Project Settings → Environment Variables)

Add all three variables above to:

- [ ] Production
- [ ] Preview (optional)
- [ ] Development (optional)

### Local .env File

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJI...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJI...
```

---

## 🎉 You're Done!

Your Pondok Pesantren Registration System is now live!

### Next Steps:

1. Customize HTML pages (index.html, daftar.html, admin.html)
2. Update branding and colors in assets/css/styles.css
3. Add email notifications (optional)
4. Add file upload for documents (optional)
5. Add authentication for admin dashboard (optional)

### Need Help?

- Check `API-DOCUMENTATION.md` for detailed API docs
- Check `README.md` for full documentation
- Review `supabase-schema.sql` for database structure

---

**Happy Coding! 🚀**
