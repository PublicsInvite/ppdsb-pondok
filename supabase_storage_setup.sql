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

-- 2. Buat bucket untuk storage (RUN DI SUPABASE DASHBOARD > Storage)
-- Nama bucket: pendaftar-files
-- Public: Yes (agar bisa diakses langsung)

-- 3. Create RLS policy untuk storage bucket
-- Run di Supabase SQL Editor setelah bucket dibuat:

-- Policy untuk UPLOAD (anon dapat upload)
INSERT INTO storage.policies (name, bucket_id, definition, operation)
VALUES (
  'Allow anon upload',
  'pendaftar-files',
  '(role() = ''anon''::text)',
  'INSERT'
) ON CONFLICT DO NOTHING;

-- Policy untuk READ (public dapat download)
INSERT INTO storage.policies (name, bucket_id, definition, operation)
VALUES (
  'Allow public read',
  'pendaftar-files',
  'true',
  'SELECT'
) ON CONFLICT DO NOTHING;

-- Policy untuk DELETE (service_role dapat delete)
INSERT INTO storage.policies (name, bucket_id, definition, operation)
VALUES (
  'Allow service role delete',
  'pendaftar-files',
  '(role() = ''service_role''::text)',
  'DELETE'
) ON CONFLICT DO NOTHING;

-- =====================================================
-- CARA SETUP DI SUPABASE DASHBOARD:
-- =====================================================
-- 1. Buka Supabase Dashboard
-- 2. Pilih project Anda
-- 3. Klik "Storage" di menu kiri
-- 4. Klik "Create a new bucket"
-- 5. Name: pendaftar-files
-- 6. Public bucket: CENTANG (Yes)
-- 7. Klik "Create bucket"
-- 8. Lalu run SQL ini di SQL Editor
-- =====================================================
