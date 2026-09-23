#!/bin/sh
set -e

export PORT="${PORT:-8080}"

python -c "
import os, socket, time
host = os.environ.get('FASTAPI_DB_HOST', 'localhost')
port = int(os.environ.get('FASTAPI_DB_PORT', '3306'))
for _ in range(30):
    try:
        socket.create_connection((host, port), timeout=2).close()
        break
    except OSError:
        time.sleep(1)
else:
    raise SystemExit(f'Database not reachable at {host}:{port}')
"

exec python run.py
