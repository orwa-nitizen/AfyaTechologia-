# AfyaTech

AfyaTech is a secure Flask and PostgreSQL application built for healthcare data protection. It uses PostgreSQL Row-Level Security, database permissions, automated RLS audits, and a Docker-based production deployment with Gunicorn and Nginx.

## Features

- Flask web application.
- PostgreSQL database with Row-Level Security.
- Automated audit script for RLS validation.
- GitHub Actions workflow for CI checks.
- Dockerized development and production setup.
- Gunicorn and Nginx for secure deployment.

## Project Structure

```text
afyatech/
├── app.py
├── audit_rls.py
├── deploy.sh
├── Dockerfile
├── docker-compose.prod.yml
├── nginx.conf
├── Makefile
├── requirements.txt
├── .env.example
├── README.md
├── migrations/
│   ├── 001_schema.sql
│   ├── 002_rls.sql
│   └── 003_grants.sql
└── .github/
    └── workflows/
        └── rls-audit.yml
