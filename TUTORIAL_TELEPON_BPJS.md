# TUTORIAL: Tambah No Telepon Orang Tua & Upload BPJS

## 📋 Ringkasan
Menambahkan 2 field baru di form pendaftaran:
- **No Telepon Orang Tua**: Field input telepon
- **Upload File BPJS**: Field upload file (PDF/JPG/PNG)

---

## 🗄️ STEP 1: UPDATE DATABASE (SUPABASE)

### 1.1 Login ke Supabase
1. Buka https://supabase.com
2. Login dan pilih project Anda
3. Klik **SQL Editor** di sidebar kiri

### 1.2 Jalankan SQL
1. Copy semua isi file `sql/add_telepon_bpjs.sql`
2. Paste di SQL Editor
3. Klik **RUN** (Ctrl + Enter)
4. Tunggu hingga selesai

### 1.3 Verifikasi
Jalankan query ini untuk cek kolom sudah ada:
```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'pendaftar' 
AND column_name IN ('telepon_orang_tua', 'file_bpjs');
```

Expected result:
```
column_name         | data_type          | is_nullable
--------------------|--------------------|-----------
telepon_orang_tua   | character varying  | YES
file_bpjs           | text              | YES
```

✅ **Database siap!**

---

## 🎨 STEP 2: UPDATE FRONTEND (HTML)

### File: `public/daftar.html`

#### 2.1 Tambah Field No Telepon Orang Tua
Cari bagian form (setelah field nomor telepon siswa), tambahkan:
```html
<!-- No Telepon Orang Tua -->
<div class="mb-3">
  <label for="teleponOrtu" class="form-label">
    No Telepon Orang Tua/Wali <span class="text-danger">*</span>
  </label>
  <input
    type="tel"
    class="form-control"
    id="teleponOrtu"
    name="teleponOrtu"
    placeholder="081234567890"
    required
  />
  <div class="form-text">Format: 081234567890 atau +62812345678</div>
</div>
```

#### 2.2 Tambah Field Upload BPJS
Cari bagian upload files (setelah upload KK), tambahkan:
```html
<!-- Upload BPJS -->
<div class="mb-3">
  <label for="fileBpjs" class="form-label">
    Upload Kartu BPJS <span class="text-danger">*</span>
  </label>
  <input
    type="file"
    class="form-control"
    id="fileBpjs"
    name="fileBpjs"
    accept=".jpg,.jpeg,.png,.pdf"
    required
  />
  <div class="form-text">Format: JPG, PNG, atau PDF (Maks 2MB)</div>
</div>
```

#### 2.3 Update JavaScript Submit Handler
Cari function submit form, tambahkan field baru:
```javascript
// Get values
const teleponOrtu = document.getElementById('teleponOrtu').value;
const fileBpjs = document.getElementById('fileBpjs').files[0];

// Upload BPJS
const bpjsBase64 = await fileToBase64(fileBpjs);
const bpjsResponse = await fetch('/api/upload_file', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    file: bpjsBase64.split(',')[1],
    fileName: fileBpjs.name,
    fileType: 'bpjs',
    mimeType: fileBpjs.type,
    nomorRegistrasi: nomorReg
  })
});
const bpjsResult = await bpjsResponse.json();

// Add to formData
formData.teleponOrtu = teleponOrtu;
formData.fileBpjs = bpjsResult.url;
```

---

## ⚙️ STEP 3: UPDATE BACKEND (API)

### File: `api/pendaftar_create.py`

#### 3.1 Update Insert Data
Cari bagian `.insert()`, tambahkan field baru:
```python
result = supa.table("pendaftar").insert({
    # ... existing fields ...
    "teleponortu": body.get("teleponOrtu"),
    "filebpjs": body.get("fileBpjs"),
}).execute()
```

**CATATAN**: Nama kolom di database pakai lowercase tanpa underscore:
- Frontend: `teleponOrtu` (camelCase)
- Backend: `teleponortu` (lowercase)
- Database: `telepon_orang_tua` (snake_case)

---

## 🔍 STEP 4: UPDATE ADMIN VIEW

### File: `public/admin.html`

#### 4.1 Tambah di Modal Detail
Cari modal detail pendaftar, tambahkan:
```html
<dt class="col-sm-5">No Telepon Orang Tua:</dt>
<dd class="col-sm-7" id="detail-telepon-ortu"></dd>

<!-- Tambah tombol download BPJS -->
<dt class="col-sm-5">Kartu BPJS:</dt>
<dd class="col-sm-7">
  <a id="detail-bpjs-link" href="#" target="_blank" class="btn btn-sm btn-info">
    <i class="bi bi-download"></i> Lihat BPJS
  </a>
</dd>
```

#### 4.2 Update JavaScript viewDetail()
```javascript
document.getElementById('detail-telepon-ortu').textContent = 
  data.teleponortu || '-';
document.getElementById('detail-bpjs-link').href = 
  data.filebpjs || '#';
```

---

## 📊 STEP 5: UPDATE CSV EXPORT

### File: `public/admin.html`

Cari function `exportToCSV()`, tambahkan kolom:
```javascript
const headers = [
  // ... existing headers ...
  'No Telepon Ortu',
  'File BPJS'
];

const row = [
  // ... existing fields ...
  escapeCSV(item.teleponortu || ''),
  escapeCSV(item.filebpjs || '')
].join(',');
```

---

## 🧪 TESTING

### 1. Test Database
```sql
-- Insert test data
UPDATE pendaftar 
SET telepon_orang_tua = '081234567890',
    file_bpjs = 'https://example.com/test.pdf'
WHERE id = 1;

-- Query test
SELECT nama_lengkap, telepon_orang_tua, file_bpjs 
FROM pendaftar 
LIMIT 5;
```

### 2. Test Form Pendaftaran
1. Buka `/daftar`
2. Isi form termasuk No Telepon Ortu
3. Upload file BPJS (PDF/JPG)
4. Submit
5. Cek database apakah data masuk

### 3. Test Admin View
1. Login admin
2. Klik detail pendaftar
3. Cek No Telepon Ortu muncul
4. Klik tombol "Lihat BPJS" → file terbuka

### 4. Test CSV Export
1. Export CSV dari admin
2. Buka di Excel/Google Sheets
3. Cek kolom "No Telepon Ortu" dan "File BPJS" ada

---

## 🔒 OPTIONAL: Make Fields REQUIRED

Jika ingin field WAJIB diisi:
```sql
ALTER TABLE pendaftar 
ALTER COLUMN telepon_orang_tua SET NOT NULL;

ALTER TABLE pendaftar 
ALTER COLUMN file_bpjs SET NOT NULL;
```

⚠️ **Warning**: Jalankan ini hanya setelah semua data lama sudah diisi!

---

## 📝 CHECKLIST

- [ ] Jalankan SQL di Supabase
- [ ] Update form pendaftaran (daftar.html)
- [ ] Update API create (pendaftar_create.py)
- [ ] Update admin detail view
- [ ] Update CSV export
- [ ] Test end-to-end
- [ ] Deploy ke production

---

## 🆘 TROUBLESHOOTING

**Q: Error "column does not exist"**
A: Pastikan sudah jalankan SQL ALTER TABLE di Supabase

**Q: File BPJS tidak terupload**
A: Cek Supabase Storage bucket "pendaftar-files" sudah ada dan public

**Q: Data tidak masuk ke database**
A: Cek nama field di API harus lowercase: `teleponortu`, `filebpjs`

**Q: Admin tidak bisa lihat BPJS**
A: Pastikan URL file valid dan bucket Supabase public

---

**Good luck! 🚀**
