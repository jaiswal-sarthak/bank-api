"""GraphQL schema for Bank Branches API using Strawberry."""
from typing import List, Optional
import strawberry
from sqlalchemy.orm import Session
from app import models, crud
from app.database import SessionLocal


@strawberry.type
class BankType:
    """GraphQL type for Bank."""
    id: int
    name: str


@strawberry.type
class BranchType:
    """GraphQL type for Branch."""
    ifsc: str
    branch: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    bank_id: int
    bank: Optional[BankType] = None


@strawberry.type
class BranchEdge:
    """GraphQL edge type for pagination."""
    node: BranchType


@strawberry.type
class BranchesConnection:
    """GraphQL connection type for branches."""
    edges: List[BranchEdge]


@strawberry.type
class Query:
    """GraphQL Query type."""
    
    @strawberry.field
    def branches(
        self,
        bank_name: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> BranchesConnection:
        """Get branches with optional filters."""
        db = SessionLocal()
        try:
            branches = crud.get_branches(
                db,
                skip=offset,
                limit=limit,
                bank_name=bank_name,
                city=city,
                state=state
            )
            
            edges = [
                BranchEdge(
                    node=BranchType(
                        ifsc=branch.ifsc,
                        branch=branch.branch,
                        address=branch.address,
                        city=branch.city,
                        district=branch.district,
                        state=branch.state,
                        bank_id=branch.bank_id,
                        bank=BankType(id=branch.bank.id, name=branch.bank.name) if branch.bank else None
                    )
                )
                for branch in branches
            ]
            
            return BranchesConnection(edges=edges)
        finally:
            db.close()
    
    @strawberry.field
    def banks(self, limit: int = 100, offset: int = 0) -> List[BankType]:
        """Get all banks."""
        db = SessionLocal()
        try:
            banks = crud.get_banks(db, skip=offset, limit=limit)
            return [BankType(id=bank.id, name=bank.name) for bank in banks]
        finally:
            db.close()
    
    @strawberry.field
    def bank(self, bank_id: int) -> Optional[BankType]:
        """Get a specific bank by ID."""
        db = SessionLocal()
        try:
            bank = crud.get_bank(db, bank_id=bank_id)
            if bank:
                return BankType(id=bank.id, name=bank.name)
            return None
        finally:
            db.close()
    
    @strawberry.field
    def branch(self, ifsc: str) -> Optional[BranchType]:
        """Get a specific branch by IFSC."""
        db = SessionLocal()
        try:
            branch = crud.get_branch(db, ifsc=ifsc)
            if branch:
                return BranchType(
                    ifsc=branch.ifsc,
                    branch=branch.branch,
                    address=branch.address,
                    city=branch.city,
                    district=branch.district,
                    state=branch.state,
                    bank_id=branch.bank_id,
                    bank=BankType(id=branch.bank.id, name=branch.bank.name) if branch.bank else None
                )
            return None
        finally:
            db.close()


# Create GraphQL schema
schema = strawberry.Schema(query=Query)

