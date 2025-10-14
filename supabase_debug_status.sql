-- =====================================================
-- DEBUG: Cek Status Data yang Bermasalah
-- =====================================================

-- 1. CEK semua nilai statusberkas yang ada (termasuk yang aneh)
SELECT 
  statusberkas,
  COUNT(*) as jumlah,
  UPPER(statusberkas) as akan_jadi
FROM pendaftar 
GROUP BY statusberkas
ORDER BY jumlah DESC;

-- 2. CEK apakah ada NULL
SELECT COUNT(*) as jumlah_null
FROM pendaftar 
WHERE statusberkas IS NULL;

-- 3. CEK apakah ada string kosong atau whitespace
SELECT COUNT(*) as jumlah_kosong
FROM pendaftar 
WHERE statusberkas = '' OR TRIM(statusberkas) = '';

-- 4. LIHAT contoh data yang bermasalah
SELECT id, nomorregistrasi, namalengkap, statusberkas, createdat
FROM pendaftar
ORDER BY createdat DESC
LIMIT 10;
