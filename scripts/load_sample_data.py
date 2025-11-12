"""Script to load sample bank and branch data for testing purposes."""
import sys
import os

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import Base, Bank, Branch


def load_sample_data():
    """Load sample bank and branch data for testing."""
    
    # Create database tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Create a new database session
    db = SessionLocal()
    
    try:
        print("\nLoading sample banks...")
        
        # Sample banks
        banks_data = [
            {"id": 1, "name": "STATE BANK OF INDIA"},
            {"id": 2, "name": "HDFC BANK"},
            {"id": 3, "name": "ICICI BANK"},
            {"id": 4, "name": "AXIS BANK"},
            {"id": 5, "name": "PUNJAB NATIONAL BANK"},
            {"id": 6, "name": "BANK OF BARODA"},
            {"id": 7, "name": "KOTAK MAHINDRA BANK"},
            {"id": 8, "name": "CANARA BANK"},
            {"id": 9, "name": "UNION BANK OF INDIA"},
            {"id": 10, "name": "BANK OF INDIA"}
        ]
        
        for bank_data in banks_data:
            existing_bank = db.query(Bank).filter(Bank.id == bank_data["id"]).first()
            if not existing_bank:
                bank = Bank(**bank_data)
                db.add(bank)
        
        db.commit()
        print(f"Loaded {len(banks_data)} banks")
        
        print("\nLoading sample branches...")
        
        # Sample branches
        branches_data = [
            {
                "ifsc": "SBIN0000001",
                "bank_id": 1,
                "branch": "MUMBAI MAIN",
                "address": "MUMBAI SAMACHAR MARG, FORT, MUMBAI 400001",
                "city": "MUMBAI",
                "district": "MUMBAI",
                "state": "MAHARASHTRA"
            },
            {
                "ifsc": "SBIN0000002",
                "bank_id": 1,
                "branch": "NEW DELHI MAIN",
                "address": "11 SANSAD MARG, NEW DELHI 110001",
                "city": "NEW DELHI",
                "district": "NEW DELHI",
                "state": "DELHI"
            },
            {
                "ifsc": "SBIN0000003",
                "bank_id": 1,
                "branch": "CHENNAI MAIN",
                "address": "NO 125, RAJAJI SALAI, CHENNAI 600001",
                "city": "CHENNAI",
                "district": "CHENNAI",
                "state": "TAMIL NADU"
            },
            {
                "ifsc": "HDFC0000001",
                "bank_id": 2,
                "branch": "RTGS-HO",
                "address": "KAMALA MILLS COMPOUND, SENAPATI BAPAT MARG, LOWER PAREL, MUMBAI 400013",
                "city": "MUMBAI",
                "district": "MUMBAI",
                "state": "MAHARASHTRA"
            },
            {
                "ifsc": "HDFC0000002",
                "bank_id": 2,
                "branch": "CONNAUGHT PLACE",
                "address": "F-10 CONNAUGHT PLACE, NEW DELHI 110001",
                "city": "NEW DELHI",
                "district": "NEW DELHI",
                "state": "DELHI"
            },
            {
                "ifsc": "ICIC0000001",
                "bank_id": 3,
                "branch": "MUMBAI NARIMAN POINT",
                "address": "MITTAL TOWER, B WING, NARIMAN POINT, MUMBAI 400021",
                "city": "MUMBAI",
                "district": "MUMBAI",
                "state": "MAHARASHTRA"
            },
            {
                "ifsc": "ICIC0000002",
                "bank_id": 3,
                "branch": "BANGALORE MG ROAD",
                "address": "BRIGADE TOWERS, MG ROAD, BANGALORE 560001",
                "city": "BANGALORE",
                "district": "BANGALORE URBAN",
                "state": "KARNATAKA"
            },
            {
                "ifsc": "UTIB0000001",
                "bank_id": 4,
                "branch": "MUMBAI MAIN",
                "address": "TULSIANI CHAMBERS, NARIMAN POINT, MUMBAI 400021",
                "city": "MUMBAI",
                "district": "MUMBAI",
                "state": "MAHARASHTRA"
            },
            {
                "ifsc": "PUNB0000001",
                "bank_id": 5,
                "branch": "NEW DELHI MAIN",
                "address": "7 BHIKAIJI CAMA PLACE, NEW DELHI 110066",
                "city": "NEW DELHI",
                "district": "NEW DELHI",
                "state": "DELHI"
            },
            {
                "ifsc": "BARB0000001",
                "bank_id": 6,
                "branch": "VADODARA MAIN",
                "address": "PRODUCTIVITY ROAD, ALKAPURI, VADODARA 390007",
                "city": "VADODARA",
                "district": "VADODARA",
                "state": "GUJARAT"
            },
            {
                "ifsc": "KKBK0000001",
                "bank_id": 7,
                "branch": "MUMBAI BKC",
                "address": "27 BKC, BANDRA KURLA COMPLEX, MUMBAI 400051",
                "city": "MUMBAI",
                "district": "MUMBAI",
                "state": "MAHARASHTRA"
            },
            {
                "ifsc": "CNRB0000001",
                "bank_id": 8,
                "branch": "BANGALORE MAIN",
                "address": "112 JC ROAD, BANGALORE 560002",
                "city": "BANGALORE",
                "district": "BANGALORE URBAN",
                "state": "KARNATAKA"
            },
            {
                "ifsc": "UBIN0000001",
                "bank_id": 9,
                "branch": "MUMBAI FORT",
                "address": "239 VEER NARIMAN ROAD, FORT, MUMBAI 400001",
                "city": "MUMBAI",
                "district": "MUMBAI",
                "state": "MAHARASHTRA"
            },
            {
                "ifsc": "BKID0000001",
                "bank_id": 10,
                "branch": "MUMBAI MAIN",
                "address": "STAR HOUSE, C-5, G BLOCK, BANDRA KURLA COMPLEX, MUMBAI 400051",
                "city": "MUMBAI",
                "district": "MUMBAI",
                "state": "MAHARASHTRA"
            },
            {
                "ifsc": "SBIN0005943",
                "bank_id": 1,
                "branch": "PUNE CAMP",
                "address": "241 MG ROAD, CAMP, PUNE 411001",
                "city": "PUNE",
                "district": "PUNE",
                "state": "MAHARASHTRA"
            }
        ]
        
        for branch_data in branches_data:
            existing_branch = db.query(Branch).filter(Branch.ifsc == branch_data["ifsc"]).first()
            if not existing_branch:
                branch = Branch(**branch_data)
                db.add(branch)
        
        db.commit()
        print(f"Loaded {len(branches_data)} branches")
        
        # Display summary
        total_banks = db.query(Bank).count()
        total_branches = db.query(Branch).count()
        
        print("\n" + "="*50)
        print("Sample data loading completed successfully!")
        print("="*50)
        print(f"Total Banks in database: {total_banks}")
        print(f"Total Branches in database: {total_branches}")
        print("="*50)
        print("\nNote: This is sample data for testing purposes.")
        print("For full data, run: python scripts/load_data.py")
        
    except Exception as e:
        db.rollback()
        print(f"Error loading data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("="*50)
    print("Sample Bank Branches Data Loader")
    print("="*50)
    print("\nThis script will load sample bank branch data")
    print("into the database for testing purposes.\n")
    
    load_sample_data()
    
    print("\nYou can now start the API server using:")
    print("  uvicorn app.main:app --reload")
