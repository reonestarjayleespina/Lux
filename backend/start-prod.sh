#!/bin/bash
# Production startup script for LUX backend
# DO NOT use --reload in production

set -e

# Load environment variables
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

# Start Uvicorn in production mode
uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}" --workers 4
