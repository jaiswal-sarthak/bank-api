"""CRUD operations for database models."""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_
from typing import List, Optional
from app import models, schemas


def get_bank(db: Session, bank_id: int) -> Optional[models.Bank]:
    """
    Retrieve a bank by its ID.
    
    Args:
        db: Database session
        bank_id: ID of the bank to retrieve
        
    Returns:
        Bank model instance or None if not found
    """
    return db.query(models.Bank).filter(models.Bank.id == bank_id).first()


def get_bank_by_name(db: Session, bank_name: str) -> Optional[models.Bank]:
    """
    Retrieve a bank by its name (case-insensitive).
    
    Args:
        db: Database session
        bank_name: Name of the bank to retrieve
        
    Returns:
        Bank model instance or None if not found
    """
    return db.query(models.Bank).filter(
        func.lower(models.Bank.name) == bank_name.lower()
    ).first()


def get_banks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None
) -> List[models.Bank]:
    """
    Retrieve list of banks with optional search and pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        search: Optional search term to filter banks by name
        
    Returns:
        List of Bank model instances
    """
    query = db.query(models.Bank)
    
    if search:
        query = query.filter(models.Bank.name.ilike(f"%{search}%"))
    
    return query.offset(skip).limit(limit).all()


def get_banks_count(db: Session, search: Optional[str] = None) -> int:
    """
    Get total count of banks.
    
    Args:
        db: Database session
        search: Optional search term to filter banks by name
        
    Returns:
        Total count of banks
    """
    query = db.query(func.count(models.Bank.id))
    
    if search:
        query = query.filter(models.Bank.name.ilike(f"%{search}%"))
    
    return query.scalar()


def get_branch(db: Session, ifsc: str) -> Optional[models.Branch]:
    """
    Retrieve a branch by its IFSC code.
    
    Args:
        db: Database session
        ifsc: IFSC code of the branch
        
    Returns:
        Branch model instance with bank details or None if not found
    """
    return db.query(models.Branch).options(
        joinedload(models.Branch.bank)
    ).filter(models.Branch.ifsc == ifsc.upper()).first()


def get_branches(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    bank_id: Optional[int] = None,
    bank_name: Optional[str] = None,
    city: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    search: Optional[str] = None
) -> List[models.Branch]:
    """
    Retrieve list of branches with optional filters and pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        bank_id: Optional filter by bank ID
        bank_name: Optional filter by bank name (case-insensitive)
        city: Optional filter by city (case-insensitive)
        district: Optional filter by district (case-insensitive)
        state: Optional filter by state (case-insensitive)
        search: Optional search term to filter branches by name or address
        
    Returns:
        List of Branch model instances with bank details
    """
    query = db.query(models.Branch).options(joinedload(models.Branch.bank))
    
    if bank_id:
        query = query.filter(models.Branch.bank_id == bank_id)
    
    if bank_name:
        query = query.join(models.Bank).filter(
            func.lower(models.Bank.name) == bank_name.lower()
        )
    
    if city:
        query = query.filter(func.lower(models.Branch.city) == city.lower())
    
    if district:
        query = query.filter(func.lower(models.Branch.district) == district.lower())
    
    if state:
        query = query.filter(func.lower(models.Branch.state) == state.lower())
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Branch.branch.ilike(search_term),
                models.Branch.address.ilike(search_term),
                models.Branch.ifsc.ilike(search_term)
            )
        )
    
    return query.offset(skip).limit(limit).all()


def get_branches_count(
    db: Session,
    bank_id: Optional[int] = None,
    bank_name: Optional[str] = None,
    city: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    search: Optional[str] = None
) -> int:
    """
    Get total count of branches with optional filters.
    
    Args:
        db: Database session
        bank_id: Optional filter by bank ID
        bank_name: Optional filter by bank name (case-insensitive)
        city: Optional filter by city (case-insensitive)
        district: Optional filter by district (case-insensitive)
        state: Optional filter by state (case-insensitive)
        search: Optional search term to filter branches
        
    Returns:
        Total count of branches matching the filters
    """
    query = db.query(func.count(models.Branch.ifsc))
    
    if bank_id:
        query = query.filter(models.Branch.bank_id == bank_id)
    
    if bank_name:
        query = query.join(models.Bank).filter(
            func.lower(models.Bank.name) == bank_name.lower()
        )
    
    if city:
        query = query.filter(func.lower(models.Branch.city) == city.lower())
    
    if district:
        query = query.filter(func.lower(models.Branch.district) == district.lower())
    
    if state:
        query = query.filter(func.lower(models.Branch.state) == state.lower())
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Branch.branch.ilike(search_term),
                models.Branch.address.ilike(search_term),
                models.Branch.ifsc.ilike(search_term)
            )
        )
    
    return query.scalar()


def create_bank(db: Session, bank: schemas.BankCreate) -> models.Bank:
    """
    Create a new bank in the database.
    
    Args:
        db: Database session
        bank: Bank data to create
        
    Returns:
        Created Bank model instance
    """
    db_bank = models.Bank(id=bank.id, name=bank.name)
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    return db_bank


def create_branch(db: Session, branch: schemas.BranchCreate) -> models.Branch:
    """
    Create a new branch in the database.
    
    Args:
        db: Database session
        branch: Branch data to create
        
    Returns:
        Created Branch model instance
    """
    db_branch = models.Branch(**branch.dict())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch
