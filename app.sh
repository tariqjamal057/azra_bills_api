#!/bin/bash
# Load environment variables from .env file
set -a
source .env
set +a
# Check the ENVIRONMENT variable
if [ "$ENVIRONMENT" = "development" ]; then
    echo "Running application server in development mode"
    poetry run fastapi dev main.py --host 0.0.0.0 --port 8000
else
    echo "Running application server in production mode"
    poetry run fastapi run main.py --host 0.0.0.0 --port 8000
fi