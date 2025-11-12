"""SQLAlchemy database models."""
from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Bank(Base):
    """
    Bank model representing the banks table.
    
    Attributes:
        id: Unique identifier for the bank
        name: Name of the bank
        branches: Relationship to Branch model
    """
    __tablename__ = "banks"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(49), nullable=False)
    
    # Relationship with branches
    branches = relationship("Branch", back_populates="bank")


class Branch(Base):
    """
    Branch model representing the branches table.
    
    Attributes:
        ifsc: IFSC code (primary key)
        bank_id: Foreign key reference to banks table
        branch: Branch name
        address: Full address of the branch
        city: City name
        district: District name
        state: State name
        bank: Relationship to Bank model
    """
    __tablename__ = "branches"
    
    ifsc = Column(String(11), primary_key=True, index=True)
    bank_id = Column(BigInteger, ForeignKey("banks.id"), nullable=False, index=True)
    branch = Column(String(74))
    address = Column(String(195))
    city = Column(String(50), index=True)
    district = Column(String(50))
    state = Column(String(26))
    
    # Relationship with bank
    bank = relationship("Bank", back_populates="branches")
