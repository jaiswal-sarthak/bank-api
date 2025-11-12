"""Comprehensive test cases for the Bank Branches API."""
import pytest


class TestRootEndpoints:
    """Test root and health endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
        # GraphQL is optional, so we just check if it's in the response (or check if it's not available)
        assert "ui" in data
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestBanksEndpoints:
    """Test bank-related endpoints."""
    
    def test_list_banks_empty(self, client):
        """Test listing banks when database is empty."""
        response = client.get("/api/banks")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_banks(self, client, sample_banks):
        """Test listing all banks."""
        response = client.get("/api/banks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["name"] == "STATE BANK OF INDIA"
    
    def test_list_banks_with_pagination(self, client, sample_banks):
        """Test bank listing with pagination."""
        response = client.get("/api/banks?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_list_banks_with_search(self, client, sample_banks):
        """Test bank listing with search filter."""
        response = client.get("/api/banks?search=HDFC")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "HDFC BANK"
    
    def test_get_bank_by_id(self, client, sample_banks):
        """Test retrieving a specific bank by ID."""
        response = client.get("/api/banks/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "STATE BANK OF INDIA"
    
    def test_get_bank_not_found(self, client, sample_banks):
        """Test retrieving a non-existent bank."""
        response = client.get("/api/banks/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Bank not found"
    
    def test_get_bank_branches(self, client, sample_banks, sample_branches):
        """Test retrieving branches of a specific bank."""
        response = client.get("/api/banks/1/branches")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2  # SBI has 2 branches in sample data
        assert all(branch["bank_id"] == 1 for branch in data)
    
    def test_get_bank_branches_with_city_filter(self, client, sample_banks, sample_branches):
        """Test retrieving bank branches filtered by city."""
        response = client.get("/api/banks/1/branches?city=MUMBAI")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["city"] == "MUMBAI"
    
    def test_get_bank_branches_pagination(self, client, sample_banks, sample_branches):
        """Test bank branches with pagination."""
        response = client.get("/api/banks/1/branches?page=1&page_size=1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
    
    def test_get_bank_branches_invalid_bank(self, client, sample_banks, sample_branches):
        """Test retrieving branches of non-existent bank."""
        response = client.get("/api/banks/999/branches")
        assert response.status_code == 404


class TestBranchesEndpoints:
    """Test branch-related endpoints."""
    
    def test_list_branches_empty(self, client, sample_banks):
        """Test listing branches when none exist."""
        response = client.get("/api/branches")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_branches(self, client, sample_banks, sample_branches):
        """Test listing all branches."""
        response = client.get("/api/branches")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4
        assert "bank" in data[0]
    
    def test_list_branches_with_pagination(self, client, sample_banks, sample_branches):
        """Test branch listing with pagination."""
        response = client.get("/api/branches?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_list_branches_filter_by_bank(self, client, sample_banks, sample_branches):
        """Test filtering branches by bank name."""
        response = client.get("/api/branches?bank_name=STATE BANK OF INDIA")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(branch["bank"]["name"] == "STATE BANK OF INDIA" for branch in data)
    
    def test_list_branches_filter_by_city(self, client, sample_banks, sample_branches):
        """Test filtering branches by city."""
        response = client.get("/api/branches?city=MUMBAI")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(branch["city"] == "MUMBAI" for branch in data)
    
    def test_list_branches_filter_by_state(self, client, sample_banks, sample_branches):
        """Test filtering branches by state."""
        response = client.get("/api/branches?state=DELHI")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["state"] == "DELHI"
    
    def test_list_branches_multiple_filters(self, client, sample_banks, sample_branches):
        """Test filtering branches with multiple parameters."""
        response = client.get("/api/branches?bank_name=STATE BANK OF INDIA&city=MUMBAI")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["bank"]["name"] == "STATE BANK OF INDIA"
        assert data[0]["city"] == "MUMBAI"
    
    def test_list_branches_with_search(self, client, sample_banks, sample_branches):
        """Test searching branches by name or address."""
        response = client.get("/api/branches?search=NARIMAN")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "NARIMAN POINT" in data[0]["branch"]
    
    def test_get_branch_by_ifsc(self, client, sample_banks, sample_branches):
        """Test retrieving a branch by IFSC code."""
        response = client.get("/api/branches/SBIN0000001")
        assert response.status_code == 200
        data = response.json()
        assert data["ifsc"] == "SBIN0000001"
        assert data["branch"] == "MUMBAI MAIN"
        assert "bank" in data
        assert data["bank"]["name"] == "STATE BANK OF INDIA"
    
    def test_get_branch_by_ifsc_case_insensitive(self, client, sample_banks, sample_branches):
        """Test IFSC code is case-insensitive."""
        response = client.get("/api/branches/sbin0000001")
        assert response.status_code == 200
        data = response.json()
        assert data["ifsc"] == "SBIN0000001"
    
    def test_get_branch_not_found(self, client, sample_banks, sample_branches):
        """Test retrieving non-existent branch."""
        response = client.get("/api/branches/XXXX0000000")
        assert response.status_code == 404
        assert response.json()["detail"] == "Branch not found"
    
    def test_get_branch_invalid_ifsc_length(self, client, sample_banks, sample_branches):
        """Test IFSC code validation."""
        response = client.get("/api/branches/SHORT")
        assert response.status_code == 400
        assert "11 characters" in response.json()["detail"]


class TestStatisticsEndpoint:
    """Test statistics endpoint."""
    
    def test_get_statistics_empty(self, client):
        """Test statistics with empty database."""
        response = client.get("/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_banks"] == 0
        assert data["total_branches"] == 0
    
    def test_get_statistics(self, client, sample_banks, sample_branches):
        """Test statistics with data."""
        response = client.get("/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_banks"] == 3
        assert data["total_branches"] == 4


class TestCaseInsensitivity:
    """Test case-insensitive search functionality."""
    
    def test_bank_search_case_insensitive(self, client, sample_banks):
        """Test bank search is case-insensitive."""
        response1 = client.get("/api/banks?search=hdfc")
        response2 = client.get("/api/banks?search=HDFC")
        response3 = client.get("/api/banks?search=Hdfc")
        
        assert response1.json() == response2.json() == response3.json()
    
    def test_city_filter_case_insensitive(self, client, sample_banks, sample_branches):
        """Test city filter is case-insensitive."""
        response1 = client.get("/api/branches?city=mumbai")
        response2 = client.get("/api/branches?city=MUMBAI")
        response3 = client.get("/api/branches?city=Mumbai")
        
        assert len(response1.json()) == len(response2.json()) == len(response3.json())


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_invalid_page_number(self, client, sample_banks):
        """Test invalid page number."""
        response = client.get("/api/banks?page=0")
        assert response.status_code == 422  # Validation error
    
    def test_invalid_page_size(self, client, sample_banks):
        """Test invalid page size."""
        response = client.get("/api/banks?page_size=101")
        assert response.status_code == 422  # Validation error
    
    def test_large_page_number(self, client, sample_banks):
        """Test large page number returns empty list."""
        response = client.get("/api/banks?page=1000")
        assert response.status_code == 200
        assert response.json() == []
