#!/usr/bin/env python3
import os
from flask import Flask, g, request, jsonify
import psycopg2
import psycopg2.extras

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/afyadb")
APP_USER = os.getenv("APP_DB_ROLE", "app_role")

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
        g.db.autocommit = True
    return g.db

def set_db_context(user_id=None, tenant_id=None):
    db = get_db()
    cur = db.cursor()
    if user_id is None:
        cur.execute("SET LOCAL app.current_user = NULL;")
    else:
        cur.execute("SET LOCAL app.current_user = %s;", (str(user_id),))
    if tenant_id is None:
        cur.execute("SET LOCAL app.current_tenant = NULL;")
    else:
        cur.execute("SET LOCAL app.current_tenant = %s;", (str(tenant_id),))
    cur.close()

app = Flask(__name__)

@app.teardown_appcontext
def close_db(exc):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/patients", methods=["GET"])
def list_patients():
    user_id = request.headers.get("X-User-Id")
    tenant_id = request.headers.get("X-Tenant-Id")
    set_db_context(user_id=user_id, tenant_id=tenant_id)
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, tenant_id, name, dob FROM patient ORDER BY id LIMIT 100;")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows)

@app.route("/patients", methods=["POST"])
def create_patient():
    payload = request.get_json() or {}
    name = payload.get("name")
    dob = payload.get("dob")
    tenant_id = request.headers.get("X-Tenant-Id")
    user_id = request.headers.get("X-User-Id")
    set_db_context(user_id=user_id, tenant_id=tenant_id)
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO patient (tenant_id, name, dob, created_by) VALUES (%s,%s,%s,%s) RETURNING id;",
                (tenant_id, name, dob, user_id))
    new_id = cur.fetchone()[0]
    cur.close()
    return jsonify({"id": new_id}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=(os.getenv("FLASK_ENV")!="production"))
