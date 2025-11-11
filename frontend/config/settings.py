"""
Frontend Configuration Settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# Authentication
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1 hour
TOKEN_REFRESH_INTERVAL = int(os.getenv("TOKEN_REFRESH_INTERVAL", "1800"))  # 30 minutes

# UI Configuration
PAGE_TITLE = "EMIS - Education Management Information System"
PAGE_ICON = "🎓"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# Theme Configuration
THEME = {
    "primaryColor": "#0066cc",
    "backgroundColor": "#ffffff",
    "secondaryBackgroundColor": "#f0f2f6",
    "textColor": "#262730",
    "font": "sans serif"
}

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# File Upload
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {
    "documents": [".pdf", ".doc", ".docx"],
    "images": [".jpg", ".jpeg", ".png", ".gif"],
    "spreadsheets": [".xls", ".xlsx", ".csv"]
}

# Date Format
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DISPLAY_DATE_FORMAT = "%d/%m/%Y"
DISPLAY_DATETIME_FORMAT = "%d/%m/%Y %H:%M"

# Chart Configuration
CHART_HEIGHT = 400
CHART_WIDTH = 800
