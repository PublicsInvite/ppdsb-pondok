# System Architecture Diagram

## 🏗️ High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         CLIENT SIDE                               │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐               │
│  │  index.html│  │ daftar.html│  │  admin.html  │               │
│  │  (Landing) │  │   (Form)   │  │ (Dashboard)  │               │
│  └─────┬──────┘  └─────┬──────┘  └──────┬───────┘               │
│        │               │                 │                        │
│        │               │                 │                        │
│        └───────┬───────┴────────┬────────┘                       │
│                │                │                                 │
│                │    Assets:     │                                 │
│                │  • styles.css  │                                 │
│                │  • app.js      │                                 │
│                │  • Bootstrap   │                                 │
│                │  • AOS         │                                 │
└────────────────┼────────────────┼─────────────────────────────────┘
                 │                │
                 ↓                ↓
┌──────────────────────────────────────────────────────────────────┐
│                      VERCEL EDGE NETWORK                          │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Python Serverless Functions                 │    │
│  │                                                          │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │  POST /api/pendaftar_create                      │   │    │
│  │  │  • Validate input (jenisKelamin, required fields)│   │    │
│  │  │  • Use SUPABASE_ANON_KEY (public access)        │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  │                                                          │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │  GET /api/pendaftar_list                         │   │    │
│  │  │  • Filter by status, search by name              │   │    │
│  │  │  • Pagination (page, pageSize)                   │   │    │
│  │  │  • Use SUPABASE_SERVICE_ROLE_KEY (admin)        │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  │                                                          │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │  PATCH /api/pendaftar_status                     │   │    │
│  │  │  • Call RPC: pendaftar_set_status               │   │    │
│  │  │  • Update status + deskripsi                     │   │    │
│  │  │  • Use SUPABASE_SERVICE_ROLE_KEY (admin)        │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  │                                                          │    │
│  │  ┌──────────────────────────────────────────────────┐   │    │
│  │  │  api/_supabase.py (Helper)                       │   │    │
│  │  │  • Create Supabase client                        │   │    │
│  │  │  • Switch between ANON_KEY / SERVICE_ROLE_KEY   │   │    │
│  │  └──────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────┘    │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ HTTPS + Auth Header
                             ↓
┌──────────────────────────────────────────────────────────────────┐
│                        SUPABASE                                   │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │               PostgreSQL Database                       │     │
│  │                                                         │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  Table: pendaftar                                │   │     │
│  │  │  ┌─────────────────────────────────────────┐    │   │     │
│  │  │  │ • id (BIGSERIAL, PK)                    │    │   │     │
│  │  │  │ • nomorRegistrasi (TEXT, UNIQUE)        │    │   │     │
│  │  │  │ • nikCalon, kkNo, nisn                  │    │   │     │
│  │  │  │ • namaLengkap, tempatLahir, ...         │    │   │     │
│  │  │  │ • alamatJalan, desa, kecamatan, ...     │    │   │     │
│  │  │  │ • namaAyah, nikAyah, namaIbu, nikIbu   │    │   │     │
│  │  │  │ • statusBerkas (MENUNGGU/DITERIMA/...)  │    │   │     │
│  │  │  │ • createdAt, updatedAt (TIMESTAMPTZ)    │    │   │     │
│  │  │  └─────────────────────────────────────────┘    │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  │                                                         │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  Triggers                                        │   │     │
│  │  │  • generate_nomor_registrasi (BEFORE INSERT)   │   │     │
│  │  │  • update_timestamp (BEFORE UPDATE)            │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  │                                                         │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  RPC Functions                                   │   │     │
│  │  │  • pendaftar_set_status(p_id, p_status, ...)   │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  │                                                         │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  Row Level Security (RLS)                        │   │     │
│  │  │  • anon: INSERT only                            │   │     │
│  │  │  • service_role: ALL operations                 │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  │                                                         │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  Indexes                                         │   │     │
│  │  │  • idx_pendaftar_status                         │   │     │
│  │  │  • idx_pendaftar_created_at                     │   │     │
│  │  │  • idx_pendaftar_nama                           │   │     │
│  │  │  • idx_pendaftar_nomor_reg                      │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  └────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Registration Flow (Detailed)

```
┌──────────┐
│  User    │
└────┬─────┘
     │
     │ 1. Visit /daftar
     ↓
┌────────────────┐
│  daftar.html   │
│  (Form Page)   │
└────┬───────────┘
     │
     │ 2. Fill form (20+ fields)
     │    - nikCalon, kkNo, nisn
     │    - namaLengkap, tempatLahir, tanggalLahir
     │    - jenisKelamin (L/P)
     │    - Address fields
     │    - Education plans
     │    - Parents data
     │
     │ 3. Submit (JavaScript fetch)
     ↓
┌────────────────────────────────────┐
│  POST /api/pendaftar_create        │
│  (Python Serverless Function)      │
│                                    │
│  4. Parse JSON body                │
│  5. Validate:                      │
│     • Required fields present      │
│     • jenisKelamin = 'L' or 'P'   │
│  6. Prepare payload object         │
│  7. Get Supabase client (ANON_KEY)│
└────────┬───────────────────────────┘
         │
         │ 8. Insert data
         ↓
┌────────────────────────────────────┐
│  Supabase (PostgreSQL)             │
│                                    │
│  9. Insert row into pendaftar      │
│  10. TRIGGER: generate_nomor_reg   │
│      → Set nomorRegistrasi         │
│         Format: REG-YYYYMMDD-00001 │
│  11. Set statusBerkas = MENUNGGU   │
│  12. Set createdAt = NOW()         │
│  13. Set updatedAt = NOW()         │
└────────┬───────────────────────────┘
         │
         │ 14. Return inserted row
         ↓
┌────────────────────────────────────┐
│  API Response                      │
│  {                                 │
│    "ok": true,                     │
│    "id": 1,                        │
│    "nomorRegistrasi": "REG-..."   │
│  }                                 │
└────────┬───────────────────────────┘
         │
         │ 15. Show success message
         ↓
┌────────────────┐
│  User sees     │
│  confirmation  │
│  with nomor    │
│  registrasi    │
└────────────────┘
```

---

## 🔍 Admin List Flow

```
┌──────────┐
│  Admin   │
└────┬─────┘
     │
     │ 1. Visit /admin
     ↓
┌────────────────────────┐
│  admin.html            │
│  (Dashboard)           │
│                        │
│  2. Page loads         │
│  3. Call loadData()    │
└────┬───────────────────┘
     │
     │ 4. Fetch with query params
     │    ?page=1&pageSize=10&q=&status=
     ↓
┌──────────────────────────────────────┐
│  GET /api/pendaftar_list             │
│  (Python Serverless Function)        │
│                                      │
│  5. Parse query parameters           │
│     • page (default: 1)              │
│     • pageSize (default: 10, max: 50)│
│     • q (search query)               │
│     • status (filter)                │
│                                      │
│  6. Calculate range (offset, limit)  │
│  7. Get Supabase client (SERVICE_ROLE)│
└────────┬─────────────────────────────┘
         │
         │ 8. Query database
         ↓
┌──────────────────────────────────────┐
│  Supabase Query Builder              │
│                                      │
│  9. SELECT * FROM pendaftar          │
│  10. ORDER BY createdAt DESC         │
│  11. IF status: WHERE statusBerkas = │
│  12. IF q: WHERE namaLengkap ILIKE   │
│  13. RANGE (offset, limit)           │
└────────┬─────────────────────────────┘
         │
         │ 14. Return rows
         ↓
┌──────────────────────────────────────┐
│  API Response                        │
│  {                                   │
│    "ok": true,                       │
│    "rows": [...],                    │
│    "page": 1,                        │
│    "pageSize": 10                    │
│  }                                   │
└────────┬─────────────────────────────┘
         │
         │ 15. Render table
         │ 16. Render pagination
         ↓
┌──────────────────────────┐
│  Admin sees:             │
│  • Table with data       │
│  • Status badges         │
│  • Action buttons        │
│  • Pagination controls   │
└──────────────────────────┘
```

---

## ✏️ Status Update Flow

```
┌──────────┐
│  Admin   │
└────┬─────┘
     │
     │ 1. Click "Terima" or "Tolak"
     ↓
┌────────────────────────┐
│  JavaScript Handler    │
│  updateStatus()        │
│                        │
│  2. Show confirmation  │
│  3. User confirms      │
└────┬───────────────────┘
     │
     │ 4. PATCH request
     │    Body: { id, status, alasan }
     ↓
┌──────────────────────────────────────┐
│  PATCH /api/pendaftar_status         │
│  (Python Serverless Function)        │
│                                      │
│  5. Parse JSON body                  │
│  6. Validate:                        │
│     • id present                     │
│     • status in valid values         │
│       (MENUNGGU/DITERIMA/DITOLAK)   │
│  7. Get Supabase client (SERVICE_ROLE)│
└────────┬─────────────────────────────┘
         │
         │ 8. Call RPC function
         ↓
┌──────────────────────────────────────┐
│  Supabase RPC                        │
│  pendaftar_set_status()              │
│                                      │
│  9. Validate status value            │
│  10. UPDATE pendaftar SET:           │
│      • statusBerkas = p_status       │
│      • deskripsiStatus = p_deskripsi │
│  11. TRIGGER: update_timestamp       │
│      → Set updatedAt = NOW()         │
│  12. Check if row found              │
│  13. Raise exception if not found    │
└────────┬─────────────────────────────┘
         │
         │ 14. Return success
         ↓
┌──────────────────────────────────────┐
│  API Response                        │
│  { "ok": true }                      │
└────────┬─────────────────────────────┘
         │
         │ 15. Show alert
         │ 16. Reload data
         ↓
┌──────────────────────────┐
│  Admin sees:             │
│  • Success message       │
│  • Updated status badge  │
│  • Updated timestamp     │
└──────────────────────────┘
```

---

## 🔐 Security Model

```
┌─────────────────────────────────────────────────┐
│              Security Layers                     │
├─────────────────────────────────────────────────┤
│                                                  │
│  Layer 1: Environment Variables                  │
│  ┌────────────────────────────────────────┐     │
│  │ • SUPABASE_URL (public)                │     │
│  │ • SUPABASE_ANON_KEY (public ops)       │     │
│  │ • SUPABASE_SERVICE_ROLE_KEY (secret!)  │     │
│  └────────────────────────────────────────┘     │
│                                                  │
│  Layer 2: API Access Control                     │
│  ┌────────────────────────────────────────┐     │
│  │ Public Endpoint:                        │     │
│  │   POST /api/pendaftar_create           │     │
│  │   → Uses ANON_KEY                      │     │
│  │   → Can only INSERT                    │     │
│  │                                         │     │
│  │ Admin Endpoints:                        │     │
│  │   GET /api/pendaftar_list              │     │
│  │   PATCH /api/pendaftar_status          │     │
│  │   → Use SERVICE_ROLE_KEY               │     │
│  │   → Can SELECT/UPDATE                  │     │
│  └────────────────────────────────────────┘     │
│                                                  │
│  Layer 3: Row Level Security (RLS)               │
│  ┌────────────────────────────────────────┐     │
│  │ Policy 1: "Allow public insert"        │     │
│  │   FOR INSERT                            │     │
│  │   TO anon, authenticated                │     │
│  │   WITH CHECK (true)                     │     │
│  │                                         │     │
│  │ Policy 2: "Allow service role all"     │     │
│  │   FOR ALL                               │     │
│  │   TO service_role                       │     │
│  │   USING (true)                          │     │
│  └────────────────────────────────────────┘     │
│                                                  │
│  Layer 4: Data Validation                        │
│  ┌────────────────────────────────────────┐     │
│  │ API Level:                              │     │
│  │ • Required fields check                 │     │
│  │ • Regex validation (jenisKelamin)      │     │
│  │ • Status value whitelist               │     │
│  │                                         │     │
│  │ Database Level:                         │     │
│  │ • NOT NULL constraints                  │     │
│  │ • CHECK constraints                     │     │
│  │ • UNIQUE constraints                    │     │
│  └────────────────────────────────────────┘     │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 📦 Deployment Pipeline

```
┌──────────────┐
│ Local Dev    │
│              │
│ 1. Code      │
│ 2. Test      │
│ 3. Git commit│
└──────┬───────┘
       │
       │ git push
       ↓
┌──────────────┐
│  GitHub      │
│  Repository  │
└──────┬───────┘
       │
       │ webhook
       ↓
┌─────────────────────────────────┐
│  Vercel Build Pipeline          │
│                                 │
│  1. Clone repository            │
│  2. Detect Python runtime       │
│  3. Install requirements.txt    │
│  4. Build static assets         │
│  5. Deploy to edge network      │
│  6. Inject environment vars     │
└──────┬──────────────────────────┘
       │
       │ deploy
       ↓
┌─────────────────────────────────┐
│  Vercel Edge Network            │
│                                 │
│  • HTML served from CDN         │
│  • Python functions serverless  │
│  • Auto-scaling                 │
│  • HTTPS by default             │
└──────┬──────────────────────────┘
       │
       │ API calls
       ↓
┌─────────────────────────────────┐
│  Supabase                       │
│                                 │
│  • PostgreSQL database          │
│  • Connection pooling           │
│  • Auto-backups                 │
│  • Realtime subscriptions       │
└─────────────────────────────────┘
```

---

**Last Updated:** October 14, 2025
