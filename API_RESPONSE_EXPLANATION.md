# 📚 API Response Explanation

## Root Endpoint Response

When you access the root endpoint (`GET /`), you receive this JSON response:

```json
{
  "message": "Welcome to Indian Bank Branches API",
  "version": "1.0.0",
  "docs": "/docs",
  "ui": "/ui",
  "graphql": "Not available (install Rust and strawberry-graphql)",
  "endpoints": {
    "banks": "/api/banks",
    "branches": "/api/branches",
    "health": "/health",
    "ui": "/ui"
  }
}
```

## Field Explanations

### 1. `message`
- **Type**: String
- **Value**: `"Welcome to Indian Bank Branches API"`
- **Description**: Welcome message for the API
- **Purpose**: Identifies the API and greets users

### 2. `version`
- **Type**: String
- **Value**: `"1.0.0"`
- **Description**: API version number
- **Purpose**: Indicates the current version of the API
- **Format**: Semantic versioning (major.minor.patch)

### 3. `docs`
- **Type**: String
- **Value**: `"/docs"`
- **Description**: Path to interactive API documentation
- **Purpose**: Direct link to Swagger UI documentation
- **Access**: `http://localhost:8000/docs`
- **Features**: 
  - Interactive API testing
  - Endpoint documentation
  - Request/response examples
  - Try-it-out functionality

### 4. `ui`
- **Type**: String
- **Value**: `"/ui"`
- **Description**: Path to enhanced web interface
- **Purpose**: Direct link to user-friendly web UI
- **Access**: `http://localhost:8000/ui`
- **Features**:
  - Search branches
  - Filter by bank, city, state
  - GraphQL query executor
  - Statistics dashboard
  - Modern, responsive design

### 5. `graphql`
- **Type**: String
- **Value**: `"Not available (install Rust and strawberry-graphql)"`
- **Description**: GraphQL endpoint status
- **Purpose**: Indicates whether GraphQL is available
- **Status**: 
  - ⚠️ **Not available** (requires Rust installation)
  - ✅ **Available** at `/graphql` (when Rust is installed)
- **Note**: GraphQL is optional - REST API works without it
- **To Enable**: 
  1. Install Rust: https://rustup.rs/
  2. Install Strawberry: `pip install strawberry-graphql[fastapi]`
  3. Restart server
  4. GraphQL will be available at `/graphql`

### 6. `endpoints`
- **Type**: Object
- **Description**: Object containing all available API endpoints
- **Purpose**: Quick reference to all API endpoints
- **Endpoints**:
  - `banks`: `/api/banks` - List all banks
  - `branches`: `/api/branches` - List all branches
  - `health`: `/health` - Health check endpoint
  - `ui`: `/ui` - Enhanced web interface

## API Endpoints Breakdown

### 1. Banks Endpoint (`/api/banks`)
- **Method**: GET
- **Description**: List all banks
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `page_size`: Items per page (default: 50, max: 100)
  - `search`: Search banks by name
- **Example**: 
  ```bash
  GET /api/banks?page=1&page_size=50&search=STATE BANK
  ```
- **Response**: List of banks with ID and name

### 2. Branches Endpoint (`/api/branches`)
- **Method**: GET
- **Description**: List all branches
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `page_size`: Items per page (default: 50, max: 100)
  - `bank_name`: Filter by bank name
  - `city`: Filter by city
  - `district`: Filter by district
  - `state`: Filter by state
  - `search`: Search in branch name, address, or IFSC
- **Example**: 
  ```bash
  GET /api/branches?bank_name=STATE BANK OF INDIA&city=MUMBAI&page=1&page_size=50
  ```
- **Response**: List of branches with bank details

### 3. Health Endpoint (`/health`)
- **Method**: GET
- **Description**: Health check endpoint
- **Purpose**: Check if API is running
- **Example**: 
  ```bash
  GET /health
  ```
- **Response**: 
  ```json
  {
    "status": "healthy",
    "version": "1.0.0"
  }
  ```

### 4. UI Endpoint (`/ui`)
- **Method**: GET
- **Description**: Enhanced web interface
- **Purpose**: User-friendly web UI for browsing banks and branches
- **Access**: Open in browser: `http://localhost:8000/ui`
- **Features**:
  - Search branches
  - Filter by bank, city, state
  - GraphQL query executor
  - Statistics dashboard

## Complete API Structure

### REST API Endpoints

#### Banks
- `GET /api/banks` - List all banks
- `GET /api/banks/{bank_id}` - Get bank details
- `GET /api/banks/{bank_id}/branches` - Get bank branches

#### Branches
- `GET /api/branches` - List all branches
- `GET /api/branches/{ifsc}` - Get branch by IFSC

#### Other
- `GET /` - API information (this endpoint)
- `GET /health` - Health check
- `GET /api/stats` - Statistics
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc
- `GET /ui` - Enhanced UI

### GraphQL API (Optional)
- `POST /graphql` - GraphQL endpoint
- `GET /graphql` - GraphQL Playground

## Usage Examples

### 1. Access Root Endpoint
```bash
curl http://localhost:8000/
```

### 2. Access API Documentation
```bash
# Open in browser
http://localhost:8000/docs
```

### 3. Access Enhanced UI
```bash
# Open in browser
http://localhost:8000/ui
```

### 4. Check Health
```bash
curl http://localhost:8000/health
```

### 5. Get All Banks
```bash
curl http://localhost:8000/api/banks
```

### 6. Get All Branches
```bash
curl http://localhost:8000/api/branches
```

## Response Status Codes

### Success
- `200 OK` - Request successful
- `201 Created` - Resource created (if applicable)

### Client Errors
- `400 Bad Request` - Invalid request
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error

### Server Errors
- `500 Internal Server Error` - Server error

## GraphQL Status

### Current Status
- ⚠️ **Not Available** - Requires Rust installation
- ✅ **REST API Works** - All REST endpoints functional
- ✅ **UI Works** - Enhanced UI fully functional

### To Enable GraphQL
1. **Install Rust**:
   ```bash
   # Windows: Download from https://rustup.rs/
   # Linux/Mac: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

2. **Install Strawberry GraphQL**:
   ```bash
   pip install strawberry-graphql[fastapi]
   ```

3. **Restart Server**:
   ```bash
   python run.py
   ```

4. **Access GraphQL**:
   - GraphQL Playground: `http://localhost:8000/graphql`
   - GraphQL Endpoint: `POST http://localhost:8000/graphql`

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

## API Information

### Version
- **Current Version**: 1.0.0
- **Version Format**: Semantic versioning (major.minor.patch)
- **Version Location**: `app/config.py`

### Documentation
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **Enhanced UI**: `/ui`
- **API Examples**: `API_EXAMPLES.md`

### Features
- ✅ REST API (fully functional)
- ✅ Enhanced UI (fully functional)
- ✅ Interactive documentation (Swagger UI)
- ✅ Health check endpoint
- ✅ Statistics endpoint
- ⚠️ GraphQL (optional, requires Rust)

## Summary

### What This Response Tells You
1. **API Name**: Indian Bank Branches API
2. **API Version**: 1.0.0
3. **Documentation**: Available at `/docs`
4. **UI**: Available at `/ui`
5. **GraphQL**: Not available (optional)
6. **Endpoints**: Quick reference to all endpoints

### What You Can Do
1. **Access Documentation**: Visit `/docs` for interactive API docs
2. **Use UI**: Visit `/ui` for user-friendly interface
3. **Access Endpoints**: Use the endpoints listed in the response
4. **Check Health**: Visit `/health` to check API status
5. **Enable GraphQL**: Install Rust and Strawberry to enable GraphQL

### Next Steps
1. **Explore API**: Visit `/docs` to explore all endpoints
2. **Use UI**: Visit `/ui` to browse banks and branches
3. **Test Endpoints**: Use the endpoints listed in the response
4. **Enable GraphQL**: Install Rust and Strawberry if needed

## Conclusion

This response provides a comprehensive overview of the API:
- ✅ API information
- ✅ Version information
- ✅ Documentation links
- ✅ UI links
- ✅ Endpoint references
- ✅ GraphQL status

**All REST API endpoints are fully functional, even without GraphQL!** 🚀

