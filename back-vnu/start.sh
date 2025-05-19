#!/bin/sh

echo "🔄 Waiting for PostgreSQL..."
sleep 5

echo "🔍 Checking PostgreSQL connection..."
python3 -c "
import psycopg2, os, time

dsn = os.environ.get('PSQL_DSN')
retries = 5
for i in range(retries):
    try:
        conn = psycopg2.connect(dsn=dsn)
        conn.close()
        print('✅ Connected to PostgreSQL!')
        break
    except Exception as e:
        print(f'❌ Attempt {i+1}/{retries} failed: {e}')
        time.sleep(5)
else:
    print('🚫 PostgreSQL unavailable after retries.')
    exit(1)
"

echo "📥 Running schema from db.sql..."
psql "$PSQL_DSN" -f ./app/db/db.sql

echo "🚀 Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
