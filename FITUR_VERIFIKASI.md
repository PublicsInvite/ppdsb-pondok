# Fitur Verifikasi Admin - Pondok Pesantren

## 📋 Deskripsi
Fitur verifikasi pendaftar dengan 3 status: **Diterima**, **Revisi**, dan **Ditolak** beserta catatan/alasan.

## ✨ Fitur yang Ditambahkan

### 1. Dashboard Stats
- **Total Pendaftar**: Jumlah semua pendaftar
- **Pending**: Pendaftar yang belum diverifikasi
- **Revisi**: Pendaftar yang perlu melakukan revisi dokumen
- **Diterima**: Pendaftar yang diterima
- **Ditolak**: Pendaftar yang ditolak

### 2. Tombol Aksi Verifikasi
Untuk pendaftar dengan status **Pending** atau **Revisi**, admin dapat:
- ✅ **Terima** (tombol hijau dengan icon check-circle)
- 🔄 **Revisi** (tombol biru dengan icon arrow-repeat)
- ❌ **Tolak** (tombol merah dengan icon x-circle)

### 3. Modal Verifikasi
Saat admin klik tombol aksi, muncul modal dengan:
- **Judul**: Sesuai status (Verifikasi: Diterima/Revisi/Ditolak)
- **Status Display**: Menampilkan status dengan warna yang sesuai
- **Form Catatan**: 
  - Untuk **Revisi**: "Catatan Revisi" - Jelaskan apa yang perlu direvisi
  - Untuk **Ditolak**: "Alasan Penolakan" - Jelaskan alasan penolakan
  - Untuk **Diterima**: "Catatan" - Opsional
- **Tombol Konfirmasi**: Warna sesuai status (hijau/biru/merah)

### 4. Color Coding
- **Pending**: Warning (Kuning/Orange) 
- **Revisi**: Info (Biru)
- **Diterima**: Success (Hijau)
- **Ditolak**: Danger (Merah)
- **Selesai**: Secondary (Abu-abu) - untuk status final (diterima/ditolak)

## 🔧 Cara Penggunaan

### Login Admin
1. Buka `/login`
2. Email: `admin`
3. Password: `admin`
4. Klik Login

### Verifikasi Pendaftar
1. Masuk ke dashboard admin `/admin`
2. Lihat daftar pendaftar di tab "Data Pendaftar"
3. Untuk pendaftar dengan status **Pending** atau **Revisi**:
   - Klik tombol **Terima** (✓) untuk menerima
   - Klik tombol **Revisi** (↻) untuk minta revisi
   - Klik tombol **Tolak** (✗) untuk menolak
4. Modal verifikasi akan muncul
5. Isi catatan/alasan (wajib untuk revisi & tolak, opsional untuk terima)
6. Klik tombol konfirmasi sesuai status
7. Status akan terupdate dan pendaftar mendapat notifikasi

### Melihat Statistik
Dashboard menampilkan real-time statistik:
- Total semua pendaftar
- Jumlah per status (Pending/Revisi/Diterima/Ditolak)

## 📡 API Endpoint

### Update Status Pendaftar
**Endpoint**: `PATCH /api/pendaftar_status`

**Request Body**:
```json
{
  "id": 1,
  "status": "revisi",
  "alasan": "KTP tidak jelas, mohon upload ulang dengan resolusi lebih tinggi"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Status updated"
}
```

**Status yang Valid**:
- `pending` - Menunggu verifikasi
- `revisi` - Perlu revisi dokumen
- `diterima` - Diterima
- `ditolak` - Ditolak

## 🎨 Design Improvements

### Before:
- Hanya 2 tombol: Terima (✓) dan Tolak (✗)
- Tidak ada opsi revisi
- Tidak ada catatan/alasan

### After:
- 3 tombol: Terima (✓), Revisi (↻), Tolak (✗)
- Modal konfirmasi dengan form catatan
- Color-coded badges untuk setiap status
- Statistik lengkap dengan card Revisi
- UX lebih baik dengan konfirmasi dan feedback

## 🔄 Workflow Verifikasi

```
PENDAFTAR BARU
    ↓
[PENDING] → Admin Review
    ↓
    ├─→ [DITERIMA] ✅ (Final)
    ├─→ [REVISI] 🔄 → Pendaftar perbaiki → [PENDING] → Review lagi
    └─→ [DITOLAK] ❌ (Final)
```

## 📝 Notes
- Status **Diterima** dan **Ditolak** bersifat final (tombol disabled)
- Status **Revisi** dapat diverifikasi ulang menjadi Diterima/Ditolak
- Catatan disimpan untuk tracking dan komunikasi dengan pendaftar
- Semua perubahan status tercatat dengan timestamp

## 🚀 Deployment
```bash
git add -A
git commit -m "feat: add verifikasi with 3 status and notes"
vercel --prod
```

**URL Production**: https://project-python-7y1nfp19g-dewas-projects-d0163f17.vercel.app/admin
