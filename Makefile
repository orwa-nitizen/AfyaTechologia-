.PHONY: init-db audit run build docker-up docker-down

init-db:
\tdocker-compose -f docker-compose.prod.yml up -d db
\tsleep 3
\tdocker cp migrations/ db:/migrations
\tdocker exec -i $(shell docker ps -qf "name=db") bash -c "psql -U postgres -d afyadb -f /migrations/001_schema.sql; psql -U postgres -d afyadb -f /migrations/002_rls.sql; psql -U postgres -d afyadb -f /migrations/003_grants.sql;"

audit:
\tpython3 audit_rls.py

run:
\tFLASK_ENV=development python3 app.py

build:
\tdocker build -t afyatech:latest .

docker-up:
\tdocker-compose -f docker-compose.prod.yml up -d --build

docker-down:
\tdocker-compose -f docker-compose.prod.yml down
