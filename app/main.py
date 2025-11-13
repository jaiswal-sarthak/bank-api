"""Main FastAPI application with REST API and GraphQL endpoints."""
from fastapi import FastAPI, Depends, HTTPException, Query
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse
import csv
from io import StringIO
from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud, models, schemas
from app.database import engine, get_db, SessionLocal
from app.config import settings

# Try to import GraphQL (optional - REST API works without it)
try:
    import importlib
    strawberry_fastapi = importlib.import_module("strawberry.fastapi")
    GraphQLRouter = getattr(strawberry_fastapi, "GraphQLRouter")
    from app.graphql_schema import schema
    GRAPHQL_AVAILABLE = True
except Exception:
    GRAPHQL_AVAILABLE = False
    print("Warning: GraphQL not available. REST API will work without GraphQL.")
    print("To enable GraphQL, install Rust and run: pip install 'strawberry-graphql[fastapi]'")

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="REST API and GraphQL API for Indian Bank Branches - Search and retrieve bank and branch information",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add GraphQL endpoint (if available)
if GRAPHQL_AVAILABLE:
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Check if database is empty and load data if needed. Print helpful URLs on startup."""
    import sys
    from pathlib import Path
    
    # Check if database has data
    db = SessionLocal()
    try:
        bank_count = db.query(models.Bank).count()
        if bank_count == 0:
            print("⚠️  Database is empty. Loading bank data from CSV...")
            db.close()
            
            # Load data from scripts
            script_path = Path(__file__).parent.parent / "scripts" / "load_data.py"
            if script_path.exists():
                import subprocess
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    cwd=Path(__file__).parent.parent,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print("✓ Data loaded successfully!")
                else:
                    print(f"⚠️  Data loading failed: {result.stderr}")
            else:
                print(f"⚠️  Load script not found at {script_path}")
    finally:
        db.close()
    
    # Print helpful URLs
    host = os.environ.get("HOST", "127.0.0.1")
    port = os.environ.get("PORT", "8000")
    print(f"UI available at: http://{host}:{port}/ui")
    print(f"REST docs: http://{host}:{port}/docs    ReDoc: http://{host}:{port}/redoc")
    if GRAPHQL_AVAILABLE:
        print(f"GraphQL playground available at: http://{host}:{port}/graphql")
    else:
        print("GraphQL not enabled. Install 'strawberry-graphql[fastapi]' to enable GraphQL playground.")


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint providing API information.
    
    Returns:
        dict: API information including name, version, and available endpoints
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "ui": "/ui",
        "graphql": "/graphql" if GRAPHQL_AVAILABLE else "Not available (install Rust and strawberry-graphql)",
        "endpoints": {
            "banks": "/api/banks",
            "branches": "/api/branches",
            "health": "/health",
            "ui": "/ui"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status of the API
    """
    return {"status": "healthy", "version": settings.app_version}


@app.get("/api/banks", response_model=List[schemas.Bank], tags=["Banks"])
async def list_banks(
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    page_size: int = Query(50, ge=1, le=100, description="Number of items per page"),
    search: Optional[str] = Query(None, description="Search banks by name"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of all banks.
    
    Parameters:
        - **page**: Page number (minimum 1)
        - **page_size**: Number of items per page (1-100)
        - **search**: Optional search term to filter banks by name
        
    Returns:
        List of banks with their details
    """
    skip = (page - 1) * page_size
    banks = crud.get_banks(db, skip=skip, limit=page_size, search=search)
    return banks


@app.get("/api/banks/{bank_id}", response_model=schemas.Bank, tags=["Banks"])
async def get_bank(
    bank_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve details of a specific bank by ID.
    
    Parameters:
        - **bank_id**: Unique identifier of the bank
        
    Returns:
        Bank details
        
    Raises:
        HTTPException: 404 if bank not found
    """
    bank = crud.get_bank(db, bank_id=bank_id)
    if bank is None:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank


@app.get("/api/banks/{bank_id}/branches", response_model=List[schemas.Branch], tags=["Banks"])
async def get_bank_branches(
    bank_id: int,
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    page_size: int = Query(50, ge=0, le=1000, description="Number of items per page (0 = all, max 1000)"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all branches of a specific bank.
    
    Parameters:
        - **bank_id**: Unique identifier of the bank
        - **page**: Page number (minimum 1)
        - **page_size**: Number of items per page (1-100)
        - **city**: Optional filter by city
        - **state**: Optional filter by state
        
    Returns:
        List of branches for the specified bank
        
    Raises:
        HTTPException: 404 if bank not found
    """
    # Check if bank exists
    bank = crud.get_bank(db, bank_id=bank_id)
    if bank is None:
        raise HTTPException(status_code=404, detail="Bank not found")
    
    # interpret page_size == 0 as no limit (return all matching)
    if page_size == 0:
        skip = 0
        limit = None
    else:
        skip = (page - 1) * page_size
        limit = page_size

    branches = crud.get_branches(
        db,
        skip=skip,
        limit=limit,
        bank_id=bank_id,
        city=city,
        state=state
    )
    return branches


@app.get("/api/branches", response_model=List[schemas.BranchWithBank], tags=["Branches"])
async def list_branches(
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    page_size: int = Query(50, ge=0, le=1000, description="Number of items per page (0 = all, max 1000)"),
    bank_id: Optional[int] = Query(None, description="Filter by bank ID"),
    bank_name: Optional[str] = Query(None, description="Filter by bank name"),
    city: Optional[str] = Query(None, description="Filter by city"),
    district: Optional[str] = Query(None, description="Filter by district"),
    state: Optional[str] = Query(None, description="Filter by state"),
    search: Optional[str] = Query(None, description="Search in branch name, address, or IFSC"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a paginated list of branches with optional filters.
    
    Parameters:
        - **page**: Page number (minimum 1)
        - **page_size**: Number of items per page (1-100)
        - **bank_name**: Optional filter by bank name (case-insensitive)
        - **city**: Optional filter by city (case-insensitive)
        - **district**: Optional filter by district (case-insensitive)
        - **state**: Optional filter by state (case-insensitive)
        - **search**: Optional search term for branch name, address, or IFSC
        
    Returns:
        List of branches with bank details
        
    Example:
        - Get all branches: `/api/branches`
        - Filter by bank and city: `/api/branches?bank_name=STATE BANK OF INDIA&city=MUMBAI`
        - Search branches: `/api/branches?search=connaught`
    """
    # If page_size is 0, return all matching results (ignore page)
    if page_size == 0:
        skip = 0
        limit = None
    else:
        skip = (page - 1) * page_size
        limit = page_size

    branches = crud.get_branches(
        db,
        skip=skip,
        limit=limit,
        bank_id=bank_id,
        bank_name=bank_name,
        city=city,
        district=district,
        state=state,
        search=search
    )
    return branches


@app.get("/api/branches/count", tags=["Branches"])
async def branches_count(
    bank_id: Optional[int] = Query(None, description="Filter by bank ID"),
    bank_name: Optional[str] = Query(None, description="Filter by bank name"),
    city: Optional[str] = Query(None, description="Filter by city"),
    district: Optional[str] = Query(None, description="Filter by district"),
    state: Optional[str] = Query(None, description="Filter by state"),
    search: Optional[str] = Query(None, description="Search in branch name, address, or IFSC"),
    db: Session = Depends(get_db)
):
    """Return count of branches matching filters."""
    try:
        cnt = crud.get_branches_count(
            db,
            bank_id=bank_id,
            bank_name=bank_name,
            city=city,
            district=district,
            state=state,
            search=search
        )
        return {"count": int(cnt or 0)}
    except Exception as e:
        # Return a friendly 400 with message if something's wrong with parameters
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/branches/export", tags=["Branches"])
def export_branches_csv(
    bank_id: Optional[int] = Query(None, description="Filter by bank ID"),
    bank_name: Optional[str] = Query(None, description="Filter by bank name"),
    city: Optional[str] = Query(None, description="Filter by city"),
    district: Optional[str] = Query(None, description="Filter by district"),
    state: Optional[str] = Query(None, description="Filter by state"),
    search: Optional[str] = Query(None, description="Search in branch name, address, or IFSC"),
    db: Session = Depends(get_db)
):
    """Stream CSV export of branches matching filters."""

    def row_generator():
        # Header
        header = ['ifsc','bank_id','bank_name','branch','address','city','district','state']
        sio = StringIO()
        writer = csv.writer(sio)
        writer.writerow(header)
        yield sio.getvalue()
        sio.seek(0)
        sio.truncate(0)

        # Fetch all matching rows in batches to avoid loading entire table
        batch_size = 1000
        offset = 0
        while True:
            rows = crud.get_branches(
                db,
                skip=offset,
                limit=batch_size,
                bank_id=bank_id,
                bank_name=bank_name,
                city=city,
                district=district,
                state=state,
                search=search
            )
            if not rows:
                break
            for r in rows:
                # r.bank may be lazy-loaded; ensure name available
                bankname = getattr(r.bank, 'name', '') if r.bank is not None else ''
                writer.writerow([
                    r.ifsc,
                    r.bank_id,
                    bankname,
                    r.branch or '',
                    r.address or '',
                    r.city or '',
                    r.district or '',
                    r.state or ''
                ])
                yield sio.getvalue()
                sio.seek(0)
                sio.truncate(0)

            if len(rows) < batch_size:
                break
            offset += batch_size

    filename = "branches_export.csv"
    return StreamingResponse(row_generator(), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})


@app.get("/api/branches/{ifsc}", response_model=schemas.BranchWithBank, tags=["Branches"])
async def get_branch(
    ifsc: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve details of a specific branch by IFSC code.
    
    Parameters:
        - **ifsc**: IFSC code of the branch (case-insensitive, 11 characters)
        
    Returns:
        Branch details including bank information
        
    Raises:
        HTTPException: 404 if branch not found
        
    Example:
        - Get branch by IFSC: `/api/branches/SBIN0000001`
    """
    if len(ifsc) != 11:
        raise HTTPException(
            status_code=400, 
            detail="IFSC code must be exactly 11 characters"
        )
    
    branch = crud.get_branch(db, ifsc=ifsc)
    if branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch


@app.get("/api/stats", tags=["Statistics"])
async def get_statistics(db: Session = Depends(get_db)):
    """
    Get overall statistics about banks and branches.
    
    Returns:
        Statistics including total banks and branches
    """
    total_banks = crud.get_banks_count(db)
    total_branches = crud.get_branches_count(db)
    
    return {
        "total_banks": total_banks,
        "total_branches": total_branches
    }


@app.get("/ui", response_class=HTMLResponse, tags=["UI"])
async def ui_page():
    """
    Enhanced UI page for browsing banks and branches.
    
    Returns:
        HTML page with interactive UI
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bank Branches API - Enhanced UI</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .header p {
                font-size: 1.2em;
                opacity: 0.9;
            }
            .tabs {
                display: flex;
                background: #f5f5f5;
                border-bottom: 2px solid #ddd;
            }
            .tab {
                flex: 1;
                padding: 20px;
                text-align: center;
                cursor: pointer;
                background: #f5f5f5;
                border: none;
                font-size: 1.1em;
                transition: all 0.3s;
            }
            .tab:hover {
                background: #e0e0e0;
            }
            .tab.active {
                background: white;
                border-bottom: 3px solid #667eea;
                font-weight: bold;
            }
            .content {
                padding: 30px;
            }
            .tab-content {
                display: none;
            }
            .tab-content.active {
                display: block;
            }
            .search-box {
                margin-bottom: 20px;
                padding: 15px;
                border: 2px solid #ddd;
                border-radius: 10px;
                font-size: 1.1em;
                width: 100%;
                transition: border-color 0.3s;
            }
            .search-box:focus {
                outline: none;
                border-color: #667eea;
            }
            .filters {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }
            .filter-input {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 1em;
            }
            .filter-input:focus {
                outline: none;
                border-color: #667eea;
            }
            .btn {
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 1.1em;
                cursor: pointer;
                transition: transform 0.2s;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .back-btn {
                padding: 10px 16px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                font-size: 0.95em;
            }
            .back-btn:hover {
                background: #5568d3;
            }
            .stats-header {
                padding: 15px 0;
                margin-bottom: 20px;
                border-bottom: 1px solid #ddd;
            }
            .results {
                margin-top: 30px;
            }
            .result-item {
                background: #f9f9f9;
                padding: 20px;
                margin-bottom: 15px;
                border-radius: 10px;
                border-left: 4px solid #667eea;
                transition: transform 0.2s;
            }
            .result-item:hover {
                transform: translateX(5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .result-item h3 {
                color: #667eea;
                margin-bottom: 10px;
            }
            .result-item p {
                margin: 5px 0;
                color: #666;
            }
            .loading {
                text-align: center;
                padding: 40px;
                font-size: 1.2em;
                color: #666;
            }
            .error {
                background: #ffebee;
                color: #c62828;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                cursor: pointer;
            }
            .stat-card h3 {
                font-size: 2em;
                margin-bottom: 10px;
            }
            .stat-card p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            .pagination {
                display: flex;
                justify-content: center;
                gap: 10px;
                margin-top: 20px;
            }
            .page-btn {
                padding: 10px 20px;
                background: #f5f5f5;
                border: 2px solid #ddd;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s;
            }
            .page-btn:hover {
                background: #667eea;
                color: white;
                border-color: #667eea;
            }
            .page-btn.active {
                background: #667eea;
                color: white;
                border-color: #667eea;
            }
            .api-links {
                display: flex;
                gap: 15px;
                margin-top: 20px;
                flex-wrap: wrap;
            }
            .api-link {
                padding: 10px 20px;
                background: #f5f5f5;
                border-radius: 8px;
                text-decoration: none;
                color: #667eea;
                transition: all 0.3s;
            }
            .api-link:hover {
                background: #667eea;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏦 Bank Branches API</h1>
                <p>Search and explore Indian bank branches</p>
            </div>
            <div class="tabs">
                <button class="tab active" onclick="switchTab('rest')">REST API</button>
                <button class="tab" onclick="switchTab('graphql')">GraphQL</button>
                <button class="tab" onclick="switchTab('stats')">Statistics</button>
            </div>
            <div class="content">
                <div id="rest" class="tab-content active">
                    <h2>Search Branches</h2>
                    <input type="text" class="search-box" id="searchInput" placeholder="Search by branch name, IFSC, or address...">
                    <div class="filters">
                        <input type="number" class="filter-input" id="bankIdFilter" placeholder="Bank ID (numeric)">
                        <input type="text" class="filter-input" id="bankFilter" placeholder="Bank Name">
                        <input type="text" class="filter-input" id="cityFilter" placeholder="City">
                        <input type="text" class="filter-input" id="stateFilter" placeholder="State">
                        <label style="display:flex; align-items:center; gap:8px;">
                            <input type="checkbox" id="showAllCheckbox"> <span style="font-size:0.9em;">Show all results</span>
                        </label>
                        <button class="btn" onclick="searchBranches()">Search</button>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; gap:20px; margin-top:12px;">
                        <div id="resultInfo" style="color:#333; font-weight:600;">&nbsp;</div>
                        <div style="display:flex; gap:10px;">
                            <button class="btn" id="downloadCsvBtn" onclick="downloadCSV()" disabled>Download CSV</button>
                        </div>
                    </div>
                    <div id="restResults" class="results"></div>
                    <div class="pagination" id="restPagination"></div>
                </div>
                <div id="graphql" class="tab-content">
                    <h2>GraphQL Query</h2>
                    <textarea class="search-box" id="graphqlQuery" rows="10" style="font-family: monospace;">query {
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
}</textarea>
                    <button class="btn" onclick="executeGraphQL()">Execute Query</button>
                    <div id="graphqlResults" class="results"></div>
                </div>
                <div id="stats" class="tab-content">
                    <div class="stats" id="statsContainer"></div>
                </div>
            </div>
            <div style="padding: 20px; background: #f5f5f5; text-align: center;">
                <p>API Endpoints:</p>
                <div class="api-links">
                    <a href="/docs" class="api-link" target="_blank">REST API Docs</a>
                    <a href="/graphql" class="api-link" target="_blank">GraphQL Playground</a>
                    <a href="/redoc" class="api-link" target="_blank">ReDoc</a>
                    <a href="/api/stats" class="api-link" target="_blank">Stats API</a>
                </div>
            </div>
        </div>
        <script>
            let currentPage = 1;
            const defaultPageSize = 20;
            let lastResults = [];
            
            function switchTab(tabName) {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
                event.target.classList.add('active');
                document.getElementById(tabName).classList.add('active');
                
                if (tabName === 'stats') {
                    loadStats();
                }
            }
            
            async function searchBranches() {
                const search = document.getElementById('searchInput').value;
                const bankId = document.getElementById('bankIdFilter').value;
                const bank = document.getElementById('bankFilter').value;
                const city = document.getElementById('cityFilter').value;
                const state = document.getElementById('stateFilter').value;
                const showAll = document.getElementById('showAllCheckbox').checked;
                // If showAll is checked, request page_size=0 which our API interprets as "all"
                const pageSize = showAll ? 0 : defaultPageSize;
                let url = `/api/branches?page=${currentPage}&page_size=${pageSize}`;
                if (search) url += `&search=${encodeURIComponent(search)}`;
                if (bankId) url += `&bank_id=${encodeURIComponent(bankId)}`;
                if (bank) url += `&bank_name=${encodeURIComponent(bank)}`;
                if (city) url += `&city=${encodeURIComponent(city)}`;
                if (state) url += `&state=${encodeURIComponent(state)}`;
                
                document.getElementById('restResults').innerHTML = '<div class="loading">Loading...</div>';
                
                try {
                    const response = await fetch(url);
                        const data = await response.json();
                        lastResults = data || [];
                        // update resultInfo via count endpoint when possible
                        try {
                            const params = new URLSearchParams();
                            if (bankId) params.append('bank_id', bankId);
                            if (bank) params.append('bank_name', bank);
                            if (city) params.append('city', city);
                            if (state) params.append('state', state);
                            if (search) params.append('search', search);
                            const countResp = await fetch('/api/branches/count?' + params.toString());
                            const countData = await countResp.json();
                            const total = (countData && typeof countData.count === 'number') ? countData.count : ((lastResults && lastResults.length) || 0);
                            const resultInfoEl = document.getElementById('resultInfo');
                            if (resultInfoEl) resultInfoEl.innerText = `${total} branches found`;
                        } catch (e) {
                            const total = (lastResults && lastResults.length) || 0;
                            const resultInfoEl = document.getElementById('resultInfo');
                            if (resultInfoEl) resultInfoEl.innerText = `${total} results`;
                        }
                        displayResults(data);
                        const downloadBtn = document.getElementById('downloadCsvBtn');
                        if (downloadBtn) downloadBtn.disabled = !(lastResults && lastResults.length > 0);
                } catch (error) {
                    document.getElementById('restResults').innerHTML = `<div class="error">Error: ${error.message}</div>`;
                }
            }
            
            function displayResults(branches) {
                const container = document.getElementById('restResults');
                if (branches.length === 0) {
                    container.innerHTML = '<div class="loading">No branches found</div>';
                    return;
                }
                
                container.innerHTML = branches.map(branch => `
                    <div class="result-item">
                        <h3>${branch.branch || branch.ifsc}</h3>
                        <p><strong>IFSC:</strong> ${branch.ifsc}</p>
                        <p><strong>Bank:</strong> ${branch.bank.name}</p>
                        <p><strong>Address:</strong> ${branch.address || 'N/A'}</p>
                        <p><strong>City:</strong> ${branch.city || 'N/A'}</p>
                        <p><strong>State:</strong> ${branch.state || 'N/A'}</p>
                    </div>
                `).join('');
            }

            // Download CSV via server exporter using current filters
            function downloadCSV() {
                const search = document.getElementById('searchInput').value;
                const bankId = document.getElementById('bankIdFilter').value;
                const bank = document.getElementById('bankFilter').value;
                const city = document.getElementById('cityFilter').value;
                const state = document.getElementById('stateFilter').value;
                const params = new URLSearchParams();
                if (bankId) params.append('bank_id', bankId);
                if (bank) params.append('bank_name', bank);
                if (city) params.append('city', city);
                if (state) params.append('state', state);
                if (search) params.append('search', search);
                // open export URL - browser will download
                const url = '/api/branches/export?' + params.toString();
                window.location = url;
            }

            let statsPageData = null;  // Track pagination state

            function reloadStats() {
                statsPageData = null;
                loadStats();
            }

            // Show all banks (paginated client-side to collect all)
            async function showBanks() {
                // switch to stats tab and render into statsContainer
                try {
                    switchTab('stats');
                } catch (e) {}
                const container = document.getElementById('statsContainer');
                container.innerHTML = '<div class="stats-header"><button class="back-btn" onclick="reloadStats()">← Back</button></div><div class="loading">Loading banks...</div>';
                let page = 1;
                const page_size = 100;
                let all = [];
                while (true) {
                    const resp = await fetch(`/api/banks?page=${page}&page_size=${page_size}`);
                    const data = await resp.json();
                    if (!data || data.length === 0) break;
                    all = all.concat(data);
                    if (data.length < page_size) break;
                    page += 1;
                }
                lastResults = all;
                const downloadBtn = document.getElementById('downloadCsvBtn');
                if (downloadBtn) downloadBtn.disabled = !(lastResults && lastResults.length > 0);
                container.innerHTML = `<div class="stats-header"><button class="back-btn" onclick="reloadStats()">← Back</button></div><div class="results">${all.map(b => `<div class="result-item"><h3>${b.name}</h3><p>ID: ${b.id}</p></div>`).join('')}</div>`;
            }

            // Show all branches - paginated lazy-loading for performance
            async function showBranches() {
                try {
                    switchTab('stats');
                } catch (e) {}
                
                const container = document.getElementById('statsContainer');
                container.innerHTML = '<div class="stats-header"><button class="back-btn" onclick="reloadStats()">← Back</button></div><div class="loading">Loading branches...</div>';
                
                try {
                    // get count with filters currently set in the UI
                    const params = new URLSearchParams();
                    const search = document.getElementById('searchInput').value;
                    const bankId = document.getElementById('bankIdFilter').value;
                    const bank = document.getElementById('bankFilter').value;
                    const city = document.getElementById('cityFilter').value;
                    const state = document.getElementById('stateFilter').value;
                    if (bankId) params.append('bank_id', bankId);
                    if (bank) params.append('bank_name', bank);
                    if (city) params.append('city', city);
                    if (state) params.append('state', state);
                    if (search) params.append('search', search);
                    
                    const respCount = await fetch('/api/branches/count?' + params.toString());
                    const countData = await respCount.json();
                    const total = (countData && typeof countData.count === 'number') ? countData.count : 0;
                    
                    if (total > 5000) {
                        if (!confirm(`There are ${total} branches. This may take a moment. Proceed?`)) {
                            reloadStats();
                            return;
                        }
                    }

                    // Lazy-load branches using pagination 
                    statsPageData = {
                        params: params,
                        currentPage: 1,
                        pageSize: 500,  // larger page size for faster loading
                        total: total,
                        loaded: 0,
                        branches: []
                    };
                    
                    container.innerHTML = `<div class="stats-header"><button class="back-btn" onclick="reloadStats()">← Back</button></div><div class="results" id="branchList" style=""></div><div id="loadMoreContainer" style="text-align:center; padding:20px;"><button class="btn" onclick="loadMoreBranches()">Load More</button></div>`;
                    
                    await loadMoreBranches();
                } catch (e) {
                    container.innerHTML = `<div class="stats-header"><button class="back-btn" onclick="reloadStats()">← Back</button></div><div class="error">Error: ${(e.message || e)}</div>`;
                }
            }

            async function loadMoreBranches() {
                if (!statsPageData) return;
                
                const container = document.getElementById('branchList');
                const params = new URLSearchParams(statsPageData.params);
                params.append('page', statsPageData.currentPage);
                params.append('page_size', statsPageData.pageSize);
                
                try {
                    const resp = await fetch('/api/branches?' + params.toString());
                    const data = await resp.json();
                    
                    if (!data || data.length === 0) {
                        document.getElementById('loadMoreContainer').innerHTML = `<p style="color:#666;">Loaded all ${statsPageData.loaded} branches ✓</p>`;
                        return;
                    }
                    
                    statsPageData.branches = statsPageData.branches.concat(data);
                    statsPageData.loaded += data.length;
                    statsPageData.currentPage += 1;
                    
                    // Append new results to existing list
                    const newHtml = data.map(b => `<div class="result-item" style="margin-bottom:10px;"><h3>${b.branch || b.ifsc}</h3><p>${(b.bank && b.bank.name) || ''} — ${b.city || ''}, ${b.state || ''}</p></div>`).join('');
                    container.innerHTML += newHtml;
                    
                    lastResults = statsPageData.branches;
                    const downloadBtn = document.getElementById('downloadCsvBtn');
                    if (downloadBtn) downloadBtn.disabled = !(lastResults && lastResults.length > 0);
                    
                    // Update load more button
                    if (statsPageData.loaded >= statsPageData.total) {
                        document.getElementById('loadMoreContainer').innerHTML = `<p style="color:#666;">Loaded all ${statsPageData.total} branches ✓</p>`;
                    } else {
                        document.getElementById('loadMoreContainer').innerHTML = `<button class="btn" onclick="loadMoreBranches()">Load More (${statsPageData.loaded}/${statsPageData.total})</button>`;
                    }
                } catch (e) {
                    document.getElementById('loadMoreContainer').innerHTML = `<div class="error">Error loading more: ${e.message}</div>`;
                }
            }
            
            async function executeGraphQL() {
                const query = document.getElementById('graphqlQuery').value;
                document.getElementById('graphqlResults').innerHTML = '<div class="loading">Executing query...</div>';
                
                try {
                    const response = await fetch('/graphql', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ query }),
                    });
                    const data = await response.json();
                    document.getElementById('graphqlResults').innerHTML = `<pre style="background: #f5f5f5; padding: 20px; border-radius: 8px; overflow-x: auto;">${JSON.stringify(data, null, 2)}</pre>`;
                } catch (error) {
                    document.getElementById('graphqlResults').innerHTML = `<div class="error">Error: ${error.message}</div>`;
                }
            }
            
            async function loadStats() {
                try {
                    const response = await fetch('/api/stats');
                    const data = await response.json();
                    document.getElementById('statsContainer').innerHTML = `
                        <div class="stat-card" onclick="showBanks()">
                            <h3>${data.total_banks}</h3>
                            <p>Total Banks</p>
                        </div>
                        <div class="stat-card" onclick="showBranches()">
                            <h3>${data.total_branches}</h3>
                            <p>Total Branches</p>
                        </div>
                    `;
                } catch (error) {
                    document.getElementById('statsContainer').innerHTML = `<div class="error">Error: ${error.message}</div>`;
                }
            }
            
            // Load initial data
            searchBranches();
            
            // Allow Enter key to search from main search input or bank id input
            ['searchInput','bankIdFilter','bankFilter','cityFilter','stateFilter'].forEach(id => {
                const el = document.getElementById(id);
                if (el) {
                    el.addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') {
                            searchBranches();
                        }
                    });
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
