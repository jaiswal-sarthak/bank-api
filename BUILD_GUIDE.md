# 🏗️ Bank Branches API - Complete Build Guide

## Overview

This is a complete, production-ready REST API and GraphQL API for Indian Bank Branches. The project includes:

- ✅ REST API with comprehensive endpoints
- ✅ GraphQL API with Strawberry
- ✅ Enhanced Web UI
- ✅ Test cases (31+ tests)
- ✅ Docker support
- ✅ Heroku deployment ready
- ✅ Clean code with type hints
- ✅ Comprehensive documentation

## Prerequisites

- Python 3.8+
- pip
- (Optional) Docker for containerization
- (Optional) PostgreSQL for production

## Quick Setup

### Option 1: Using Setup Script (Recommended)
```bash
python setup.py
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Load data
python scripts/load_data.py

# 3. Start server
python run.py
```

## Data Files

The project expects `bank_branches.csv` in one of these locations:
- `bank_branches.csv` (root folder)
- `data/bank_branches.csv` (data folder)

### CSV Format
The CSV file should have the following columns:
- `ifsc`: IFSC code (primary key)
- `bank_id`: Bank identifier
- `branch`: Branch name
- `address`: Full address
- `city`: City name
- `district`: District name
- `state`: State name
- `bank_name`: Bank name

## Project Structure

```
bank_api/
├── app/                    # Application code
│   ├── main.py            # FastAPI app with REST and GraphQL routes
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # Database operations
│   ├── database.py        # Database configuration
│   ├── config.py          # Application settings
│   └── graphql_schema.py  # GraphQL schema
│
├── tests/                 # Test suite
│   ├── test_api.py        # API tests
│   └── conftest.py        # Test fixtures
│
├── scripts/               # Utility scripts
│   ├── load_data.py       # Load data from CSV
│   └── load_sample_data.py # Load sample data
│
├── requirements.txt       # Python dependencies
├── setup.py              # Setup script
├── run.py                # Run script
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── Procfile              # Heroku configuration
└── runtime.txt           # Python version for Heroku
```

## API Endpoints

### REST API

#### Banks
- `GET /api/banks` - List all banks (with pagination & search)
- `GET /api/banks/{bank_id}` - Get bank details
- `GET /api/banks/{bank_id}/branches` - Get bank branches

#### Branches
- `GET /api/branches` - List all branches (with filters)
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

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_api.py::TestBanksEndpoints::test_list_banks -v
```

### Test Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

## Deployment

### Docker

#### Build Image
```bash
docker build -t bank-api .
```

#### Run Container
```bash
docker run -p 8000:8000 bank-api
```

### Docker Compose

#### Start Services
```bash
docker-compose up
```

#### Stop Services
```bash
docker-compose down
```

### Heroku

#### Create App
```bash
heroku create bank-api
```

#### Set Environment Variables
```bash
heroku config:set DATABASE_URL=postgresql://...
```

#### Deploy
```bash
git push heroku main
```

#### Load Data
```bash
heroku run python scripts/load_data.py
```

## Configuration

### Environment Variables
- `DATABASE_URL`: Database connection string (default: `sqlite:///./bank_branches.db`)
- `DEBUG`: Debug mode (default: `False`)

### Database Options
- **SQLite**: Default, for development
- **PostgreSQL**: For production (configure in `DATABASE_URL`)

## Troubleshooting

### Data Loading Issues
1. Check if CSV file exists
2. Verify CSV format
3. Check file permissions
4. Review error messages

### Database Issues
1. Delete database file and reload
2. Check database permissions
3. Verify connection string
4. Check database logs

### Port Issues
1. Check if port 8000 is available
2. Change port in configuration
3. Check firewall settings

### Dependency Issues
1. Update pip: `pip install --upgrade pip`
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python version: `python --version`

## Performance

### Optimization Tips
1. Use PostgreSQL for production
2. Enable database indexes
3. Use pagination for large datasets
4. Cache frequently accessed data
5. Use connection pooling

### Database Indexes
The following indexes are created automatically:
- `banks.id` (primary key)
- `branches.ifsc` (primary key)
- `branches.bank_id` (foreign key)
- `branches.city` (for filtering)

## Security

### Best Practices
1. Use environment variables for sensitive data
2. Enable HTTPS in production
3. Implement rate limiting
4. Validate all inputs
5. Use parameterized queries (SQLAlchemy does this)

## Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Statistics
```bash
curl http://localhost:8000/api/stats
```

## Support

For issues or questions:
1. Check the documentation
2. Review test cases
3. Check API examples
4. Verify data files
5. Check error logs

## License

This project is open source and available under the MIT License.

## Credits

- FastAPI: Modern web framework
- SQLAlchemy: ORM for database
- Strawberry: GraphQL library
- Pydantic: Data validation
- Pytest: Testing framework

