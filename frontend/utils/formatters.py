"""
Data Formatters
"""
from datetime import datetime, date
from typing import Any, Optional


def format_currency(amount: float, currency: str = "₹", decimals: int = 2) -> str:
    """Format amount as currency"""
    return f"{currency}{amount:,.{decimals}f}"


def format_date(date_obj: Any, format_str: str = "%d-%m-%Y") -> str:
    """Format date object to string"""
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        except ValueError:
            return date_obj
    
    if isinstance(date_obj, (datetime, date)):
        return date_obj.strftime(format_str)
    
    return str(date_obj)


def format_datetime(dt_obj: Any, format_str: str = "%d-%m-%Y %H:%M:%S") -> str:
    """Format datetime object to string"""
    if isinstance(dt_obj, str):
        try:
            dt_obj = datetime.fromisoformat(dt_obj.replace('Z', '+00:00'))
        except ValueError:
            return dt_obj
    
    if isinstance(dt_obj, datetime):
        return dt_obj.strftime(format_str)
    
    return str(dt_obj)


def format_time(time_obj: Any, format_str: str = "%H:%M:%S") -> str:
    """Format time object to string"""
    if isinstance(time_obj, datetime):
        return time_obj.strftime(format_str)
    return str(time_obj)


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format value as percentage"""
    return f"{value:.{decimals}f}%"


def format_phone(phone: str) -> str:
    """Format phone number"""
    # Remove all non-numeric characters
    cleaned = ''.join(filter(str.isdigit, phone))
    
    # Format as XXX-XXX-XXXX or +XX-XXXX-XXXXXX
    if len(cleaned) == 10:
        return f"{cleaned[:3]}-{cleaned[3:6]}-{cleaned[6:]}"
    elif len(cleaned) == 12:
        return f"+{cleaned[:2]}-{cleaned[2:6]}-{cleaned[6:]}"
    return phone


def format_name(name: str) -> str:
    """Format name with proper capitalization"""
    return ' '.join(word.capitalize() for word in name.split())


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def format_number(num: float, decimals: int = 2, thousand_sep: str = ",") -> str:
    """Format number with thousand separator"""
    format_str = f"{{:,.{decimals}f}}"
    return format_str.format(num)


def format_duration(seconds: int) -> str:
    """Format duration in seconds to readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_grade(percentage: float) -> str:
    """Format percentage to grade"""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C+"
    elif percentage >= 40:
        return "C"
    else:
        return "F"


def format_list(items: list, separator: str = ", ", last_sep: str = " and ") -> str:
    """Format list to readable string"""
    if not items:
        return ""
    if len(items) == 1:
        return str(items[0])
    if len(items) == 2:
        return f"{items[0]}{last_sep}{items[1]}"
    return separator.join(str(i) for i in items[:-1]) + last_sep + str(items[-1])
