-- =====================================================
-- STEP 1: Migrasi Data Existing (RUN INI DULU)
-- =====================================================
-- Run script ini dulu untuk update data yang sudah ada

-- 1. DROP CONSTRAINT DULU jika sudah ada (biar bisa update data)
ALTER TABLE pendaftar 
DROP CONSTRAINT IF EXISTS pendaftar_statusberkas_check;

-- 2. Cek data existing
SELECT statusberkas, COUNT(*) as jumlah 
FROM pendaftar 
GROUP BY statusberkas;

-- 3. Update statusberkas yang NULL atau kosong ke PENDING dulu
UPDATE pendaftar 
SET statusberkas = 'PENDING' 
WHERE statusberkas IS NULL OR TRIM(statusberkas) = '';

-- 4. Update semua statusberkas ke UPPERCASE
UPDATE pendaftar 
SET statusberkas = UPPER(TRIM(statusberkas));

-- 5. Update yang tidak sesuai ke PENDING (safety net)
UPDATE pendaftar 
SET statusberkas = 'PENDING'
WHERE statusberkas NOT IN ('PENDING', 'DITERIMA', 'DITOLAK', 'REVISI');

-- 6. Cek hasil update - HARUS semua UPPERCASE
SELECT statusberkas, COUNT(*) as jumlah 
FROM pendaftar 
GROUP BY statusberkas;

-- =====================================================
-- Setelah run ini, lanjut ke supabase_verifikasi_step2.sql
-- =====================================================
