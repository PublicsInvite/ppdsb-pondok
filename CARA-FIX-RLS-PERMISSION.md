## 🔧 CARA FIX RLS DENGAN BENAR

### ❌ Masalah: Permission Error

Error: `must be owner of table pendaftar`

### ✅ Solusi: Gunakan Role yang Benar di SQL Editor

---

## 📋 LANGKAH-LANGKAH:

### 1️⃣ Buka Supabase SQL Editor

🔗 https://supabase.com/dashboard/project/pislnvhdmsxudltcuuku/sql/new

### 2️⃣ **PENTING: Pilih Role yang Benar**

Di bagian bawah SQL Editor, ada dropdown **"Run as role"**

- ❌ JANGAN pilih `anon` atau `authenticated`
- ✅ HARUS pilih **`postgres`** (superuser role)

![image](https://github.com/user-attachments/assets/role-selector.png)

### 3️⃣ Copy & Paste SQL Ini:

```sql
-- Disable RLS temporarily
ALTER TABLE pendaftar DISABLE ROW LEVEL SECURITY;

-- Enable RLS
ALTER TABLE pendaftar ENABLE ROW LEVEL SECURITY;

-- Drop existing policies
DROP POLICY IF EXISTS "Allow public insert" ON pendaftar;
DROP POLICY IF EXISTS "anon_insert_policy" ON pendaftar;
DROP POLICY IF EXISTS "service_role_all_policy" ON pendaftar;

-- Create INSERT policy for anon (public form)
CREATE POLICY "anon_insert_policy"
ON pendaftar
FOR INSERT
TO anon
WITH CHECK (true);

-- Create ALL policy for service_role (admin)
CREATE POLICY "service_role_all_policy"
ON pendaftar
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- Grant permissions
GRANT INSERT ON pendaftar TO anon;
GRANT ALL ON pendaftar TO service_role;

-- Verify policies
SELECT
    policyname,
    roles,
    cmd
FROM pg_policies
WHERE tablename = 'pendaftar';
```

### 4️⃣ Klik "RUN" (atau tekan Cmd+Enter)

### 5️⃣ Verifikasi Output

Seharusnya muncul tabel dengan hasil seperti ini:

```
policyname              | roles          | cmd
------------------------|----------------|--------
anon_insert_policy      | {anon}         | INSERT
service_role_all_policy | {service_role} | ALL
```

---

## 🧪 TEST SETELAH FIX

Jalankan test script:

```bash
.venv/bin/python test_rls_anon.py
```

✅ **Expected Output:**

```
🧪 Testing RLS policy with ANON key...
✅ SUCCESS! RLS policy is working correctly!
```

---

## 📝 PENJELASAN ROLE:

1. **`postgres`** = Superuser role (pemilik database)

   - Digunakan untuk: DDL commands (CREATE, DROP, ALTER)
   - Di SQL Editor: Pilih "postgres" di dropdown role

2. **`anon`** = Anonymous role (public users)

   - Digunakan untuk: User yang belum login (form pendaftaran)
   - Di API: Menggunakan SUPABASE_ANON_KEY

3. **`service_role`** = Service role (backend/admin)
   - Digunakan untuk: Admin operations, bypass RLS
   - Di API: Menggunakan SUPABASE_SERVICE_ROLE_KEY

---

## ⚠️ TROUBLESHOOTING

### Jika masih error "must be owner":

1. Pastikan dropdown **"Run as role"** = **`postgres`**
2. Coba refresh halaman Supabase Dashboard
3. Logout dan login kembali ke Supabase

### Jika tidak ada dropdown role:

SQL Editor versi lama mungkin tidak ada dropdown. Gunakan:

```sql
SET ROLE postgres;
-- kemudian jalankan SQL di atas
```
