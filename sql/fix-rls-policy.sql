-- ========================================
-- FIX RLS POLICY untuk pendaftar table
-- ========================================

-- Drop existing policies
DROP POLICY IF EXISTS "Allow public insert" ON pendaftar;
DROP POLICY IF EXISTS "Allow service role all" ON pendaftar;

-- Policy 1: Allow INSERT for anon and authenticated (form pendaftaran public)
CREATE POLICY "Allow public insert" 
  ON pendaftar 
  FOR INSERT 
  TO anon, authenticated
  WITH CHECK (true);

-- Policy 2: Allow ALL operations for service_role (admin)
CREATE POLICY "Allow service role all" 
  ON pendaftar 
  FOR ALL 
  TO service_role
  USING (true)
  WITH CHECK (true);

-- Verify policies
SELECT tablename, policyname, permissive, roles, cmd 
FROM pg_policies 
WHERE tablename = 'pendaftar';
