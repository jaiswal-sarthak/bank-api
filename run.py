"""Run script for Bank Branches API."""
import os
import sys
import subprocess
import uvicorn

def check_database():
    """Check if database exists and has data."""
    db_path = os.path.join(os.path.dirname(__file__), "bank_branches.db")
    if not os.path.exists(db_path):
        print("⚠ Warning: Database not found")
        print("  Please run: python scripts/load_data.py")
        response = input("  Load data now? (y/n): ")
        if response.lower() == 'y':
            try:
                subprocess.check_call([sys.executable, "scripts/load_data.py"])
            except subprocess.CalledProcessError as e:
                print(f"✗ Error loading data: {e}")
                return False
        else:
            print("  Starting server with empty database...")
    return True

def main():
    """Main run function."""
    print("=" * 60)
    print("Bank Branches API - Starting Server")
    print("=" * 60)
    
    # Check database
    check_database()
    
    print("\nStarting server...")
    print("Access the API at:")
    print("  - REST API Docs: http://localhost:8000/docs")
    print("  - GraphQL: http://localhost:8000/graphql")
    print("  - UI: http://localhost:8000/ui")
    print("  - Health: http://localhost:8000/health")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60)
    
    # Start server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()

