"""
Utility Functions for Frontend
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date
from typing import Any, Dict, List, Optional
from config.settings import DATE_FORMAT, DATETIME_FORMAT, DISPLAY_DATE_FORMAT


def init_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "user_role" not in st.session_state:
        st.session_state.user_role = None


def format_date(date_obj: Any, format_str: str = DISPLAY_DATE_FORMAT) -> str:
    """Format date object to string"""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj, DATE_FORMAT)
        except ValueError:
            return date_obj
    
    if isinstance(date_obj, (datetime, date)):
        return date_obj.strftime(format_str)
    
    return str(date_obj)


def parse_date(date_str: str, format_str: str = DATE_FORMAT) -> Optional[datetime]:
    """Parse date string to datetime object"""
    try:
        return datetime.strptime(date_str, format_str)
    except (ValueError, TypeError):
        return None


def show_success(message: str):
    """Display success message"""
    st.success(f"✅ {message}")


def show_error(message: str):
    """Display error message"""
    st.error(f"❌ {message}")


def show_warning(message: str):
    """Display warning message"""
    st.warning(f"⚠️ {message}")


def show_info(message: str):
    """Display info message"""
    st.info(f"ℹ️ {message}")


def create_download_button(data: pd.DataFrame, filename: str, label: str = "Download CSV"):
    """Create download button for dataframe"""
    csv = data.to_csv(index=False)
    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime="text/csv"
    )


def paginate_dataframe(df: pd.DataFrame, page_size: int = 20) -> pd.DataFrame:
    """Add pagination to dataframe"""
    total_pages = len(df) // page_size + (1 if len(df) % page_size > 0 else 0)
    
    if total_pages > 1:
        page = st.selectbox("Page", range(1, total_pages + 1))
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        return df.iloc[start_idx:end_idx]
    
    return df


def format_currency(amount: float, currency: str = "₹") -> str:
    """Format amount as currency"""
    return f"{currency}{amount:,.2f}"


def calculate_percentage(value: float, total: float) -> float:
    """Calculate percentage"""
    if total == 0:
        return 0
    return (value / total) * 100


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> bool:
    """Validate required fields in form data"""
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        show_error(f"Missing required fields: {', '.join(missing_fields)}")
        return False
    
    return True


def get_user_role() -> Optional[str]:
    """Get current user role"""
    return st.session_state.get("user_role")


def has_permission(required_role: str) -> bool:
    """Check if user has required permission"""
    user_role = get_user_role()
    
    role_hierarchy = {
        "admin": 4,
        "teacher": 3,
        "staff": 2,
        "student": 1
    }
    
    user_level = role_hierarchy.get(user_role, 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    return user_level >= required_level


def requires_authentication(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not st.session_state.get("authenticated", False):
            st.warning("Please login to access this page")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def requires_role(role: str):
    """Decorator to require specific role"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not has_permission(role):
                st.error("You don't have permission to access this page")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    return decorator
