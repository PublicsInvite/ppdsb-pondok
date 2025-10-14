-- ========================================
-- TABEL: pendaftar
-- ========================================
CREATE TABLE pendaftar (
  id BIGSERIAL PRIMARY KEY,
  
  -- Nomor Registrasi (Auto-generated)
  nomorRegistrasi TEXT UNIQUE NOT NULL,
  
  -- Data Calon Santri
  nikCalon TEXT NOT NULL,
  kkNo TEXT NOT NULL,
  nisn TEXT,
  namaLengkap TEXT NOT NULL,
  tempatLahir TEXT NOT NULL,
  tanggalLahir DATE NOT NULL,
  jenisKelamin CHAR(1) NOT NULL CHECK (jenisKelamin IN ('L', 'P')),
  
  -- Alamat
  alamatJalan TEXT NOT NULL,
  desa TEXT NOT NULL,
  kecamatan TEXT NOT NULL,
  kotaKabupaten TEXT NOT NULL,
  provinsi TEXT NOT NULL,
  
  -- Pendidikan & Rencana
  ijazahFormalTerakhir TEXT NOT NULL,
  rencanaDomisili TEXT NOT NULL,
  rencanaTingkat TEXT NOT NULL,
  rencanaKelas TEXT NOT NULL,
  
  -- Data Orang Tua
  namaAyah TEXT NOT NULL,
  nikAyah TEXT NOT NULL,
  namaIbu TEXT NOT NULL,
  nikIbu TEXT NOT NULL,
  
  -- Status & Timestamps
  statusBerkas TEXT DEFAULT 'MENUNGGU_VERIFIKASI' 
    CHECK (statusBerkas IN ('MENUNGGU_VERIFIKASI', 'DITERIMA', 'DITOLAK')),
  deskripsiStatus TEXT,
  createdAt TIMESTAMPTZ DEFAULT NOW(),
  updatedAt TIMESTAMPTZ DEFAULT NOW()
);

-- ========================================
-- TRIGGER: Auto-generate nomorRegistrasi
-- ========================================
CREATE OR REPLACE FUNCTION generate_nomor_registrasi()
RETURNS TRIGGER AS $$
BEGIN
  NEW.nomorRegistrasi := 'REG-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || LPAD(NEW.id::TEXT, 6, '0');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_generate_nomor_registrasi
  BEFORE INSERT ON pendaftar
  FOR EACH ROW
  EXECUTE FUNCTION generate_nomor_registrasi();

-- ========================================
-- TRIGGER: Auto-update updatedAt
-- ========================================
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updatedAt = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_timestamp
  BEFORE UPDATE ON pendaftar
  FOR EACH ROW
  EXECUTE FUNCTION update_timestamp();

-- ========================================
-- RPC FUNCTION: pendaftar_set_status
-- Untuk mengubah status dengan validasi
-- ========================================
CREATE OR REPLACE FUNCTION pendaftar_set_status(
  p_id BIGINT,
  p_status TEXT,
  p_deskripsi TEXT DEFAULT NULL
)
RETURNS void AS $$
BEGIN
  -- Validasi status
  IF p_status NOT IN ('MENUNGGU_VERIFIKASI', 'DITERIMA', 'DITOLAK') THEN
    RAISE EXCEPTION 'Invalid status: %', p_status;
  END IF;
  
  -- Update status
  UPDATE pendaftar
  SET 
    statusBerkas = p_status,
    deskripsiStatus = p_deskripsi,
    updatedAt = NOW()
  WHERE id = p_id;
  
  -- Cek apakah row ditemukan
  IF NOT FOUND THEN
    RAISE EXCEPTION 'Pendaftar with id % not found', p_id;
  END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ========================================
-- INDEXES untuk performa query
-- ========================================
CREATE INDEX idx_pendaftar_status ON pendaftar(statusBerkas);
CREATE INDEX idx_pendaftar_created_at ON pendaftar(createdAt DESC);
CREATE INDEX idx_pendaftar_nama ON pendaftar(namaLengkap);
CREATE INDEX idx_pendaftar_nomor_reg ON pendaftar(nomorRegistrasi);

-- ========================================
-- ROW LEVEL SECURITY (RLS)
-- ========================================

-- Enable RLS
ALTER TABLE pendaftar ENABLE ROW LEVEL SECURITY;

-- Policy 1: Semua orang bisa INSERT (untuk form pendaftaran public)
CREATE POLICY "Allow public insert" 
  ON pendaftar 
  FOR INSERT 
  TO anon, authenticated
  WITH CHECK (true);

-- Policy 2: Hanya service_role yang bisa SELECT/UPDATE/DELETE (untuk admin)
CREATE POLICY "Allow service role all" 
  ON pendaftar 
  FOR ALL 
  TO service_role
  USING (true)
  WITH CHECK (true);

-- ========================================
-- SAMPLE DATA (Optional - untuk testing)
-- ========================================
-- INSERT INTO pendaftar (
--   nikCalon, kkNo, nisn, namaLengkap, tempatLahir, tanggalLahir, jenisKelamin,
--   alamatJalan, desa, kecamatan, kotaKabupaten, provinsi,
--   ijazahFormalTerakhir, rencanaDomisili, rencanaTingkat, rencanaKelas,
--   namaAyah, nikAyah, namaIbu, nikIbu
-- ) VALUES (
--   '3201234567890123', '3201234567890001', '0012345678', 'Ahmad Fauzi', 
--   'Jakarta', '2008-05-15', 'L',
--   'Jl. Raya Pondok No. 123', 'Ciputat', 'Ciputat Timur', 'Tangerang Selatan', 'Banten',
--   'SMP', 'Mukim', 'MTs', 'Kelas 1',
--   'Budi Santoso', '3201234567890100', 'Siti Aminah', '3201234567890101'
-- );

-- ========================================
-- GRANT PERMISSIONS
-- ========================================
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT SELECT, INSERT ON pendaftar TO anon, authenticated;
GRANT ALL ON pendaftar TO service_role;
GRANT USAGE, SELECT ON SEQUENCE pendaftar_id_seq TO anon, authenticated, service_role;
GRANT EXECUTE ON FUNCTION pendaftar_set_status TO service_role;
