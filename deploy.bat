@echo off
REM Deployment script for Bank Branches API (Windows)

echo ==========================================
echo Bank Branches API - Deployment Script
echo ==========================================

echo Loading data...
python scripts/load_data.py

echo Starting server...
uvicorn app.main:app --host 0.0.0.0 --port 8000

pause

