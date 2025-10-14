-- ================================================================
-- SOLUSI SEMENTARA: DISABLE RLS 
-- ================================================================
-- Ini untuk testing dulu apakah API berfungsi tanpa RLS
-- Nanti kita bisa enable lagi setelah yakin API sudah OK
-- ================================================================

-- DISABLE RLS untuk table pendaftar
ALTER TABLE pendaftar DISABLE ROW LEVEL SECURITY;

-- Verify RLS status
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' AND tablename = 'pendaftar';

-- Expected result: rowsecurity = false
