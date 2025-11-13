# Indian Bank Branches REST API

A production-ready REST API service for querying Indian bank branches data, built with FastAPI and SQLAlchemy. This API provides endpoints to search and retrieve information about banks and their branches across India.

## Features

- 🚀 **Fast & Modern**: Built with FastAPI for high performance
- 🔍 **Powerful Search**: Search banks and branches with multiple filters
- 📊 **Rich Data**: Complete branch details including IFSC, address, city, district, and state
- 🎯 **RESTful Design**: Clean and intuitive REST API endpoints
- 🔮 **GraphQL API**: GraphQL endpoint with Strawberry for flexible queries
- 🎨 **Enhanced UI**: Interactive web interface for browsing banks and branches
- 📝 **Auto Documentation**: Interactive API docs with Swagger UI
- ✅ **Tested**: Comprehensive test suite with pytest (31+ tests)
- 🔒 **Type Safe**: Full type hints and Pydantic validation
- 🎨 **Clean Code**: Well-structured, documented, and maintainable
- 🐳 **Docker Ready**: Containerized for easy deployment
- ☁️ **Heroku Ready**: Deploy to Heroku with one command

## Data Source

Data is included from the official [Indian Banks repository](https://github.com/Amanskywalker/indian_banks.git) which contains:
- **170 banks**
- **127863 unique branch records** (873 duplicates removed)
- Official IFSC codes, addresses, and locations
- Complete CSV file included in `data/bank_branches.csv` (18 MB)

## Technology Stack

- **Framework**: FastAPI 0.104+
- **GraphQL**: Strawberry GraphQL 0.200+
- **ORM**: SQLAlchemy 2.0+
- **Database**: SQLite
- **Validation**: Pydantic 2.0+
- **Testing**: Pytest 7.4+
- **Server**: Uvicorn 0.24+

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection (for initial data download)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/jaiswal-sarthak/bank-api.git
   cd bank_api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (optional)
   ```bash
   cp .env.example .env
   # Edit .env file if needed
   ```

5. **Load data into database**
   ```bash
   python scripts/load_data.py
   ```
   This will download the latest data from GitHub and populate the database.

6. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```
   
   The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, access the interactive documentation:
- **REST API Docs**: http://localhost:8000/docs
- **GraphQL Playground**: http://localhost:8000/graphql
- **Enhanced UI**: http://localhost:8000/ui
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Root & Health

- `GET /` - API information
- `GET /health` - Health check

### Banks

- `GET /api/banks` - List all banks
  - Query params: `page`, `page_size`, `search`
- `GET /api/banks/{bank_id}` - Get specific bank
- `GET /api/banks/{bank_id}/branches` - Get all branches of a bank
  - Query params: `page`, `page_size`, `city`, `state`

### Branches

- `GET /api/branches` - List all branches with filters
  - Query params: `page`, `page_size`, `bank_name`, `city`, `district`, `state`, `search`
- `GET /api/branches/{ifsc}` - Get branch by IFSC code

### Statistics

- `GET /api/stats` - Get overall statistics

### GraphQL

- `POST /graphql` - GraphQL endpoint
- `GET /graphql` - GraphQL Playground

### UI

- `GET /ui` - Enhanced web interface

## Usage Examples

### Get all banks
```bash
curl http://localhost:8000/api/banks
```

### Search banks by name
```bash
curl http://localhost:8000/api/banks?search=STATE%20BANK
```

### Get specific bank details
```bash
curl http://localhost:8000/api/banks/1
```

### Get branch by IFSC code
```bash
curl http://localhost:8000/api/branches/SBIN0000001
```

### GraphQL Query Example
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

### GraphQL Query via cURL
```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ branches { edges { node { branch ifsc bank { name } } } } }"}'
```

### Access Enhanced UI
Open http://localhost:8000/ui in your browser

### Get branches by bank and city
```bash
curl "http://localhost:8000/api/branches?bank_name=STATE%20BANK%20OF%20INDIA&city=MUMBAI"
```

### Search branches
```bash
curl "http://localhost:8000/api/branches?search=connaught"
```

### Get branches with pagination
```bash
curl "http://localhost:8000/api/branches?page=1&page_size=50"
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

## Project Structure

```
bank_api/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application and routes
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Database configuration
│   ├── crud.py           # Database operations
│   └── config.py         # Application settings
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # Pytest fixtures
│   └── test_api.py       # API test cases
├── scripts/
│   └── load_data.py      # Data loading script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Configuration

Environment variables (optional):

- `APP_NAME`: Application name (default: "Indian Bank Branches API")
- `APP_VERSION`: API version (default: "1.0.0")
- `DATABASE_URL`: Database connection string (default: SQLite)
- `DEBUG`: Debug mode (default: False)

## Deployment

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python scripts/load_data.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t bank-api .
docker run -p 8000:8000 bank-api
```

### Deploying to Heroku

1. Create `Procfile`:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

2. Create `runtime.txt`:
   ```
   python-3.11.0
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku run python scripts/load_data.py
   ```

### Using PostgreSQL (Production)

1. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost/bank_branches
   ```

3. The application will automatically use PostgreSQL

## Performance Considerations

- **Indexing**: IFSC, bank_id, and city fields are indexed for fast queries
- **Pagination**: All list endpoints support pagination (max 100 per page)
- **Batch Loading**: Data is loaded in batches of 1000 for efficiency
- **Connection Pooling**: SQLAlchemy manages database connections efficiently

## Code Quality

- ✅ Type hints throughout the codebase
- ✅ Comprehensive docstrings
- ✅ Input validation with Pydantic
- ✅ Error handling and appropriate HTTP status codes
- ✅ Clean code following PEP 8 guidelines
- ✅ Modular and maintainable structure

## Development Time

**Total Development Time**: Approximately 4-5 hours

- Project setup and structure: 30 minutes
- Database models and schemas: 45 minutes
- CRUD operations: 1 hour
- API endpoints: 1 hour
- Test cases: 1 hour
- Data loading script: 45 minutes
- Documentation: 30 minutes

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

This project is for educational and evaluation purposes. The bank data is sourced from official RBI listings.

## Support

For questions or issues:
- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review test cases for usage examples

## Acknowledgments

- Bank data sourced from [Amanskywalker/indian_banks](https://github.com/Amanskywalker/indian_banks.git)
- Built with FastAPI framework
- Inspired by modern REST API best practices
