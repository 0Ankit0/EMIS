"""
API Client for Backend Communication
"""
import requests
import streamlit as st
from typing import Dict, Any, Optional, List
from config.settings import API_BASE_URL, API_TIMEOUT


class APIClient:
    """HTTP client for backend API communication"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = API_TIMEOUT
        self.session = requests.Session()
        
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication token"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Add auth token if available
        if "access_token" in st.session_state:
            headers["Authorization"] = f"Bearer {st.session_state.access_token}"
            
        return headers
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response"""
        try:
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                st.session_state.clear()
                st.error("Session expired. Please login again.")
                st.rerun()
            elif response.status_code == 403:
                st.error("You don't have permission to perform this action.")
            else:
                error_msg = response.json().get("detail", str(e)) if response.content else str(e)
                st.error(f"API Error: {error_msg}")
            raise
        except requests.exceptions.RequestException as e:
            st.error(f"Network Error: {str(e)}")
            raise
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(
            url, 
            params=params, 
            headers=self._get_headers(),
            timeout=self.timeout
        )
        return self._handle_response(response)
    
    def post(self, endpoint: str, data: Optional[Dict] = None, files: Optional[Dict] = None) -> Dict[str, Any]:
        """Make POST request"""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        if files:
            # Remove Content-Type for multipart/form-data
            headers.pop("Content-Type", None)
            response = self.session.post(
                url,
                data=data,
                files=files,
                headers=headers,
                timeout=self.timeout
            )
        else:
            response = self.session.post(
                url,
                json=data,
                headers=headers,
                timeout=self.timeout
            )
        return self._handle_response(response)
    
    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make PUT request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(
            url,
            json=data,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        return self._handle_response(response)
    
    def patch(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make PATCH request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.patch(
            url,
            json=data,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        return self._handle_response(response)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(
            url,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        return self._handle_response(response)
    
    # Authentication endpoints
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user"""
        return self.post("/api/auth/login", {
            "username": username,
            "password": password
        })
    
    def logout(self) -> None:
        """Logout user"""
        try:
            self.post("/api/auth/logout")
        finally:
            st.session_state.clear()


# Create global API client instance
api_client = APIClient()
