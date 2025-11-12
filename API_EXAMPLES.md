# API Usage Examples

Comprehensive examples of how to use the Bank Branches API.

## Base URL

```
http://localhost:8000
```

## Authentication

No authentication required for this API.

---

## Banks Endpoints

### 1. List All Banks

Get a paginated list of all banks.

**Request:**
```bash
curl http://localhost:8000/api/banks
```

**Response:**
```json
[
  {
    "name": "STATE BANK OF INDIA",
    "id": 1
  },
  {
    "name": "HDFC BANK",
    "id": 2
  }
]
```

### 2. Search Banks

Search banks by name (case-insensitive).

**Request:**
```bash
curl "http://localhost:8000/api/banks?search=HDFC"
```

**Response:**
```json
[
  {
    "name": "HDFC BANK",
    "id": 2
  }
]
```

### 3. Paginate Banks

Control pagination with page and page_size parameters.

**Request:**
```bash
curl "http://localhost:8000/api/banks?page=1&page_size=5"
```

### 4. Get Specific Bank

Get details of a specific bank by ID.

**Request:**
```bash
curl http://localhost:8000/api/banks/1
```

**Response:**
```json
{
  "name": "STATE BANK OF INDIA",
  "id": 1
}
```

### 5. Get Bank's Branches

Get all branches of a specific bank.

**Request:**
```bash
curl http://localhost:8000/api/banks/1/branches
```

**Response:**
```json
[
  {
    "ifsc": "SBIN0000001",
    "branch": "MUMBAI MAIN",
    "address": "MUMBAI SAMACHAR MARG, FORT, MUMBAI 400001",
    "city": "MUMBAI",
    "district": "MUMBAI",
    "state": "MAHARASHTRA",
    "bank_id": 1
  }
]
```

### 6. Filter Bank Branches by City

**Request:**
```bash
curl "http://localhost:8000/api/banks/1/branches?city=MUMBAI"
```

---

## Branches Endpoints

### 1. List All Branches

Get a paginated list of all branches with bank details.

**Request:**
```bash
curl http://localhost:8000/api/branches
```

**Response:**
```json
[
  {
    "ifsc": "SBIN0000001",
    "branch": "MUMBAI MAIN",
    "address": "MUMBAI SAMACHAR MARG, FORT, MUMBAI 400001",
    "city": "MUMBAI",
    "district": "MUMBAI",
    "state": "MAHARASHTRA",
    "bank_id": 1,
    "bank": {
      "name": "STATE BANK OF INDIA",
      "id": 1
    }
  }
]
```

### 2. Get Branch by IFSC Code

Get detailed information about a specific branch.

**Request:**
```bash
curl http://localhost:8000/api/branches/SBIN0000001
```

**Response:**
```json
{
  "ifsc": "SBIN0000001",
  "branch": "MUMBAI MAIN",
  "address": "MUMBAI SAMACHAR MARG, FORT, MUMBAI 400001",
  "city": "MUMBAI",
  "district": "MUMBAI",
  "state": "MAHARASHTRA",
  "bank_id": 1,
  "bank": {
    "name": "STATE BANK OF INDIA",
    "id": 1
  }
}
```

### 3. Filter by Bank Name

Get all branches of a specific bank.

**Request:**
```bash
curl "http://localhost:8000/api/branches?bank_name=STATE%20BANK%20OF%20INDIA"
```

### 4. Filter by City

Get all branches in a specific city.

**Request:**
```bash
curl "http://localhost:8000/api/branches?city=MUMBAI"
```

### 5. Filter by Multiple Parameters

Combine multiple filters for precise results.

**Request:**
```bash
curl "http://localhost:8000/api/branches?bank_name=STATE%20BANK%20OF%20INDIA&city=MUMBAI&state=MAHARASHTRA"
```

### 6. Filter by State

Get all branches in a specific state.

**Request:**
```bash
curl "http://localhost:8000/api/branches?state=MAHARASHTRA"
```

### 7. Filter by District

Get all branches in a specific district.

**Request:**
```bash
curl "http://localhost:8000/api/branches?district=MUMBAI"
```

### 8. Search Branches

Search across branch name, address, and IFSC code.

**Request:**
```bash
curl "http://localhost:8000/api/branches?search=nariman"
```

### 9. Paginate Results

Control the number of results per page.

**Request:**
```bash
curl "http://localhost:8000/api/branches?page=1&page_size=10"
```

---

## Statistics Endpoint

### Get API Statistics

Get overall statistics about the database.

**Request:**
```bash
curl http://localhost:8000/api/stats
```

**Response:**
```json
{
  "total_banks": 10,
  "total_branches": 15
}
```

---

## Python Examples

### Using requests library

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Get all banks
response = requests.get(f"{BASE_URL}/api/banks")
banks = response.json()
print(f"Found {len(banks)} banks")

# Search for a specific bank
response = requests.get(f"{BASE_URL}/api/banks", params={"search": "HDFC"})
hdfc_banks = response.json()

# Get branch by IFSC
ifsc = "SBIN0000001"
response = requests.get(f"{BASE_URL}/api/branches/{ifsc}")
branch = response.json()
print(f"Branch: {branch['branch']}, City: {branch['city']}")

# Filter branches by bank and city
params = {
    "bank_name": "STATE BANK OF INDIA",
    "city": "MUMBAI"
}
response = requests.get(f"{BASE_URL}/api/branches", params=params)
branches = response.json()
print(f"Found {len(branches)} SBI branches in Mumbai")
```

---

## JavaScript/Node.js Examples

### Using fetch API

```javascript
const BASE_URL = 'http://localhost:8000';

// Get all banks
async function getAllBanks() {
  const response = await fetch(`${BASE_URL}/api/banks`);
  const banks = await response.json();
  console.log(`Found ${banks.length} banks`);
  return banks;
}

// Get branch by IFSC
async function getBranchByIFSC(ifsc) {
  const response = await fetch(`${BASE_URL}/api/branches/${ifsc}`);
  const branch = await response.json();
  console.log(`Branch: ${branch.branch}, City: ${branch.city}`);
  return branch;
}

// Filter branches
async function filterBranches(bankName, city) {
  const params = new URLSearchParams({
    bank_name: bankName,
    city: city
  });
  const response = await fetch(`${BASE_URL}/api/branches?${params}`);
  const branches = await response.json();
  return branches;
}

// Usage
getAllBanks();
getBranchByIFSC('SBIN0000001');
filterBranches('STATE BANK OF INDIA', 'MUMBAI');
```

---

## Error Handling

### 404 - Not Found

**Request:**
```bash
curl http://localhost:8000/api/branches/INVALID000
```

**Response:**
```json
{
  "detail": "Branch not found"
}
```

### 400 - Bad Request

**Request:**
```bash
curl http://localhost:8000/api/branches/SHORT
```

**Response:**
```json
{
  "detail": "IFSC code must be exactly 11 characters"
}
```

### 422 - Validation Error

**Request:**
```bash
curl "http://localhost:8000/api/banks?page=0"
```

**Response:**
```json
{
  "detail": [
    {
      "loc": ["query", "page"],
      "msg": "ensure this value is greater than or equal to 1",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

---

## Best Practices

1. **Use Pagination**: Always use pagination for large result sets
   ```bash
   curl "http://localhost:8000/api/branches?page=1&page_size=50"
   ```

2. **Case-Insensitive Search**: All search and filter parameters are case-insensitive
   ```bash
   # These are equivalent:
   curl "http://localhost:8000/api/branches?city=mumbai"
   curl "http://localhost:8000/api/branches?city=MUMBAI"
   ```

3. **Combine Filters**: Use multiple filters for precise results
   ```bash
   curl "http://localhost:8000/api/branches?bank_name=HDFC&city=MUMBAI&page_size=10"
   ```

4. **URL Encoding**: Remember to encode special characters in URLs
   ```bash
   # Spaces should be %20 or +
   curl "http://localhost:8000/api/branches?bank_name=STATE%20BANK%20OF%20INDIA"
   ```

5. **Error Handling**: Always check response status codes and handle errors
   ```python
   response = requests.get(f"{BASE_URL}/api/branches/{ifsc}")
   if response.status_code == 200:
       branch = response.json()
   elif response.status_code == 404:
       print("Branch not found")
   else:
       print(f"Error: {response.status_code}")
   ```

---

## Rate Limiting

Currently, there are no rate limits on this API. However, please use responsibly:
- Use pagination to avoid fetching too much data at once
- Cache responses when appropriate
- Avoid unnecessary repeated requests

---

## Interactive Documentation

For interactive API testing, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Try out API endpoints directly from your browser
- See request/response examples
- View detailed parameter descriptions
- Test different query combinations
