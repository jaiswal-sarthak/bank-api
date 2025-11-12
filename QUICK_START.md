# ⚡ Bank Branches API - Quick Start

## Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Load Data
```bash
python scripts/load_data.py
```

### Step 3: Start Server
```bash
python run.py
```

### Step 4: Access API
- **REST API Docs**: http://localhost:8000/docs
- **GraphQL**: http://localhost:8000/graphql
- **UI**: http://localhost:8000/ui
- **Health**: http://localhost:8000/health

## That's It! 🎉

You now have a fully functional API running locally.

## Quick Test

### Test REST API
```bash
curl http://localhost:8000/api/banks
```

### Test GraphQL
```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ branches { edges { node { branch ifsc bank { name } } } } }"}'
```

### Test UI
Open http://localhost:8000/ui in your browser

## Common Issues

### Rust Not Found (for GraphQL)
- Install Rust: https://rustup.rs/
- Or use REST API only (GraphQL is optional)

### Port Already in Use
- Change port: `uvicorn app.main:app --port 8001`
- Or kill process using port 8000

### Data File Not Found
- Ensure `bank_branches.csv` is in the root folder
- Or in `data/bank_branches.csv`

## Next Steps

1. **Explore API**: Visit http://localhost:8000/docs
2. **Try GraphQL**: Visit http://localhost:8000/graphql
3. **Use UI**: Visit http://localhost:8000/ui
4. **Run Tests**: `pytest tests/ -v`
5. **Deploy**: See `DEPLOYMENT_GUIDE.md`

## Support

- Documentation: `README.md`
- Setup Guide: `README_SETUP.md`
- Installation Guide: `INSTALLATION_GUIDE.md`
- Deployment Guide: `DEPLOYMENT_GUIDE.md`

## Happy Coding! 🚀

