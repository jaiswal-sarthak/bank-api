# 🚀 Bank Branches API - Complete Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Load Data
```bash
python scripts/load_data.py
```

### 3. Start Server
```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload
```

### 4. Access the API
- **REST API Docs**: http://localhost:8000/docs
- **GraphQL**: http://localhost:8000/graphql
- **UI**: http://localhost:8000/ui
- **Health Check**: http://localhost:8000/health

## Features

### ✅ REST API
- List all banks
- Get bank details
- Get bank branches
- Search branches
- Filter by city, state, district
- Pagination support

### ✅ GraphQL API
- Query banks and branches
- Filter and pagination
- GraphQL Playground

### ✅ Enhanced UI
- Interactive web interface
- Search and filter branches
- GraphQL query executor
- Statistics dashboard

### ✅ Test Cases
- 31+ comprehensive tests
- Unit and integration tests
- Edge case coverage

### ✅ Deployment Ready
- Docker support
- Heroku ready
- PostgreSQL support

## Data Files

The project uses `bank_branches.csv` from the root folder or `data/bank_branches.csv`.

### CSV Structure
- `ifsc`: IFSC code (primary key)
- `bank_id`: Bank identifier
- `branch`: Branch name
- `address`: Full address
- `city`: City name
- `district`: District name
- `state`: State name
- `bank_name`: Bank name

## API Endpoints

### REST API

#### Banks
- `GET /api/banks` - List all banks
- `GET /api/banks/{bank_id}` - Get bank details
- `GET /api/banks/{bank_id}/branches` - Get bank branches

#### Branches
- `GET /api/branches` - List all branches
- `GET /api/branches/{ifsc}` - Get branch by IFSC

#### Other
- `GET /` - API information
- `GET /health` - Health check
- `GET /api/stats` - Statistics
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc
- `GET /ui` - Enhanced UI

### GraphQL API

#### Endpoint
- `POST /graphql` - GraphQL endpoint
- `GET /graphql` - GraphQL Playground

#### Query Example
```graphql
query {
  branches {
    edges {
      node {
        branch
        ifsc
        city
        bank {
          name
        }
      }
    }
  }
}
```

## Testing

Run tests:
```bash
pytest tests/ -v
```

Run specific test:
```bash
pytest tests/test_api.py::TestBanksEndpoints::test_list_banks -v
```

## Deployment

### Docker
```bash
docker build -t bank-api .
docker run -p 8000:8000 bank-api
```

### Docker Compose
```bash
docker-compose up
```

### Heroku
1. Create Heroku app
2. Set environment variables
3. Deploy:
```bash
git push heroku main
```

## Configuration

### Environment Variables
- `DATABASE_URL`: Database connection string (default: `sqlite:///./bank_branches.db`)
- `DEBUG`: Debug mode (default: `False`)

### Database
- **SQLite**: Default, for development
- **PostgreSQL**: For production (configure in `DATABASE_URL`)

## Troubleshooting

### Data Loading Issues
- Ensure `bank_branches.csv` is in the root folder or `data/` folder
- Check file permissions
- Verify CSV format

### Database Issues
- Delete `bank_branches.db` and reload data
- Check database permissions
- Verify database connection string

### Port Issues
- Change port in `run.py` or `uvicorn` command
- Check if port 8000 is already in use

## Support

For issues or questions:
1. Check the documentation
2. Review test cases
3. Check API examples
4. Verify data files

## License

This project is open source and available under the MIT License.

