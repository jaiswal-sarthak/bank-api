# 📦 Bank Branches API - Installation Guide

## Overview

This guide provides step-by-step instructions for installing and setting up the Bank Branches API.

## Prerequisites

### Required
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)

### Optional
- Docker (for containerization)
- PostgreSQL (for production)
- Rust (for GraphQL support)

## Installation Methods

### Method 1: Standard Installation (Recommended)

#### Step 1: Install Python
```bash
# Check Python version
python --version
# Should be 3.8 or higher

# If not installed, download from https://www.python.org/downloads/
```

#### Step 2: Install Dependencies
```bash
# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Load Data
```bash
# Load data from CSV
python scripts/load_data.py
```

#### Step 4: Start Server
```bash
# Start server
python run.py
```

#### Step 5: Access API
- REST API: http://localhost:8000/docs
- GraphQL: http://localhost:8000/graphql
- UI: http://localhost:8000/ui

### Method 2: Installation Without GraphQL (If Rust is not available)

If you encounter issues with Strawberry (GraphQL) installation due to Rust requirements:

#### Option A: Install Rust (Recommended)
```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Or on Windows, download from https://rustup.rs/

# After installing Rust, install dependencies
pip install -r requirements.txt
```

#### Option B: Use REST API Only (Temporary)
```bash
# Install dependencies without GraphQL
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-dotenv pandas pytest pytest-asyncio httpx aiosqlite jinja2 python-multipart

# Comment out GraphQL imports in app/main.py if needed
# REST API will still work
```

### Method 3: Docker Installation

#### Step 1: Install Docker
```bash
# Install Docker from https://www.docker.com/get-started
```

#### Step 2: Build Image
```bash
docker build -t bank-api .
```

#### Step 3: Run Container
```bash
docker run -p 8000:8000 bank-api
```

#### Step 4: Load Data
```bash
# Load data in container
docker exec -it <container-id> python scripts/load_data.py
```

### Method 4: Virtual Environment (Recommended for Development)

#### Step 1: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

#### Step 2: Install Dependencies
```bash
# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Load Data
```bash
# Load data
python scripts/load_data.py
```

#### Step 4: Start Server
```bash
# Start server
python run.py
```

## Troubleshooting

### Issue 1: Rust Not Found (for GraphQL)

**Error**: `error: metadata-generation-failed` or `Rust not found`

**Solution**:
1. Install Rust: https://rustup.rs/
2. Restart terminal
3. Install dependencies again: `pip install -r requirements.txt`

**Alternative**: Use REST API only (GraphQL is optional)

### Issue 2: Python Version Too Old

**Error**: `Python 3.8 or higher required`

**Solution**:
1. Update Python: https://www.python.org/downloads/
2. Verify version: `python --version`
3. Reinstall dependencies

### Issue 3: pip Not Found

**Error**: `pip: command not found`

**Solution**:
1. Install pip: `python -m ensurepip --upgrade`
2. Or download: https://pip.pypa.io/en/stable/installation/

### Issue 4: Database Connection Error

**Error**: `Database connection failed`

**Solution**:
1. Check `DATABASE_URL` environment variable
2. Verify database is running
3. Check firewall settings
4. Review database logs

### Issue 5: Data Loading Error

**Error**: `Data file not found`

**Solution**:
1. Verify `bank_branches.csv` exists in root folder
2. Check file permissions
3. Review error messages
4. Try loading from `data/bank_branches.csv`

### Issue 6: Port Already in Use

**Error**: `Port 8000 already in use`

**Solution**:
1. Change port: `uvicorn app.main:app --port 8001`
2. Or kill process using port 8000
3. Use environment variable: `PORT=8001`

### Issue 7: Dependency Installation Error

**Error**: `Failed to install dependencies`

**Solution**:
1. Update pip: `pip install --upgrade pip`
2. Check Python version: `python --version`
3. Review error messages
4. Try installing individually: `pip install fastapi`
5. Check internet connection

## Verification

### Test Installation
```bash
# Run test script
python test_setup.py
```

### Test API
```bash
# Start server
python run.py

# In another terminal, test API
curl http://localhost:8000/health
```

### Test GraphQL (if installed)
```bash
# Test GraphQL endpoint
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ banks { id name } }"}'
```

## Configuration

### Environment Variables

Create `.env` file:
```env
DATABASE_URL=sqlite:///./bank_branches.db
DEBUG=False
PORT=8000
```

### Database Configuration

#### SQLite (Default)
- No configuration needed
- Database file: `bank_branches.db`

#### PostgreSQL
```env
DATABASE_URL=postgresql://user:password@host:port/database
```

#### MySQL
```env
DATABASE_URL=mysql://user:password@host:port/database
```

## Next Steps

### 1. Load Data
```bash
python scripts/load_data.py
```

### 2. Start Server
```bash
python run.py
```

### 3. Access API
- REST API: http://localhost:8000/docs
- GraphQL: http://localhost:8000/graphql
- UI: http://localhost:8000/ui

### 4. Run Tests
```bash
pytest tests/ -v
```

### 5. Deploy
See `DEPLOYMENT_GUIDE.md` for deployment instructions.

## Support

### Resources
- Documentation: `README.md`
- Setup Guide: `README_SETUP.md`
- Build Guide: `BUILD_GUIDE.md`
- Deployment Guide: `DEPLOYMENT_GUIDE.md`
- API Examples: `API_EXAMPLES.md`

### Troubleshooting
- Check logs
- Review error messages
- Verify configuration
- Test locally
- Check documentation

## Conclusion

This installation guide provides comprehensive instructions for installing and setting up the Bank Branches API. Follow the steps carefully and refer to troubleshooting section if you encounter issues.

**Happy installing!** 🚀

