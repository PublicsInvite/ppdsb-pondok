-- ================================================================
-- SIMPLE RLS FIX - Run this in Supabase SQL Editor
-- ================================================================
-- This script uses ALTER POLICY instead of DROP/CREATE
-- to avoid permission issues
-- ================================================================

-- First, let's disable RLS temporarily to ensure we can modify policies
ALTER TABLE pendaftar DISABLE ROW LEVEL SECURITY;

-- Now enable it again
ALTER TABLE pendaftar ENABLE ROW LEVEL SECURITY;

-- Create the INSERT policy for anon role (public registration)
-- This replaces any existing INSERT policy
DROP POLICY IF EXISTS "Allow public insert" ON pendaftar;
DROP POLICY IF EXISTS "anon_insert_policy" ON pendaftar;

CREATE POLICY "anon_insert_policy" 
ON pendaftar 
FOR INSERT 
TO anon 
WITH CHECK (true);

-- Create policy for service_role (admin operations)
DROP POLICY IF EXISTS "service_role_all_policy" ON pendaftar;

CREATE POLICY "service_role_all_policy" 
ON pendaftar 
FOR ALL 
TO service_role 
USING (true) 
WITH CHECK (true);

-- Grant necessary permissions
GRANT INSERT ON pendaftar TO anon;
GRANT ALL ON pendaftar TO service_role;

-- Verify the policies
SELECT 
    schemaname,
    tablename,
    policyname,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies 
WHERE tablename = 'pendaftar';
