AfyaTech — Database + RLS security bundle

Overview
This repo contains a Flask app, Postgres schema with Row-Level Security (RLS), an audit script to validate RLS and a CI workflow to run the audit.

Quickstart (local)
1. Copy .env.example to .env and edit if needed.
2. docker-compose -f docker-compose.prod.yml up -d db
3. make init-db
4. make run
5. curl -H "X-Tenant-Id: tenant1" -H "X-User-Id: user:alice" http://localhost:8000/patients

CI
The GitHub Actions workflow will run migrations against a Postgres service and run audit_rls.py; commits that create insecure RLS configurations will fail the workflow.

Security notes
- RLS is the primary row-level control; grant roles are minimal.
- Audit warns on permissive policies (USING/WITH CHECK = true) and on sensitive tables without RLS.
