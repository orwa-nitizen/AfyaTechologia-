-- Create roles
DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_role') THEN
    CREATE ROLE app_role NOINHERIT;
  END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'migrations_role') THEN
    CREATE ROLE migrations_role NOINHERIT;
  END IF;
END$$;

-- Grant usage on schema and table privileges for migrations
GRANT USAGE ON SCHEMA public TO migrations_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO migrations_role;

-- For the app role: only connect and usage; application-level access occurs via RLS (example uses DB superuser for now)
GRANT CONNECT ON DATABASE afyadb TO app_role;
GRANT USAGE ON SCHEMA public TO app_role;
-- No blanket table grants for app_role — rely on RLS to restrict rows

-- Ensure future tables get correct grants
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO migrations_role;
