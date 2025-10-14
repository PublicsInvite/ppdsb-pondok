-- ========================================
-- SAMPLE TEST DATA for pendaftar table
-- ========================================
-- Use this to populate test data in your Supabase database
-- Run this AFTER running supabase-schema.sql

-- Sample 1: Male student from Jakarta
INSERT INTO pendaftar (
  nikCalon, kkNo, nisn, namaLengkap, tempatLahir, tanggalLahir, jenisKelamin,
  alamatJalan, desa, kecamatan, kotaKabupaten, provinsi,
  ijazahFormalTerakhir, rencanaDomisili, rencanaTingkat, rencanaKelas,
  namaAyah, nikAyah, namaIbu, nikIbu
) VALUES (
  '3101234567890001', '3101234567890011', '0012345678', 'Ahmad Fauzi Rahmat',
  'Jakarta', '2008-03-15', 'L',
  'Jl. Masjid Al-Ikhlas No. 45', 'Kebayoran Baru', 'Kebayoran Baru', 'Jakarta Selatan', 'DKI Jakarta',
  'SMP', 'Mukim', 'MTs', 'Kelas 1',
  'Muhammad Rahmat', '3101234567890100', 'Siti Khadijah', '3101234567890101'
);

-- Sample 2: Female student from Bandung
INSERT INTO pendaftar (
  nikCalon, kkNo, nisn, namaLengkap, tempatLahir, tanggalLahir, jenisKelamin,
  alamatJalan, desa, kecamatan, kotaKabupaten, provinsi,
  ijazahFormalTerakhir, rencanaDomisili, rencanaTingkat, rencanaKelas,
  namaAyah, nikAyah, namaIbu, nikIbu
) VALUES (
  '3201234567890002', '3201234567890012', '0012345679', 'Fatimah Azzahra',
  'Bandung', '2009-07-20', 'P',
  'Jl. Cibaduyut No. 123', 'Cibaduyut', 'Bojongloa Kidul', 'Bandung', 'Jawa Barat',
  'SMP', 'Mukim', 'MTs', 'Kelas 1',
  'Abdullah Malik', '3201234567890200', 'Aminah Binti Ahmad', '3201234567890201'
);

-- Sample 3: Male student from Tangerang (no NISN)
INSERT INTO pendaftar (
  nikCalon, kkNo, nisn, namaLengkap, tempatLahir, tanggalLahir, jenisKelamin,
  alamatJalan, desa, kecamatan, kotaKabupaten, provinsi,
  ijazahFormalTerakhir, rencanaDomisili, rencanaTingkat, rencanaKelas,
  namaAyah, nikAyah, namaIbu, nikIbu
) VALUES (
  '3601234567890003', '3601234567890013', NULL, 'Umar bin Khattab',
  'Tangerang', '2007-12-01', 'L',
  'Jl. Raya Serpong No. 88', 'Serpong', 'Serpong', 'Tangerang Selatan', 'Banten',
  'SMP', 'Pulang Pergi', 'MTs', 'Kelas 2',
  'Khattab bin Nufail', '3601234567890300', 'Hantamah binti Hisyam', '3601234567890301'
);

-- Sample 4: Female student from Bogor
INSERT INTO pendaftar (
  nikCalon, kkNo, nisn, namaLengkap, tempatLahir, tanggalLahir, jenisKelamin,
  alamatJalan, desa, kecamatan, kotaKabupaten, provinsi,
  ijazahFormalTerakhir, rencanaDomisili, rencanaTingkat, rencanaKelas,
  namaAyah, nikAyah, namaIbu, nikIbu
) VALUES (
  '3201234567890004', '3201234567890014', '0012345680', 'Aisyah Rahmawati',
  'Bogor', '2008-11-10', 'P',
  'Jl. Pajajaran No. 56', 'Tegallega', 'Bogor Tengah', 'Bogor', 'Jawa Barat',
  'SD', 'Mukim', 'MTs', 'Kelas 1',
  'Rahman Hakim', '3201234567890400', 'Siti Maryam', '3201234567890401'
);

-- Sample 5: Male student from Depok (High School graduate)
INSERT INTO pendaftar (
  nikCalon, kkNo, nisn, namaLengkap, tempatLahir, tanggalLahir, jenisKelamin,
  alamatJalan, desa, kecamatan, kotaKabupaten, provinsi,
  ijazahFormalTerakhir, rencanaDomisili, rencanaTingkat, rencanaKelas,
  namaAyah, nikAyah, namaIbu, nikIbu
) VALUES (
  '3201234567890005', '3201234567890015', '0012345681', 'Ali bin Abi Thalib',
  'Depok', '2006-06-25', 'L',
  'Jl. Margonda Raya No. 234', 'Kemiri Muka', 'Beji', 'Depok', 'Jawa Barat',
  'SMA', 'Mukim', 'MA', 'Kelas 1',
  'Abu Thalib', '3201234567890500', 'Fatimah binti Asad', '3201234567890501'
);

-- ========================================
-- Update some statuses for variety
-- ========================================

-- Accept first student
UPDATE pendaftar 
SET statusBerkas = 'DITERIMA', 
    deskripsiStatus = 'Memenuhi semua persyaratan dan lulus tes wawancara'
WHERE namaLengkap = 'Ahmad Fauzi Rahmat';

-- Reject one student
UPDATE pendaftar 
SET statusBerkas = 'DITOLAK', 
    deskripsiStatus = 'Usia tidak memenuhi syarat minimal'
WHERE namaLengkap = 'Ali bin Abi Thalib';

-- Leave others as MENUNGGU_VERIFIKASI (default)

-- ========================================
-- Verify inserted data
-- ========================================
SELECT 
  id,
  nomorRegistrasi,
  namaLengkap,
  jenisKelamin,
  kotaKabupaten,
  statusBerkas,
  createdAt
FROM pendaftar
ORDER BY createdAt DESC;
