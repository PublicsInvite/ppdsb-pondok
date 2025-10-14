-- =====================================================
-- SQL untuk Fitur Verifikasi Admin di Supabase
-- =====================================================
-- Copy dan paste script ini di Supabase SQL Editor
-- =====================================================

-- 1. Tambah kolom verifiedat (timestamp verifikasi)
ALTER TABLE pendaftar 
ADD COLUMN IF NOT EXISTS verifiedat TIMESTAMP WITH TIME ZONE;

-- 2. Tambah kolom verifiedby (admin yang verifikasi)
ALTER TABLE pendaftar 
ADD COLUMN IF NOT EXISTS verifiedby VARCHAR(255);

-- 3. Update constraint untuk statusberkas agar include 'revisi'
-- Drop constraint lama jika ada
ALTER TABLE pendaftar 
DROP CONSTRAINT IF EXISTS pendaftar_statusberkas_check;

-- Buat constraint baru dengan status 'revisi'
ALTER TABLE pendaftar 
ADD CONSTRAINT pendaftar_statusberkas_check 
CHECK (statusberkas IN ('PENDING', 'DITERIMA', 'DITOLAK', 'REVISI'));

-- 4. Set default value untuk statusberkas
ALTER TABLE pendaftar 
ALTER COLUMN statusberkas SET DEFAULT 'PENDING';

-- 5. Tambah index untuk performa query
CREATE INDEX IF NOT EXISTS idx_pendaftar_statusberkas ON pendaftar(statusberkas);
CREATE INDEX IF NOT EXISTS idx_pendaftar_verifiedat ON pendaftar(verifiedat);

-- 6. Update RLS policy untuk admin dapat update verifikasi
-- Drop policy lama untuk UPDATE jika ada
DROP POLICY IF EXISTS "Service role can update all" ON pendaftar;

-- Buat policy baru untuk SERVICE_ROLE dapat update
CREATE POLICY "Service role can update all"
ON pendaftar
FOR UPDATE
TO service_role
USING (true)
WITH CHECK (true);

-- 7. Buat function untuk auto-set verifiedat saat status berubah
CREATE OR REPLACE FUNCTION update_verified_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  -- Jika status berubah dari PENDING ke status lain
  IF OLD.statusberkas = 'PENDING' AND NEW.statusberkas IN ('DITERIMA', 'DITOLAK', 'REVISI') THEN
    NEW.verifiedat = NOW();
  END IF;
  
  -- Jika status berubah dari REVISI ke DITERIMA/DITOLAK
  IF OLD.statusberkas = 'REVISI' AND NEW.statusberkas IN ('DITERIMA', 'DITOLAK') THEN
    NEW.verifiedat = NOW();
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 8. Buat trigger untuk auto-update timestamp
DROP TRIGGER IF EXISTS trigger_update_verified_timestamp ON pendaftar;

CREATE TRIGGER trigger_update_verified_timestamp
BEFORE UPDATE ON pendaftar
FOR EACH ROW
EXECUTE FUNCTION update_verified_timestamp();

-- 9. Optional: Buat view untuk laporan verifikasi
CREATE OR REPLACE VIEW v_pendaftar_verifikasi AS
SELECT 
  id,
  nomorregistrasi,
  namalengkap,
  nikcalon,
  statusberkas,
  alasan,
  verifiedat,
  verifiedby,
  createdat,
  CASE 
    WHEN statusberkas = 'PENDING' THEN 'Menunggu Verifikasi'
    WHEN statusberkas = 'REVISI' THEN 'Perlu Revisi'
    WHEN statusberkas = 'DITERIMA' THEN 'Diterima'
    WHEN statusberkas = 'DITOLAK' THEN 'Ditolak'
  END as status_label,
  CASE 
    WHEN verifiedat IS NOT NULL THEN 
      EXTRACT(EPOCH FROM (verifiedat - createdat))/3600 
  END as jam_verifikasi
FROM pendaftar
ORDER BY createdat DESC;

-- 10. Grant akses view ke anon untuk public read
GRANT SELECT ON v_pendaftar_verifikasi TO anon;
GRANT SELECT ON v_pendaftar_verifikasi TO service_role;

-- =====================================================
-- SELESAI!
-- =====================================================
-- Setelah run script ini, table pendaftar akan punya:
-- - verifiedat: timestamp kapan diverifikasi
-- - verifiedby: email admin yang verifikasi
-- - statusberkas: PENDING, REVISI, DITERIMA, DITOLAK
-- - Trigger otomatis set verifiedat saat status berubah
-- =====================================================

-- QUERY UNTUK CEK HASIL:
-- SELECT * FROM pendaftar LIMIT 5;
-- SELECT * FROM v_pendaftar_verifikasi LIMIT 10;
-- \d pendaftar (untuk lihat struktur tabel)
