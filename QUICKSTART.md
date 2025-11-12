# Quick Start Guide

Get the API running in 5 minutes!

## Prerequisites

- Python 3.8+
- pip

## Setup Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Load Data

#### Option A: Load Full Real Data (INCLUDED - No Download Needed!)
```bash
python scripts/load_data.py
```
This loads **127863 real branch records** from the included CSV file (18 MB).
Takes ~2-3 minutes to complete.

#### Option B: Load Sample Data (Quick Testing)
```bash
python scripts/load_sample_data.py
```
This loads 10 banks and 15 branches for quick testing.

### 3. Start the Server

```bash
uvicorn app.main:app --reload
```

### 4. Test the API

Open your browser and go to:
- **API Docs**: http://localhost:8000/docs
- **Root Endpoint**: http://localhost:8000

## Quick API Test

```bash
# Get all banks
curl http://localhost:8000/api/banks

# Get branch by IFSC
curl http://localhost:8000/api/branches/SBIN0000001

# Search branches by bank and city
curl "http://localhost:8000/api/branches?bank_name=STATE%20BANK%20OF%20INDIA&city=MUMBAI"

# Get statistics
curl http://localhost:8000/api/stats
```

## Run Tests

```bash
pytest tests/ -v
```

## Docker (Alternative)

```bash
# Build
docker build -t bank-api .

# Run
docker run -p 8000:8000 bank-api
```

That's it! 🚀

For detailed documentation, see [README.md](README.md)
