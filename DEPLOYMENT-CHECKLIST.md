# 🚀 Deployment Checklist

Complete checklist untuk deploy Pondok Pesantren Registration System ke production.

---

## ✅ Pre-Deployment

### 1. Supabase Setup

- [ ] Buat project baru di [supabase.com](https://supabase.com)
- [ ] Tunggu project selesai provisioning (≈2 menit)
- [ ] Catat Project URL dari settings
- [ ] Catat API Keys (anon & service_role)

### 2. Database Schema

- [ ] Buka SQL Editor di Supabase Dashboard
- [ ] Copy paste isi `supabase-schema.sql`
- [ ] Execute script (klik RUN)
- [ ] Verify table created: check Tables section
- [ ] Verify triggers created: check Database → Triggers
- [ ] Verify RPC function: check Database → Functions

### 3. Test Database (Optional but Recommended)

- [ ] Copy paste isi `sample-data.sql`
- [ ] Execute script
- [ ] Verify 5 rows inserted: `SELECT COUNT(*) FROM pendaftar`
- [ ] Check nomor registrasi generated correctly
- [ ] Test RPC function manually:
  ```sql
  SELECT pendaftar_set_status(1, 'DITERIMA', 'Test approval');
  ```

### 4. Local Testing (Optional)

- [ ] Create `.env` file from `.env.example`
- [ ] Add your Supabase credentials
- [ ] Install: `pip install -r requirements.txt`
- [ ] Run: `vercel dev`
- [ ] Test registration at http://localhost:3000/daftar
- [ ] Test admin at http://localhost:3000/admin

---

## 🌐 Deployment

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

- [ ] CLI installed successfully
- [ ] Check version: `vercel --version`

### 2. Login to Vercel

```bash
vercel login
```

- [ ] Login successful
- [ ] Email verified

### 3. Deploy Project

```bash
cd "/Users/dewasatriaaa/Downloads/KULIAH/PROJECT CODE/project python"
vercel
```

**Answer prompts:**

- [ ] Set up and deploy? **Y**
- [ ] Which scope? **Select your account**
- [ ] Link to existing project? **N**
- [ ] What's your project's name? **pondok-registration** (or your choice)
- [ ] In which directory is your code located? **./** (default)
- [ ] Want to override the settings? **N**

- [ ] Deployment completed
- [ ] Note the deployment URL (e.g., pondok-registration.vercel.app)

### 4. Add Environment Variables

```bash
vercel env add SUPABASE_URL
```

- [ ] Enter value: `https://xxxxx.supabase.co`
- [ ] Select environments: **Production, Preview, Development**

```bash
vercel env add SUPABASE_ANON_KEY
```

- [ ] Enter value: `eyJhbGci...`
- [ ] Select environments: **Production, Preview, Development**

```bash
vercel env add SUPABASE_SERVICE_ROLE_KEY
```

- [ ] Enter value: `eyJhbGci...`
- [ ] Select environments: **Production, Preview, Development**
- [ ] ⚠️ Keep this key secret!

### 5. Redeploy with Environment Variables

```bash
vercel --prod
```

- [ ] Production deployment successful
- [ ] Note production URL

---

## 🧪 Post-Deployment Testing

### 1. Test Landing Page

- [ ] Visit: `https://your-app.vercel.app`
- [ ] Page loads correctly
- [ ] Animations working (AOS)
- [ ] Navigation links work
- [ ] No console errors

### 2. Test Registration Form

- [ ] Visit: `https://your-app.vercel.app/daftar`
- [ ] Form displays correctly
- [ ] Fill out all fields
- [ ] Submit form
- [ ] Success message appears
- [ ] Check Supabase dashboard for new record
- [ ] Verify nomor registrasi generated

**Test Data:**

```json
{
  "nikCalon": "3201234567890999",
  "kkNo": "3201234567890998",
  "nisn": "0012345999",
  "namaLengkap": "Test Production User",
  "tempatLahir": "Jakarta",
  "tanggalLahir": "2008-05-15",
  "jenisKelamin": "L",
  "alamatJalan": "Jl. Test Prod No. 1",
  "desa": "Test Desa",
  "kecamatan": "Test Kecamatan",
  "kotaKabupaten": "Jakarta",
  "provinsi": "DKI Jakarta",
  "ijazahFormalTerakhir": "SMP",
  "rencanaDomisili": "Mukim",
  "rencanaTingkat": "MTs",
  "rencanaKelas": "Kelas 1",
  "namaAyah": "Ayah Test Prod",
  "nikAyah": "3201234567890888",
  "namaIbu": "Ibu Test Prod",
  "nikIbu": "3201234567890777"
}
```

### 3. Test Admin Dashboard

- [ ] Visit: `https://your-app.vercel.app/admin`
- [ ] Dashboard loads correctly
- [ ] Table displays data
- [ ] Stats cards show counts
- [ ] Search works
- [ ] Filter by status works
- [ ] Pagination works (if >10 records)

### 4. Test Status Update

- [ ] Click "View" button on a record
- [ ] Modal shows correct data
- [ ] Close modal
- [ ] Click "Terima" (Accept) button
- [ ] Confirm action
- [ ] Success message appears
- [ ] Status badge updates to "DITERIMA"
- [ ] Check Supabase: verify status changed
- [ ] Check Supabase: verify updatedAt changed

### 5. Test API Endpoints Directly

**Create Registration:**

```bash
curl -X POST https://your-app.vercel.app/api/pendaftar_create \
  -H "Content-Type: application/json" \
  -d '{
    "nikCalon": "3201234567890111",
    "kkNo": "3201234567890112",
    "namaLengkap": "API Test User",
    "tempatLahir": "Jakarta",
    "tanggalLahir": "2008-05-15",
    "jenisKelamin": "P",
    "alamatJalan": "Jl. API Test",
    "desa": "Test",
    "kecamatan": "Test",
    "kotaKabupaten": "Jakarta",
    "provinsi": "DKI Jakarta",
    "ijazahFormalTerakhir": "SMP",
    "rencanaDomisili": "Mukim",
    "rencanaTingkat": "MTs",
    "rencanaKelas": "Kelas 1",
    "namaAyah": "Ayah API",
    "nikAyah": "3201234567890113",
    "namaIbu": "Ibu API",
    "nikIbu": "3201234567890114"
  }'
```

- [ ] Returns: `{"ok":true,"id":...,"nomorRegistrasi":"REG-..."}`

**List Registrations:**

```bash
curl https://your-app.vercel.app/api/pendaftar_list?page=1&pageSize=5
```

- [ ] Returns: `{"ok":true,"rows":[...],"page":1,"pageSize":5}`

**Update Status:**

```bash
curl -X PATCH https://your-app.vercel.app/api/pendaftar_status \
  -H "Content-Type: application/json" \
  -d '{"id":1,"status":"DITERIMA","alasan":"Test via API"}'
```

- [ ] Returns: `{"ok":true}`

---

## 🔒 Security Verification

### Environment Variables

- [ ] SERVICE_ROLE_KEY not exposed in browser
- [ ] Check Network tab: only see requests, not env vars
- [ ] .env file in .gitignore
- [ ] .env file NOT committed to Git

### Database Security

- [ ] RLS enabled on pendaftar table
- [ ] Test: try to access with invalid key (should fail)
- [ ] Test: anon key can INSERT (should work)
- [ ] Test: anon key can SELECT (should fail without service_role)

### API Security

- [ ] CORS headers present
- [ ] POST /api/pendaftar_create validates jenisKelamin
- [ ] POST /api/pendaftar_create validates required fields
- [ ] PATCH /api/pendaftar_status validates status values

---

## 📊 Performance Check

### Page Load Times

- [ ] Landing page: < 2s
- [ ] Registration form: < 2s
- [ ] Admin dashboard: < 3s

### API Response Times

- [ ] POST /api/pendaftar_create: < 1s
- [ ] GET /api/pendaftar_list: < 1s
- [ ] PATCH /api/pendaftar_status: < 1s

### Lighthouse Score (Optional)

- [ ] Run Lighthouse on landing page
- [ ] Performance: > 80
- [ ] Accessibility: > 90
- [ ] Best Practices: > 80
- [ ] SEO: > 80

---

## 🎨 Customization (Optional)

### Branding

- [ ] Update title in HTML files
- [ ] Update navbar brand text
- [ ] Update footer text
- [ ] Add logo (if available)

### Styling

- [ ] Update primary color in styles.css (--primary-green)
- [ ] Update Bootstrap color scheme
- [ ] Add custom fonts (if needed)

### Content

- [ ] Update landing page content
- [ ] Update feature descriptions
- [ ] Update contact information
- [ ] Add FAQ section (if needed)

---

## 📱 Mobile Testing

### Responsive Design

- [ ] Test on phone (< 768px)
- [ ] Test on tablet (768px - 1024px)
- [ ] Test on desktop (> 1024px)
- [ ] Navigation menu works on mobile
- [ ] Forms usable on mobile
- [ ] Tables scroll horizontally on mobile

---

## 🔔 Monitoring Setup (Optional)

### Vercel Analytics

- [ ] Enable Vercel Analytics in dashboard
- [ ] Monitor page views
- [ ] Monitor API requests

### Error Tracking

- [ ] Check Vercel function logs
- [ ] Set up error alerts (optional)
- [ ] Monitor Supabase logs

### Uptime Monitoring

- [ ] Set up uptime monitoring (UptimeRobot, etc.)
- [ ] Set up email/SMS alerts
- [ ] Monitor API endpoints

---

## 📋 Documentation

### Update URLs

- [ ] Update README.md with production URL
- [ ] Update API-DOCUMENTATION.md examples
- [ ] Update QUICK-START.md

### Share with Team

- [ ] Share production URL
- [ ] Share admin dashboard URL
- [ ] Share API documentation
- [ ] Share Supabase credentials (securely!)

---

## 🎉 Go Live Checklist

### Final Checks

- [ ] All features working
- [ ] No console errors
- [ ] No broken links
- [ ] Mobile responsive
- [ ] Forms validated
- [ ] Error messages clear
- [ ] Success messages clear

### Announcement

- [ ] Announce to stakeholders
- [ ] Share registration URL
- [ ] Provide admin credentials
- [ ] Schedule training (if needed)

### Backup Plan

- [ ] Export current database (if replacing old system)
- [ ] Document rollback procedure
- [ ] Have Supabase admin credentials ready
- [ ] Have Vercel admin credentials ready

---

## 📞 Support Setup

### Documentation

- [ ] README.md accessible
- [ ] API-DOCUMENTATION.md accessible
- [ ] QUICK-START.md accessible
- [ ] Contact information updated

### Issue Tracking

- [ ] Set up issue tracker (GitHub Issues, etc.)
- [ ] Document common issues
- [ ] Create FAQ document

---

## ✅ Completion

### Sign Off

- [ ] Tested by: ********\_******** Date: **\_\_\_**
- [ ] Approved by: ******\_\_\_****** Date: **\_\_\_**
- [ ] Deployed by: ******\_\_\_****** Date: **\_\_\_**

### Production URLs

```
Landing Page: https://_________________.vercel.app
Registration: https://_________________.vercel.app/daftar
Admin Dashboard: https://_________________.vercel.app/admin

API Base URL: https://_________________.vercel.app/api
```

### Credentials (Store Securely!)

```
Supabase URL: https://_________________.supabase.co
Supabase Anon Key: ___________________________________
Supabase Service Role Key: ___________________________
Vercel Project ID: ____________________________________
```

---

## 🚀 You're Live!

**Congratulations! Your Pondok Pesantren Registration System is now in production!**

### Next Steps:

1. Monitor first registrations
2. Gather user feedback
3. Plan feature enhancements
4. Schedule regular backups
5. Review analytics weekly

---

**Last Updated:** October 14, 2025
**Version:** 1.0.0
