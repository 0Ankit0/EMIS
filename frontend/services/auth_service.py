"""
Auth Service
Handles authentication and authorization
"""
from utils.api_client import api_client
from typing import Dict, Optional
import streamlit as st


class AuthService:
    """Authentication service"""
    
    @staticmethod
    def login(username: str, password: str) -> Dict:
        """
        Login user
        Returns user data with access token
        """
        data = {
            "username": username,
            "password": password
        }
        response = api_client.post("/api/auth/login", data)
        
        # Store in session
        if response:
            st.session_state.authenticated = True
            st.session_state.access_token = response.get("access_token")
            st.session_state.refresh_token = response.get("refresh_token")
            st.session_state.user = response.get("user")
            st.session_state.user_role = response.get("user", {}).get("role")
        
        return response
    
    @staticmethod
    def logout():
        """Logout user"""
        try:
            api_client.post("/api/auth/logout")
        except:
            pass
        
        # Clear session
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
    @staticmethod
    def register(data: Dict) -> Dict:
        """Register new user"""
        return api_client.post("/api/auth/register", data)
    
    @staticmethod
    def refresh_token() -> Dict:
        """Refresh access token"""
        refresh_token = st.session_state.get("refresh_token")
        if not refresh_token:
            raise Exception("No refresh token available")
        
        data = {"refresh_token": refresh_token}
        response = api_client.post("/api/auth/refresh", data)
        
        if response:
            st.session_state.access_token = response.get("access_token")
        
        return response
    
    @staticmethod
    def change_password(current_password: str, new_password: str) -> Dict:
        """Change user password"""
        data = {
            "current_password": current_password,
            "new_password": new_password
        }
        return api_client.post("/api/auth/change-password", data)
    
    @staticmethod
    def request_password_reset(email: str) -> Dict:
        """Request password reset"""
        data = {"email": email}
        return api_client.post("/api/auth/password-reset/request", data)
    
    @staticmethod
    def reset_password(token: str, new_password: str) -> Dict:
        """Reset password with token"""
        data = {
            "token": token,
            "new_password": new_password
        }
        return api_client.post("/api/auth/password-reset/confirm", data)
    
    @staticmethod
    def verify_email(token: str) -> Dict:
        """Verify email with token"""
        data = {"token": token}
        return api_client.post("/api/auth/verify-email", data)
    
    @staticmethod
    def setup_2fa() -> Dict:
        """Setup two-factor authentication"""
        return api_client.post("/api/auth/2fa/setup")
    
    @staticmethod
    def verify_2fa(code: str) -> Dict:
        """Verify 2FA code"""
        data = {"code": code}
        return api_client.post("/api/auth/2fa/verify", data)
    
    @staticmethod
    def disable_2fa() -> Dict:
        """Disable two-factor authentication"""
        return api_client.post("/api/auth/2fa/disable")
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated"""
        return st.session_state.get("authenticated", False)
    
    @staticmethod
    def get_current_user() -> Optional[Dict]:
        """Get current logged in user"""
        return st.session_state.get("user")
    
    @staticmethod
    def get_user_role() -> Optional[str]:
        """Get current user role"""
        return st.session_state.get("user_role")
    
    @staticmethod
    def has_permission(permission: str) -> bool:
        """Check if user has specific permission"""
        user = AuthService.get_current_user()
        if not user:
            return False
        
        permissions = user.get("permissions", [])
        return permission in permissions


# Singleton instance
auth_service = AuthService()
