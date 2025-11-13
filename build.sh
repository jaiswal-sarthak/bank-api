#!/bin/bash
# Build script for Render
# This runs before the web server starts

echo "==> Loading bank data from CSV..."
python scripts/load_data.py

echo "==> Data loading complete, ready to start web server"
