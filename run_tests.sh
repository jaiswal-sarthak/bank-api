#!/bin/bash
# Test runner script for Bank Branches API

echo "=========================================="
echo "Bank Branches API - Test Runner"
echo "=========================================="

echo "Running setup tests..."
python test_setup.py

echo ""
echo "Running API tests..."
pytest tests/ -v

echo ""
echo "Test execution completed!"

