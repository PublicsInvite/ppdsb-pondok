-- =====================================================
-- SQL untuk Setup Storage di Supabase
-- =====================================================
-- Run di Supabase SQL Editor
-- =====================================================

-- 1. Tambah kolom untuk menyimpan URL file di tabel pendaftar
ALTER TABLE pendaftar 
ADD COLUMN IF NOT EXISTS file_ijazah TEXT,
ADD COLUMN IF NOT EXISTS file_kk TEXT,
ADD COLUMN IF NOT EXISTS file_akta TEXT,
ADD COLUMN IF NOT EXISTS file_foto TEXT;

-- =====================================================
-- CARA SETUP STORAGE BUCKET & POLICIES:
-- =====================================================
-- Karena storage policies tidak bisa dibuat via SQL,
-- setup harus dilakukan di Supabase Dashboard.
-- =====================================================

-- STEP 1: Buat Storage Bucket
-- =============================
-- 1. Buka Supabase Dashboard (https://supabase.com/dashboard)
-- 2. Pilih project Anda
-- 3. Klik "Storage" di menu kiri
-- 4. Klik tombol "New bucket"
-- 5. Isi form:
--    - Name: pendaftar-files
--    - Public bucket: CENTANG ✅ (Yes)
--    - File size limit: 2MB (default)
--    - Allowed MIME types: (biarkan kosong = semua)
-- 6. Klik "Create bucket"

-- STEP 2: Setup Policies untuk Bucket
-- =====================================
-- Setelah bucket dibuat, klik bucket "pendaftar-files"
-- Lalu klik tab "Policies"

-- POLICY 1: Allow Public Upload (anon dapat upload)
-- --------------------------------------------------
-- Klik "New Policy" > pilih template "Enable upload for users"
-- Atau buat custom policy:
--   Policy name: Allow anon upload
--   Allowed operations: INSERT
--   Target roles: anon
--   USING expression: true
--   WITH CHECK expression: true

-- POLICY 2: Allow Public Read (semua orang bisa download)
-- --------------------------------------------------------
-- Klik "New Policy" > pilih template "Enable read access for all users"
-- Atau buat custom policy:
--   Policy name: Allow public read
--   Allowed operations: SELECT
--   Target roles: anon, authenticated, public
--   USING expression: true

-- POLICY 3: Allow Service Role Delete (admin bisa hapus)
-- -------------------------------------------------------
-- Klik "New Policy" > buat custom policy:
--   Policy name: Allow service role delete
--   Allowed operations: DELETE
--   Target roles: service_role
--   USING expression: true

-- =====================================================
-- ALTERNATIF: Setup via SQL (jika policies table ada)
-- =====================================================
-- Jika Supabase sudah support, gunakan ini:
/*
CREATE POLICY "Allow anon upload"
ON storage.objects FOR INSERT
TO anon
WITH CHECK (bucket_id = 'pendaftar-files');

CREATE POLICY "Allow public read"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'pendaftar-files');

CREATE POLICY "Allow service role delete"
ON storage.objects FOR DELETE
TO service_role
USING (bucket_id = 'pendaftar-files');
*/

-- =====================================================
-- TESTING:
-- =====================================================
-- Setelah setup, test dengan:
-- 1. Upload file dari form pendaftaran
-- 2. Cek di Storage > pendaftar-files > lihat file
-- 3. Klik file > copy URL
-- 4. Paste URL di browser baru > harus bisa diakses
-- =====================================================
