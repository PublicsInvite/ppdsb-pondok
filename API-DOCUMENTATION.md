# API Documentation

## Base URL

```
https://your-app.vercel.app
```

## Endpoints

### 1. Create Pendaftar (Public)

**Endpoint:** `POST /api/pendaftar_create`

**Description:** Create a new registration. This endpoint is public and can be accessed without authentication.

**Request Body:**

```json
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
```

**Field Validations:**

- `jenisKelamin`: Must be either 'L' (Laki-laki) or 'P' (Perempuan)
- `nisn`: Optional, can be null or empty string
- All other fields are required and must not be empty

**Success Response:**

```json
{
  "ok": true,
  "id": 1,
  "nomorRegistrasi": "REG-20251014-000001"
}
```

**Error Response:**

```json
{
  "ok": false,
  "error": "Missing required field: namaLengkap"
}
```

**Status Codes:**

- `201` - Created successfully
- `400` - Bad request (missing required fields)
- `422` - Unprocessable entity (invalid field values)
- `500` - Server error

---

### 2. List Pendaftar (Admin)

**Endpoint:** `GET /api/pendaftar_list`

**Description:** List all registrations with filtering, search, and pagination. Requires service role access (admin only).

**Query Parameters:**

- `page` (optional): Page number (default: 1)
- `pageSize` (optional): Number of items per page (default: 10, max: 50)
- `q` (optional): Search query (searches in `namaLengkap`)
- `status` (optional): Filter by status (`MENUNGGU_VERIFIKASI`, `DITERIMA`, `DITOLAK`)

**Example Request:**

```
GET /api/pendaftar_list?page=1&pageSize=10&q=ahmad&status=MENUNGGU_VERIFIKASI
```

**Success Response:**

```json
{
  "ok": true,
  "rows": [
    {
      "id": 1,
      "nomorRegistrasi": "REG-20251014-000001",
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
      "nikIbu": "3201234567890101",
      "statusBerkas": "MENUNGGU_VERIFIKASI",
      "deskripsiStatus": null,
      "createdAt": "2025-10-14T10:30:00.000Z",
      "updatedAt": "2025-10-14T10:30:00.000Z"
    }
  ],
  "page": 1,
  "pageSize": 10
}
```

**Error Response:**

```json
{
  "ok": false,
  "error": "Error message here"
}
```

**Status Codes:**

- `200` - Success
- `500` - Server error

---

### 3. Update Status (Admin)

**Endpoint:** `PATCH /api/pendaftar_status`

**Description:** Update registration status. Requires service role access (admin only). Uses Supabase RPC function `pendaftar_set_status`.

**Request Body:**

```json
{
  "id": 1,
  "status": "DITERIMA",
  "alasan": "Memenuhi semua persyaratan"
}
```

**Field Descriptions:**

- `id` (required): The pendaftar ID
- `status` (required): New status value
  - `MENUNGGU_VERIFIKASI` - Waiting for verification
  - `DITERIMA` - Accepted
  - `DITOLAK` - Rejected
- `alasan` (optional): Reason/description for the status change

**Success Response:**

```json
{
  "ok": true
}
```

**Error Response:**

```json
{
  "ok": false,
  "error": "id and status are required"
}
```

```json
{
  "ok": false,
  "error": "status must be one of: MENUNGGU_VERIFIKASI, DITERIMA, DITOLAK"
}
```

**Status Codes:**

- `200` - Success
- `400` - Bad request (missing or invalid fields)
- `500` - Server error

---

## Status Values

The system uses three status values:

1. **MENUNGGU_VERIFIKASI** (default)

   - Initial status when a new registration is created
   - Waiting for admin review

2. **DITERIMA**

   - Registration approved by admin
   - Candidate is accepted

3. **DITOLAK**
   - Registration rejected by admin
   - Candidate is not accepted

---

## CORS

All endpoints support CORS with the following headers:

- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, PATCH, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type`

---

## Authentication & Authorization

### Public Access

- `POST /api/pendaftar_create` - Uses `SUPABASE_ANON_KEY`
- Anyone can create a new registration

### Admin Access

- `GET /api/pendaftar_list` - Uses `SUPABASE_SERVICE_ROLE_KEY`
- `PATCH /api/pendaftar_status` - Uses `SUPABASE_SERVICE_ROLE_KEY`
- These endpoints require service role access (server-side only)

⚠️ **Security Note:** Never expose `SUPABASE_SERVICE_ROLE_KEY` to the browser. These keys should only be used in server-side code.

---

## Error Handling

All endpoints return errors in the following format:

```json
{
  "ok": false,
  "error": "Error description here"
}
```

Common error scenarios:

- Missing required fields → 400 Bad Request
- Invalid field values → 422 Unprocessable Entity
- Server/database errors → 500 Internal Server Error

---

## Rate Limiting

Vercel's default rate limiting applies to all endpoints. For production use, consider implementing additional rate limiting for the public registration endpoint.

---

## Examples

### Create Registration (cURL)

```bash
curl -X POST https://your-app.vercel.app/api/pendaftar_create \
  -H "Content-Type: application/json" \
  -d '{
    "nikCalon": "3201234567890123",
    "kkNo": "3201234567890001",
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
  }'
```

### List Registrations (cURL)

```bash
curl https://your-app.vercel.app/api/pendaftar_list?page=1&pageSize=10
```

### Update Status (cURL)

```bash
curl -X PATCH https://your-app.vercel.app/api/pendaftar_status \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "status": "DITERIMA",
    "alasan": "Memenuhi semua persyaratan"
  }'
```

### JavaScript/Fetch Examples

#### Create Registration

```javascript
const createRegistration = async (data) => {
  const response = await fetch("/api/pendaftar_create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();

  if (result.ok) {
    console.log("Registration created:", result.nomorRegistrasi);
  } else {
    console.error("Error:", result.error);
  }
};
```

#### List Registrations

```javascript
const listRegistrations = async (page = 1, status = "") => {
  const params = new URLSearchParams({
    page: page,
    pageSize: 10,
    status: status,
  });

  const response = await fetch(`/api/pendaftar_list?${params}`);
  const result = await response.json();

  if (result.ok) {
    console.log("Registrations:", result.rows);
  }
};
```

#### Update Status

```javascript
const updateStatus = async (id, status, alasan = null) => {
  const response = await fetch("/api/pendaftar_status", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id, status, alasan }),
  });

  const result = await response.json();

  if (result.ok) {
    console.log("Status updated successfully");
  }
};
```
