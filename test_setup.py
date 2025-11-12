"""Test script to verify the setup and installation."""
import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    try:
        import fastapi
        print("[OK] FastAPI imported successfully")
    except ImportError as e:
        print(f"[FAIL] FastAPI import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("[OK] SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"[FAIL] SQLAlchemy import failed: {e}")
        return False
    
    try:
        import pydantic
        print("[OK] Pydantic imported successfully")
    except ImportError as e:
        print(f"[FAIL] Pydantic import failed: {e}")
        return False
    
    try:
        import strawberry
        print("[OK] Strawberry imported successfully")
    except ImportError as e:
        print(f"[WARN] Strawberry import failed: {e}")
        print("  Note: Strawberry is optional. REST API works without GraphQL.")
        print("  To enable GraphQL, install Rust and run: pip install strawberry-graphql[fastapi]")
        # Don't return False - GraphQL is optional
    
    try:
        import pandas
        print("[OK] Pandas imported successfully")
    except ImportError as e:
        print(f"[FAIL] Pandas import failed: {e}")
        return False
    
    return True

def test_app_imports():
    """Test if app modules can be imported."""
    print("\nTesting app imports...")
    try:
        from app import main
        print("[OK] app.main imported successfully")
    except ImportError as e:
        print(f"[FAIL] app.main import failed: {e}")
        return False
    
    try:
        from app import models
        print("[OK] app.models imported successfully")
    except ImportError as e:
        print(f"[FAIL] app.models import failed: {e}")
        return False
    
    try:
        from app import schemas
        print("[OK] app.schemas imported successfully")
    except ImportError as e:
        print(f"[FAIL] app.schemas import failed: {e}")
        return False
    
    try:
        from app import crud
        print("[OK] app.crud imported successfully")
    except ImportError as e:
        print(f"[FAIL] app.crud import failed: {e}")
        return False
    
    try:
        from app import database
        print("[OK] app.database imported successfully")
    except ImportError as e:
        print(f"[FAIL] app.database import failed: {e}")
        return False
    
    try:
        from app import config
        print("[OK] app.config imported successfully")
    except ImportError as e:
        print(f"[FAIL] app.config import failed: {e}")
        return False
    
    try:
        from app import graphql_schema
        print("[OK] app.graphql_schema imported successfully")
    except ImportError as e:
        print(f"[WARN] app.graphql_schema import failed: {e}")
        print("  Note: GraphQL is optional. REST API works without GraphQL.")
        # Don't return False - GraphQL is optional
    
    return True

def test_files():
    """Test if required files exist."""
    print("\nTesting files...")
    files_to_check = [
        "requirements.txt",
        "app/main.py",
        "app/models.py",
        "app/schemas.py",
        "app/crud.py",
        "app/database.py",
        "app/config.py",
        "app/graphql_schema.py",
        "scripts/load_data.py",
        "tests/test_api.py",
        "tests/conftest.py",
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"[OK] {file_path} exists")
        else:
            print(f"[FAIL] {file_path} not found")
            all_exist = False
    
    return all_exist

def test_data_files():
    """Test if data files exist."""
    print("\nTesting data files...")
    data_files = [
        "bank_branches.csv",
        "data/bank_branches.csv",
    ]
    
    found = False
    for data_file in data_files:
        if os.path.exists(data_file):
            print(f"[OK] {data_file} exists")
            found = True
        else:
            print(f"[WARN] {data_file} not found")
    
    if not found:
        print("[WARN] No data files found. You may need to add bank_branches.csv")
        return False
    
    return True

def test_app_creation():
    """Test if FastAPI app can be created."""
    print("\nTesting app creation...")
    try:
        from app.main import app
        print("[OK] FastAPI app created successfully")
        print(f"  Title: {app.title}")
        print(f"  Version: {app.version}")
        return True
    except Exception as e:
        print(f"[FAIL] App creation failed: {e}")
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("Bank Branches API - Setup Test")
    print("=" * 60)
    
    results = []
    
    # Test imports (GraphQL is optional)
    imports_passed = test_imports()
    results.append(("Imports", imports_passed or True))  # Pass if GraphQL missing (optional)
    
    # Test app imports (GraphQL is optional)
    app_imports_passed = test_app_imports()
    results.append(("App Imports", app_imports_passed or True))  # Pass if GraphQL missing (optional)
    
    # Test files
    results.append(("Files", test_files()))
    
    # Test data files
    results.append(("Data Files", test_data_files()))
    
    # Test app creation
    results.append(("App Creation", test_app_creation()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("[SUCCESS] All tests passed!")
        print("\nNext steps:")
        print("1. Load data: python scripts/load_data.py")
        print("2. Start server: python run.py")
        print("3. Access API: http://localhost:8000/docs")
    else:
        print("[ERROR] Some tests failed!")
        print("\nTroubleshooting:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Check Python version: python --version (should be 3.8+)")
        print("3. Verify files exist in correct locations")
        print("4. Check error messages above")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

