-- Create custom settings namespace
ALTER SYSTEM SET session_preload_libraries = '';
SELECT pg_reload_conf();

-- Helper function to read current setting safely
CREATE OR REPLACE FUNCTION app.current_setting_text(name TEXT)
RETURNS TEXT LANGUAGE SQL AS $$
  SELECT current_setting(name, true);
$$;

-- Enable RLS on patient
ALTER TABLE public.patient ENABLE ROW LEVEL SECURITY;

-- Policy: allow selects only if tenant matches current_tenant
CREATE POLICY patient_select_policy ON public.patient
  FOR SELECT
  USING (tenant_id = current_setting('app.current_tenant', true));

-- Policy: inserts must include tenant_id equal to current_tenant
CREATE POLICY patient_insert_policy ON public.patient
  FOR INSERT
  WITH CHECK (tenant_id = current_setting('app.current_tenant', true));

-- Policy: updates allowed only if creator or same tenant
CREATE POLICY patient_update_policy ON public.patient
  FOR UPDATE
  USING (tenant_id = current_setting('app.current_tenant', true) AND (created_by = current_setting('app.current_user', true) OR created_by IS NULL))
  WITH CHECK (tenant_id = current_setting('app.current_tenant', true));

-- Deny default: if no policy matches, access is denied by RLS
