"""
Date and Time Utilities
"""
from datetime import datetime, date, timedelta
from typing import Optional


def get_current_date() -> date:
    """Get current date"""
    return date.today()


def get_current_datetime() -> datetime:
    """Get current datetime"""
    return datetime.now()


def get_current_timestamp() -> str:
    """Get current timestamp as string"""
    return datetime.now().isoformat()


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[date]:
    """Parse date string to date object"""
    try:
        return datetime.strptime(date_str, format_str).date()
    except (ValueError, TypeError):
        return None


def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """Parse datetime string to datetime object"""
    try:
        return datetime.strptime(dt_str, format_str)
    except (ValueError, TypeError):
        return None


def add_days(start_date: date, days: int) -> date:
    """Add days to a date"""
    return start_date + timedelta(days=days)


def subtract_days(start_date: date, days: int) -> date:
    """Subtract days from a date"""
    return start_date - timedelta(days=days)


def days_between(date1: date, date2: date) -> int:
    """Calculate days between two dates"""
    return abs((date2 - date1).days)


def is_weekend(check_date: date) -> bool:
    """Check if date is weekend (Saturday or Sunday)"""
    return check_date.weekday() in [5, 6]


def get_week_start(check_date: date) -> date:
    """Get start of week (Monday) for given date"""
    return check_date - timedelta(days=check_date.weekday())


def get_week_end(check_date: date) -> date:
    """Get end of week (Sunday) for given date"""
    return check_date + timedelta(days=6 - check_date.weekday())


def get_month_start(check_date: date) -> date:
    """Get first day of month"""
    return check_date.replace(day=1)


def get_month_end(check_date: date) -> date:
    """Get last day of month"""
    next_month = check_date.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def get_year_start(check_date: date) -> date:
    """Get first day of year"""
    return check_date.replace(month=1, day=1)


def get_year_end(check_date: date) -> date:
    """Get last day of year"""
    return check_date.replace(month=12, day=31)


def get_academic_year(check_date: date, start_month: int = 7) -> str:
    """
    Get academic year (e.g., 2023-2024)
    Default start month is July
    """
    year = check_date.year
    if check_date.month >= start_month:
        return f"{year}-{year + 1}"
    else:
        return f"{year - 1}-{year}"


def get_semester(check_date: date, start_month: int = 7) -> str:
    """
    Get current semester (Odd/Even)
    Assuming Odd semester starts in July/August
    """
    month = check_date.month
    
    # Odd semester: July to December
    # Even semester: January to June
    if start_month <= month <= 12:
        return "Odd"
    else:
        return "Even"


def is_past_date(check_date: date) -> bool:
    """Check if date is in the past"""
    return check_date < get_current_date()


def is_future_date(check_date: date) -> bool:
    """Check if date is in the future"""
    return check_date > get_current_date()


def get_age(birth_date: date) -> int:
    """Calculate age from birth date"""
    today = get_current_date()
    age = today.year - birth_date.year
    
    # Adjust if birthday hasn't occurred yet this year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    
    return age


def get_time_ago(past_datetime: datetime) -> str:
    """Get human-readable time ago string"""
    now = datetime.now()
    diff = now - past_datetime
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif seconds < 31536000:
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = int(seconds / 31536000)
        return f"{years} year{'s' if years != 1 else ''} ago"
