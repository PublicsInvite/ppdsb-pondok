-- ============================================
-- ALTER TABLE PENDAFTAR - Rename Column
-- ============================================
-- Ubah nama kolom nomorregistrasi → nomor_registrasi
-- Agar konsisten dengan tabel pembayaran

-- STEP 1: Rename column
ALTER TABLE pendaftar 
RENAME COLUMN nomorregistrasi TO nomor_registrasi;

-- STEP 2: Verify (uncomment untuk test)
-- SELECT column_name, data_type 
-- FROM information_schema.columns 
-- WHERE table_name = 'pendaftar' 
-- AND column_name LIKE '%registrasi%';

-- STEP 3: Check data masih ada
-- SELECT id, nomor_registrasi, nama_lengkap 
-- FROM pendaftar 
-- LIMIT 5;

-- ============================================
-- ROLLBACK (jika ada error)
-- ============================================
-- Jalankan ini jika mau balik ke nomorregistrasi:
-- ALTER TABLE pendaftar 
-- RENAME COLUMN nomor_registrasi TO nomorregistrasi;
