-- ============================================
-- ALTER TABLE PENDAFTAR
-- Tambah kolom: telepon_orang_tua dan file_bpjs
-- ============================================

-- STEP 1: Tambah kolom telepon_orang_tua
ALTER TABLE pendaftar 
ADD COLUMN IF NOT EXISTS telepon_orang_tua VARCHAR(20);

-- STEP 2: Tambah kolom file_bpjs (URL file dari Supabase Storage)
ALTER TABLE pendaftar 
ADD COLUMN IF NOT EXISTS file_bpjs TEXT;

-- STEP 3: Verify columns added
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'pendaftar' 
AND column_name IN ('telepon_orang_tua', 'file_bpjs');

-- STEP 4: Test insert (optional - uncomment untuk test)
-- UPDATE pendaftar 
-- SET telepon_orang_tua = '081234567890',
--     file_bpjs = 'https://example.com/bpjs.pdf'
-- WHERE id = 1;

-- ============================================
-- ROLLBACK (jika diperlukan)
-- ============================================
-- Uncomment untuk menghapus kolom:
-- ALTER TABLE pendaftar DROP COLUMN IF EXISTS telepon_orang_tua;
-- ALTER TABLE pendaftar DROP COLUMN IF EXISTS file_bpjs;

-- ============================================
-- CATATAN
-- ============================================
/*
Kolom yang ditambahkan:
1. telepon_orang_tua (VARCHAR 20) - Nomor telepon orang tua/wali
2. file_bpjs (TEXT) - URL file BPJS dari Supabase Storage

Format telepon: 081234567890 atau +62812345678
Format file_bpjs: https://[project].supabase.co/storage/v1/object/public/[bucket]/[path]

Data bersifat NULLABLE (boleh kosong) saat ini.
Jika ingin REQUIRED, jalankan:
  ALTER TABLE pendaftar ALTER COLUMN telepon_orang_tua SET NOT NULL;
  ALTER TABLE pendaftar ALTER COLUMN file_bpjs SET NOT NULL;
*/
