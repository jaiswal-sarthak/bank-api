#!/bin/bash
# Deployment script for Bank Branches API

echo "=========================================="
echo "Bank Branches API - Deployment Script"
echo "=========================================="

# Check if running on Heroku
if [ -n "$DYNO" ]; then
    echo "Detected Heroku environment"
    echo "Loading data..."
    python scripts/load_data.py
    echo "Starting server..."
    uvicorn app.main:app --host 0.0.0.0 --port $PORT
else
    echo "Local deployment"
    echo "Loading data..."
    python scripts/load_data.py
    echo "Starting server..."
    uvicorn app.main:app --host 0.0.0.0 --port 8000
fi

