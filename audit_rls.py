#!/usr/bin/env python3
import os
import sys
import json
import psycopg2
import psycopg2.extras

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/afyadb")

def query(q, args=()):
    with psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor) as conn:
        with conn.cursor() as cur:
            cur.execute(q, args)
            return cur.fetchall()

def main():
    problems = []
    summary = {}
    # 1) tables with sensitive columns
    sensitive_cols_q = """
    select table_schema, table_name, column_name
    from information_schema.columns
    where column_name in ('ssn','medical_record','diagnosis','patient_notes','created_by')
      and table_schema not in ('pg_catalog','information_schema')
    """
    sensitive = query(sensitive_cols_q)
    summary['sensitive_columns'] = sensitive

    # 2) which tables have rls enabled
    rls_q = """
    select schemaname, relname as table_name, relrowsecurity
    from pg_catalog.pg_class c
    join pg_catalog.pg_namespace n on n.oid = c.relnamespace
    where relkind='r' or relkind='p'
      and n.nspname not in ('pg_catalog','information_schema')
    """
    rls = query(rls_q)
    summary['table_rls'] = rls

    # 3) policies
    policies_q = """
    select pol.polname, n.nspname as schema, c.relname as table, pol.polcmd, pol.polpermissive,
           pg_get_expr(pol.polqual, pol.polrelid) as using_expr,
           pg_get_expr(pol.polwithcheck, pol.polrelid) as with_check_expr
    from pg_policy pol
    join pg_class c on pol.polrelid = c.oid
    join pg_namespace n on c.relnamespace = n.oid
    order by n.nspname, c.relname
    """
    policies = query(policies_q)
    summary['policies'] = policies

    # 4) quick checks
    for s in sensitive:
        table = "{}.{}".format(s['table_schema'], s['table_name'])
        match = [r for r in rls if r['schemaname']==s['table_schema'] and r['table_name']==s['table_name']]
        if not match:
            problems.append(f"Sensitive column {s['column_name']} on {table} is on a table without RLS enabled.")
    for p in policies:
        if p['using_expr'] is None and p['with_check_expr'] is None:
            problems.append(f"Policy {p['polname']} on {p['schema']}.{p['table']} has no USING/WITH CHECK expression.")
        if p['using_expr'] and p['using_expr'].strip().lower() in ('true','(true)'):
            problems.append(f"Policy {p['polname']} on {p['schema']}.{p['table']} uses a permissive USING = true.")
        if p['with_check_expr'] and p['with_check_expr'].strip().lower() in ('true','(true)'):
            problems.append(f"Policy {p['polname']} on {p['schema']}.{p['table']} uses a permissive WITH CHECK = true.")

    report = {"summary": summary, "problems": problems}
    print(json.dumps(report, indent=2))
    if problems:
        print("RLS audit FAILED", file=sys.stderr)
        sys.exit(2)
    else:
        print("RLS audit OK")
        sys.exit(0)

if __name__ == "__main__":
    main()
