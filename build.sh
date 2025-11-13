#!/bin/bash
# Build script for Render
# This runs before the web server starts

echo "==> Setting up database and loading bank data..."
cd /opt/render/project/src

# Create tables and load data
python -c "
import sys
sys.path.insert(0, '.')
from app.database import engine, Base
from app.models import Bank, Branch

# Create all tables
Base.metadata.create_all(bind=engine)
print('✓ Database tables created')
"

# Load data from CSV
python scripts/load_data.py

echo "==> Data loading complete, ready to start web server"
