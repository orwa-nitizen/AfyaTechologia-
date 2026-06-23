CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE IF NOT EXISTS patient (
  id serial PRIMARY KEY,
  tenant_id text NOT NULL,
  name text NOT NULL,
  dob date,
  medical_record text,
  created_at timestamptz DEFAULT now(),
  created_by text
);

CREATE TABLE IF NOT EXISTS rls_audit (
  id serial PRIMARY KEY,
  event_time timestamptz DEFAULT now(),
  role_name text,
  action text,
  object_schema text,
  object_name text,
  statement text
);
