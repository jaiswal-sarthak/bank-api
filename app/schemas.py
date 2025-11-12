"""Pydantic schemas for request and response validation."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class BankBase(BaseModel):
    """Base schema for Bank."""
    name: str = Field(..., description="Name of the bank", max_length=49)


class BankCreate(BankBase):
    """Schema for creating a new bank."""
    id: int = Field(..., description="Unique identifier for the bank")


class Bank(BankBase):
    """Schema for Bank response."""
    id: int = Field(..., description="Unique identifier for the bank")
    
    model_config = ConfigDict(from_attributes=True)


class BranchBase(BaseModel):
    """Base schema for Branch."""
    ifsc: str = Field(..., description="IFSC code of the branch", max_length=11)
    branch: Optional[str] = Field(None, description="Branch name", max_length=74)
    address: Optional[str] = Field(None, description="Full address of the branch", max_length=195)
    city: Optional[str] = Field(None, description="City name", max_length=50)
    district: Optional[str] = Field(None, description="District name", max_length=50)
    state: Optional[str] = Field(None, description="State name", max_length=26)


class BranchCreate(BranchBase):
    """Schema for creating a new branch."""
    bank_id: int = Field(..., description="Foreign key reference to bank")


class Branch(BranchBase):
    """Schema for Branch response."""
    bank_id: int = Field(..., description="Bank identifier")
    
    model_config = ConfigDict(from_attributes=True)


class BranchWithBank(Branch):
    """Schema for Branch response with bank details."""
    bank: Bank = Field(..., description="Bank details")
    
    model_config = ConfigDict(from_attributes=True)


class BankWithBranches(Bank):
    """Schema for Bank response with all branches."""
    branches: List[Branch] = Field(default=[], description="List of all branches")
    
    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel):
    """Schema for paginated response."""
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of records per page")
    data: List = Field(..., description="List of records")


class ErrorResponse(BaseModel):
    """Schema for error response."""
    detail: str = Field(..., description="Error message")
