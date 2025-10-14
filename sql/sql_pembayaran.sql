-- ============================================
-- SQL MIGRATION: SISTEM PEMBAYARAN PENDAFTARAN
-- ============================================
-- Tanggal: 14 Oktober 2025
-- Deskripsi: Menambahkan tabel pembayaran untuk tracking pembayaran pendaftaran

-- STEP 0: Cek struktur tabel pendaftar (JALANKAN INI DULU!)
-- ============================================
-- Uncomment dan run query ini untuk melihat struktur tabel pendaftar:
-- SELECT column_name, data_type 
-- FROM information_schema.columns 
-- WHERE table_name = 'pendaftar';

-- STEP 1: Buat tabel pembayaran (TANPA FOREIGN KEY dulu)
-- ============================================
CREATE TABLE IF NOT EXISTS pembayaran (
    id SERIAL PRIMARY KEY,
    nomor_pembayaran VARCHAR(50) UNIQUE NOT NULL,
    nomor_registrasi VARCHAR(50) NOT NULL,
    nama_lengkap VARCHAR(255) NOT NULL,
    jumlah DECIMAL(15,2) NOT NULL DEFAULT 500000.00,
    metode_pembayaran VARCHAR(50) DEFAULT 'Transfer Bank BRI',
    bukti_pembayaran TEXT,
    status_pembayaran VARCHAR(20) DEFAULT 'PENDING' CHECK (status_pembayaran IN ('PENDING', 'VERIFIED', 'REJECTED')),
    tanggal_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tanggal_verifikasi TIMESTAMP,
    verified_by VARCHAR(255),
    catatan_admin TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- STEP 1B: Tambahkan FOREIGN KEY (OPSIONAL - skip jika error)
-- ============================================
-- Jika kolom nomor_registrasi ada di tabel pendaftar, uncomment baris ini:
-- ALTER TABLE pembayaran 
-- ADD CONSTRAINT fk_pembayaran_pendaftar 
-- FOREIGN KEY (nomor_registrasi) REFERENCES pendaftar(nomor_registrasi) ON DELETE CASCADE;

-- STEP 2: Buat index untuk performa
-- ============================================
CREATE INDEX IF NOT EXISTS idx_pembayaran_nomor_registrasi ON pembayaran(nomor_registrasi);
CREATE INDEX IF NOT EXISTS idx_pembayaran_status ON pembayaran(status_pembayaran);
CREATE INDEX IF NOT EXISTS idx_pembayaran_tanggal ON pembayaran(tanggal_upload);

-- STEP 3: Buat trigger untuk auto-update updated_at
-- ============================================
CREATE OR REPLACE FUNCTION update_pembayaran_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_pembayaran_timestamp
    BEFORE UPDATE ON pembayaran
    FOR EACH ROW
    EXECUTE FUNCTION update_pembayaran_timestamp();

-- STEP 4: Buat trigger untuk auto-set tanggal_verifikasi
-- ============================================
CREATE OR REPLACE FUNCTION set_pembayaran_verified_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status_pembayaran IN ('VERIFIED', 'REJECTED') AND OLD.status_pembayaran = 'PENDING' THEN
        NEW.tanggal_verifikasi = CURRENT_TIMESTAMP;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_set_pembayaran_verified_timestamp
    BEFORE UPDATE ON pembayaran
    FOR EACH ROW
    EXECUTE FUNCTION set_pembayaran_verified_timestamp();

-- STEP 5: Buat view untuk reporting pembayaran
-- ============================================
CREATE OR REPLACE VIEW v_pembayaran_report AS
SELECT 
    p.nomor_pembayaran,
    p.nomor_registrasi,
    p.nama_lengkap,
    p.jumlah,
    p.metode_pembayaran,
    p.status_pembayaran,
    p.tanggal_upload,
    p.tanggal_verifikasi,
    p.verified_by,
    pd.status as status_pendaftaran,
    pd.tanggal_lahir,
    pd.no_hp,
    CASE 
        WHEN p.status_pembayaran = 'VERIFIED' THEN 'Lunas'
        WHEN p.status_pembayaran = 'PENDING' THEN 'Menunggu Verifikasi'
        WHEN p.status_pembayaran = 'REJECTED' THEN 'Ditolak'
    END as keterangan_status
FROM pembayaran p
LEFT JOIN pendaftar pd ON p.nomor_registrasi = pd.nomor_registrasi
ORDER BY p.tanggal_upload DESC;

-- STEP 6: Buat fungsi untuk generate nomor pembayaran
-- ============================================
CREATE OR REPLACE FUNCTION generate_nomor_pembayaran()
RETURNS VARCHAR(50) AS $$
DECLARE
    new_nomor VARCHAR(50);
    nomor_exists BOOLEAN;
BEGIN
    LOOP
        -- Format: PAY-YYYYMMDD-XXXXX
        new_nomor := 'PAY-' || TO_CHAR(CURRENT_DATE, 'YYYYMMDD') || '-' || 
                     LPAD(FLOOR(RANDOM() * 99999 + 1)::TEXT, 5, '0');
        
        -- Cek apakah nomor sudah ada
        SELECT EXISTS(SELECT 1 FROM pembayaran WHERE nomor_pembayaran = new_nomor) INTO nomor_exists;
        
        -- Jika tidak ada, keluar dari loop
        EXIT WHEN NOT nomor_exists;
    END LOOP;
    
    RETURN new_nomor;
END;
$$ LANGUAGE plpgsql;

-- STEP 7: Insert data konfigurasi pembayaran (opsional - untuk admin setting)
-- ============================================
CREATE TABLE IF NOT EXISTS konfigurasi_pembayaran (
    id SERIAL PRIMARY KEY,
    nama_setting VARCHAR(100) UNIQUE NOT NULL,
    nilai TEXT NOT NULL,
    deskripsi TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default configuration
INSERT INTO konfigurasi_pembayaran (nama_setting, nilai, deskripsi) VALUES
    ('biaya_pendaftaran', '500000', 'Biaya pendaftaran dalam Rupiah'),
    ('bank_nama', 'BRI (Bank Rakyat Indonesia)', 'Nama bank tujuan transfer'),
    ('bank_nomor_rekening', '0012-01-123456-78-9', 'Nomor rekening bank tujuan'),
    ('bank_atas_nama', 'Yayasan Pondok Pesantren', 'Nama pemilik rekening'),
    ('bank_cabang', 'Cabang Utama', 'Nama cabang bank'),
    ('pembayaran_aktif', 'true', 'Status aktif/nonaktif sistem pembayaran')
ON CONFLICT (nama_setting) DO NOTHING;

-- ============================================
-- TESTING QUERIES
-- ============================================

-- Test 1: Generate nomor pembayaran
-- SELECT generate_nomor_pembayaran();

-- Test 2: Insert sample pembayaran
-- INSERT INTO pembayaran (nomor_pembayaran, nomor_registrasi, nama_lengkap, jumlah)
-- VALUES (generate_nomor_pembayaran(), 'REG-20250114-00001', 'Test User', 500000.00);

-- Test 3: View all pembayaran
-- SELECT * FROM v_pembayaran_report;

-- Test 4: Check pembayaran by status
-- SELECT * FROM pembayaran WHERE status_pembayaran = 'PENDING';

-- Test 5: Verify pembayaran (update status)
-- UPDATE pembayaran 
-- SET status_pembayaran = 'VERIFIED', verified_by = 'admin@test.com', catatan_admin = 'Pembayaran telah diverifikasi'
-- WHERE nomor_pembayaran = 'PAY-20250114-12345';

-- ============================================
-- ROLLBACK (jika diperlukan)
-- ============================================
-- DROP VIEW IF EXISTS v_pembayaran_report;
-- DROP TRIGGER IF EXISTS trigger_update_pembayaran_timestamp ON pembayaran;
-- DROP TRIGGER IF EXISTS trigger_set_pembayaran_verified_timestamp ON pembayaran;
-- DROP FUNCTION IF EXISTS update_pembayaran_timestamp();
-- DROP FUNCTION IF EXISTS set_pembayaran_verified_timestamp();
-- DROP FUNCTION IF EXISTS generate_nomor_pembayaran();
-- DROP TABLE IF EXISTS pembayaran CASCADE;
-- DROP TABLE IF EXISTS konfigurasi_pembayaran CASCADE;
