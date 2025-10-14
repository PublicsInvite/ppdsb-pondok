-- ============================================
-- SQL PEMBAYARAN - VERSI SIMPLE & AMAN
-- ============================================
-- File ini dijamin bisa dijalankan tanpa error
-- Tidak menggunakan FOREIGN KEY agar tidak tergantung struktur tabel lain

-- STEP 1: Buat tabel pembayaran
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

-- STEP 2: Buat index untuk performa
-- ============================================
CREATE INDEX IF NOT EXISTS idx_pembayaran_nomor_registrasi ON pembayaran(nomor_registrasi);
CREATE INDEX IF NOT EXISTS idx_pembayaran_status ON pembayaran(status_pembayaran);
CREATE INDEX IF NOT EXISTS idx_pembayaran_tanggal ON pembayaran(tanggal_upload);
CREATE INDEX IF NOT EXISTS idx_pembayaran_nomor ON pembayaran(nomor_pembayaran);

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

-- STEP 5: Buat fungsi untuk generate nomor pembayaran
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

-- STEP 6: Buat tabel konfigurasi pembayaran
-- ============================================
CREATE TABLE IF NOT EXISTS konfigurasi_pembayaran (
    id SERIAL PRIMARY KEY,
    nama_setting VARCHAR(100) UNIQUE NOT NULL,
    nilai TEXT NOT NULL,
    deskripsi TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- STEP 7: Insert data konfigurasi default
-- ============================================
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

-- Test 1: Cek tabel berhasil dibuat
SELECT table_name FROM information_schema.tables 
WHERE table_name IN ('pembayaran', 'konfigurasi_pembayaran');

-- Test 2: Generate nomor pembayaran
SELECT generate_nomor_pembayaran();

-- Test 3: Insert sample pembayaran
INSERT INTO pembayaran (nomor_pembayaran, nomor_registrasi, nama_lengkap, jumlah)
VALUES (generate_nomor_pembayaran(), 'REG-20251014-00001', 'Test User', 500000.00);

-- Test 4: View pembayaran
SELECT * FROM pembayaran ORDER BY created_at DESC LIMIT 5;

-- Test 5: View konfigurasi
SELECT * FROM konfigurasi_pembayaran;

-- Test 6: Check pembayaran by status
SELECT nomor_pembayaran, nama_lengkap, status_pembayaran, tanggal_upload
FROM pembayaran 
WHERE status_pembayaran = 'PENDING'
ORDER BY tanggal_upload DESC;

-- Test 7: Verify pembayaran (update status)
-- Ganti 'PAY-20251014-12345' dengan nomor pembayaran yang sebenarnya
-- UPDATE pembayaran 
-- SET status_pembayaran = 'VERIFIED', 
--     verified_by = 'admin@test.com', 
--     catatan_admin = 'Pembayaran telah diverifikasi'
-- WHERE nomor_pembayaran = 'PAY-20251014-12345';

-- ============================================
-- CLEANUP / ROLLBACK (jika diperlukan)
-- ============================================
-- Hati-hati! Perintah di bawah akan MENGHAPUS semua data!
-- Uncomment hanya jika benar-benar ingin reset:

-- DROP TRIGGER IF EXISTS trigger_update_pembayaran_timestamp ON pembayaran;
-- DROP TRIGGER IF EXISTS trigger_set_pembayaran_verified_timestamp ON pembayaran;
-- DROP FUNCTION IF EXISTS update_pembayaran_timestamp();
-- DROP FUNCTION IF EXISTS set_pembayaran_verified_timestamp();
-- DROP FUNCTION IF EXISTS generate_nomor_pembayaran();
-- DROP TABLE IF EXISTS pembayaran CASCADE;
-- DROP TABLE IF EXISTS konfigurasi_pembayaran CASCADE;

-- ============================================
-- STRUKTUR TABEL PEMBAYARAN
-- ============================================
/*
Column                | Type          | Nullable | Default
----------------------|---------------|----------|------------------
id                    | integer       | NOT NULL | nextval()
nomor_pembayaran      | varchar(50)   | NOT NULL | -
nomor_registrasi      | varchar(50)   | NOT NULL | -
nama_lengkap          | varchar(255)  | NOT NULL | -
jumlah                | decimal(15,2) | NOT NULL | 500000.00
metode_pembayaran     | varchar(50)   | YES      | 'Transfer Bank BRI'
bukti_pembayaran      | text          | YES      | NULL
status_pembayaran     | varchar(20)   | YES      | 'PENDING'
tanggal_upload        | timestamp     | YES      | CURRENT_TIMESTAMP
tanggal_verifikasi    | timestamp     | YES      | NULL
verified_by           | varchar(255)  | YES      | NULL
catatan_admin         | text          | YES      | NULL
created_at            | timestamp     | YES      | CURRENT_TIMESTAMP
updated_at            | timestamp     | YES      | CURRENT_TIMESTAMP

Constraints:
- PRIMARY KEY: id
- UNIQUE: nomor_pembayaran
- CHECK: status_pembayaran IN ('PENDING', 'VERIFIED', 'REJECTED')

Indexes:
- idx_pembayaran_nomor_registrasi (nomor_registrasi)
- idx_pembayaran_status (status_pembayaran)
- idx_pembayaran_tanggal (tanggal_upload)
- idx_pembayaran_nomor (nomor_pembayaran)

Triggers:
- trigger_update_pembayaran_timestamp: Auto update updated_at
- trigger_set_pembayaran_verified_timestamp: Auto set tanggal_verifikasi
*/
