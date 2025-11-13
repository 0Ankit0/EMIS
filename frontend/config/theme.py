"""
Theme Configuration
"""

# Color palette
COLORS = {
    "primary": "#0066cc",
    "secondary": "#28a745",
    "success": "#28a745",
    "danger": "#dc3545",
    "warning": "#ffc107",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40",
    "white": "#ffffff",
    "text": "#212529",
    "muted": "#6c757d",
}

# Streamlit theme configuration
STREAMLIT_THEME = {
    "primaryColor": COLORS["primary"],
    "backgroundColor": COLORS["white"],
    "secondaryBackgroundColor": COLORS["light"],
    "textColor": COLORS["text"],
    "font": "sans serif"
}

# Chart colors
CHART_COLORS = [
    "#0066cc", "#28a745", "#ffc107", "#dc3545", 
    "#17a2b8", "#6610f2", "#e83e8c", "#fd7e14"
]

# Status colors
STATUS_COLORS = {
    "success": "#28a745",
    "error": "#dc3545",
    "warning": "#ffc107",
    "info": "#17a2b8",
    "pending": "#ffc107",
    "completed": "#28a745",
    "failed": "#dc3545",
}

# Typography
FONT_SIZES = {
    "h1": "2.5rem",
    "h2": "2rem",
    "h3": "1.75rem",
    "h4": "1.5rem",
    "h5": "1.25rem",
    "h6": "1rem",
    "body": "1rem",
    "small": "0.875rem",
    "tiny": "0.75rem",
}

# Spacing
SPACING = {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "3rem",
}

# Border radius
BORDER_RADIUS = {
    "sm": "0.2rem",
    "md": "0.25rem",
    "lg": "0.3rem",
    "circle": "50%",
}

# Box shadows
BOX_SHADOW = {
    "sm": "0 .125rem .25rem rgba(0,0,0,.075)",
    "md": "0 .5rem 1rem rgba(0,0,0,.15)",
    "lg": "0 1rem 3rem rgba(0,0,0,.175)",
}

# Custom CSS
CUSTOM_CSS = """
<style>
    .main {
        padding: 0rem 1rem;
    }
    
    .stButton>button {
        width: 100%;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .success-badge {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.875rem;
    }
    
    .warning-badge {
        background-color: #ffc107;
        color: #212529;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.875rem;
    }
    
    .danger-badge {
        background-color: #dc3545;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.875rem;
    }
    
    .info-badge {
        background-color: #17a2b8;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.875rem;
    }
</style>
"""
