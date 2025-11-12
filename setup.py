"""Setup script for Bank Branches API."""
import os
import sys
import subprocess

def install_dependencies():
    """Install Python dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def load_data():
    """Load data into database."""
    print("\nLoading data into database...")
    try:
        subprocess.check_call([sys.executable, "scripts/load_data.py"])
        print("✓ Data loaded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error loading data: {e}")
        return False

def main():
    """Main setup function."""
    print("=" * 60)
    print("Bank Branches API - Setup")
    print("=" * 60)
    
    # Check if CSV file exists
    csv_path = os.path.join(os.path.dirname(__file__), "bank_branches.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), "data", "bank_branches.csv")
        if not os.path.exists(csv_path):
            print("⚠ Warning: bank_branches.csv not found")
            print("  Please ensure the CSV file is in the project root or data/ folder")
            response = input("  Continue anyway? (y/n): ")
            if response.lower() != 'y':
                print("Setup cancelled")
                return
    
    # Install dependencies
    if not install_dependencies():
        print("Setup failed: Could not install dependencies")
        return
    
    # Load data
    response = input("\nLoad data into database? (y/n): ")
    if response.lower() == 'y':
        if not load_data():
            print("⚠ Warning: Data loading failed")
            print("  You can load data later using: python scripts/load_data.py")
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nTo start the server, run:")
    print("  uvicorn app.main:app --reload")
    print("\nOr use the run script:")
    print("  python run.py")
    print("\nAccess the API at:")
    print("  - REST API Docs: http://localhost:8000/docs")
    print("  - GraphQL: http://localhost:8000/graphql")
    print("  - UI: http://localhost:8000/ui")

if __name__ == "__main__":
    main()

