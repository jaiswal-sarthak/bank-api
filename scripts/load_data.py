"""Script to load bank and branch data from local CSV file into the database."""
import sys
import os
import pandas as pd

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import Base, Bank, Branch


def load_data_from_csv():
    """Load bank and branch data from the local CSV file."""
    # Path to the CSV file (included in the project)
    # Try root folder first, then data/ folder
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(root_dir, "bank_branches.csv")
    
    # If not in root, try data folder
    if not os.path.exists(csv_path):
        csv_path = os.path.join(root_dir, "data", "bank_branches.csv")
    
    try:
        # Check if file exists
        if not os.path.exists(csv_path):
            print(f"ERROR: Data file not found at {csv_path}")
            print("\nPlease ensure bank_branches.csv is in the project root or data/ folder")
            sys.exit(1)
        
        # Load the data
        print(f"Loading data from {csv_path}...")
        df = pd.read_csv(
            csv_path,
            on_bad_lines='skip',  # Skip malformed lines
            encoding='utf-8',
            quoting=1,  # QUOTE_ALL
            escapechar='\\'
        )
        print(f"Loaded {len(df)} records from CSV")
        
        # Clean column names (remove any extra spaces)
        df.columns = df.columns.str.strip()
        
        # Remove duplicate IFSCs (keep first occurrence)
        original_count = len(df)
        df = df.drop_duplicates(subset=['ifsc'], keep='first')
        duplicates_removed = original_count - len(df)
        if duplicates_removed > 0:
            print(f"Removed {duplicates_removed} duplicate IFSC codes")
        
        # Create database tables
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # Create a new database session
        db = SessionLocal()
        
        try:
            # Extract unique banks
            print("\nProcessing banks...")
            banks_df = df[['bank_id', 'bank_name']].drop_duplicates()
            banks_df = banks_df.rename(columns={'bank_name': 'name', 'bank_id': 'id'})
            banks_df = banks_df.sort_values('id')
            
            # Prepare bank data for bulk insert
            banks_to_insert = []
            for _, row in banks_df.iterrows():
                banks_to_insert.append({
                    'id': int(row['id']),
                    'name': row['name']
                })
            
            # Bulk insert banks (skip if already exists)
            if banks_to_insert:
                # Check which banks already exist
                existing_bank_ids = {bank.id for bank in db.query(Bank).all()}
                new_banks = [b for b in banks_to_insert if b['id'] not in existing_bank_ids]
                
                if new_banks:
                    db.execute(
                        Bank.__table__.insert(),
                        new_banks
                    )
                    db.commit()
                    print(f"Loaded {len(new_banks)} new banks (skipped {len(banks_to_insert) - len(new_banks)} existing)")
                else:
                    print(f"All {len(banks_to_insert)} banks already exist, skipping...")
            
            # Prepare branch data for bulk insert
            print("\nProcessing branches...")
            print("This may take a few minutes...")
            
            # Check which branches already exist
            existing_ifscs = {branch.ifsc for branch in db.query(Branch).all()}
            print(f"Found {len(existing_ifscs)} existing branches in database")
            
            branches_to_insert = []
            batch_size = 5000
            total_inserted = 0
            skipped = 0
            
            for idx, row in df.iterrows():
                ifsc = row['ifsc']
                
                # Skip if branch already exists
                if ifsc in existing_ifscs:
                    skipped += 1
                    continue
                
                branch_data = {
                    'ifsc': ifsc,
                    'bank_id': int(row['bank_id']),
                    'branch': row['branch'] if pd.notna(row['branch']) else None,
                    'address': row['address'] if pd.notna(row['address']) else None,
                    'city': row['city'] if pd.notna(row['city']) else None,
                    'district': row['district'] if pd.notna(row['district']) else None,
                    'state': row['state'] if pd.notna(row['state']) else None
                }
                branches_to_insert.append(branch_data)
                existing_ifscs.add(ifsc)  # Track inserted IFSC to avoid duplicates in same batch
                
                # Bulk insert when batch is ready
                if len(branches_to_insert) >= batch_size:
                    try:
                        db.execute(
                            Branch.__table__.insert(),
                            branches_to_insert
                        )
                        db.commit()
                        total_inserted += len(branches_to_insert)
                        print(f"Loaded {total_inserted} branches... (skipped {skipped} existing)")
                        branches_to_insert = []
                    except Exception as e:
                        db.rollback()
                        print(f"Error inserting batch: {e}")
                        branches_to_insert = []
            
            # Insert remaining branches
            if branches_to_insert:
                try:
                    db.execute(
                        Branch.__table__.insert(),
                        branches_to_insert
                    )
                    db.commit()
                    total_inserted += len(branches_to_insert)
                except Exception as e:
                    db.rollback()
                    print(f"Error inserting remaining branches: {e}")
            
            print(f"\nTotal branches loaded: {total_inserted}")
            if skipped > 0:
                print(f"Skipped {skipped} existing branches")
            
            # Display summary
            total_banks = db.query(Bank).count()
            total_branches = db.query(Branch).count()
            
            print("\n" + "="*50)
            print("Data loading completed successfully!")
            print("="*50)
            print(f"Total Banks in database: {total_banks}")
            print(f"Total Branches in database: {total_branches}")
            print("="*50)
            
        except Exception as e:
            db.rollback()
            print(f"Error loading data: {e}")
            raise
        finally:
            db.close()
            
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print("="*50)
    print("Bank Branches Data Loader")
    print("="*50)
    print("\nThis script will load bank branch data from the")
    print("included CSV file into the database.\n")
    
    load_data_from_csv()
    
    print("\nYou can now start the API server using:")
    print("  uvicorn app.main:app --reload")
