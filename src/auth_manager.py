"""
User Authentication and Profile Manager for UPI Financial Wellness Assistant.
Handles user registration, login, secure SHA-256 password hashing with salt,
and session management with local JSON persistence in ./data/users.json.
"""

import os
import json
import hashlib
from datetime import datetime

_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_here) if os.path.basename(_here) in ("src", "scripts") else _here
USERS_FILE = os.path.join(BASE_DIR, "data", "users.json")
GLOBAL_SALT = "upi_financial_wellness_secure_salt_v1"


def _hash_password(password: str, salt: str = GLOBAL_SALT) -> str:
    """Generates a salted SHA-256 hash for password storage."""
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()


def _get_default_users() -> dict:
    """Returns default accounts initialized for instant demo access."""
    return {
        "jashnavi": {
            "username": "jashnavi",
            "password_hash": _hash_password("admin123"),
            "full_name": "Jashnavi",
            "email": "jashnavi@upiwellness.ai",
            "monthly_income": 85000.0,
            "savings_target": 250000.0,
            "role": "Premium Member",
            "avatar": "🌟",
            "created_at": "2026-01-01 10:00:00"
        },
        "demo": {
            "username": "demo",
            "password_hash": _hash_password("demo123"),
            "full_name": "Demo Analyst",
            "email": "demo@upiwellness.ai",
            "monthly_income": 60000.0,
            "savings_target": 120000.0,
            "role": "Standard User",
            "avatar": "👤",
            "created_at": "2026-01-01 10:00:00"
        }
    }


def load_users() -> dict:
    """Loads users from JSON file, initializing defaults if absent."""
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    if not os.path.exists(USERS_FILE):
        default_users = _get_default_users()
        save_users(default_users)
        return default_users

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict) or len(data) == 0:
                data = _get_default_users()
                save_users(data)
            return data
    except Exception:
        default_users = _get_default_users()
        save_users(default_users)
        return default_users


def save_users(users: dict) -> bool:
    """Saves users dictionary to JSON file."""
    try:
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False


def authenticate(username_or_email: str, password: str) -> tuple[bool, dict | None, str]:
    """
    Authenticates a user by username or email.
    Returns: (is_success, user_dict, error_or_success_message)
    """
    users = load_users()
    key = username_or_email.strip().lower()

    # Search by username or email
    matched_user = None
    for u, details in users.items():
        if u.lower() == key or details.get("email", "").lower() == key:
            matched_user = details
            break

    if not matched_user:
        return False, None, "Account not found with this username or email."

    given_hash = _hash_password(password)
    if given_hash != matched_user.get("password_hash"):
        return False, None, "Incorrect password. Please try again."

    # Return copy without sensitive password hash
    safe_profile = dict(matched_user)
    safe_profile.pop("password_hash", None)
    return True, safe_profile, f"Welcome back, {safe_profile.get('full_name', 'User')}!"


def register_user(username: str, password: str, email: str, full_name: str, 
                  monthly_income: float = 60000.0, savings_target: float = 100000.0) -> tuple[bool, str]:
    """
    Registers a new user account.
    Returns: (is_success, message)
    """
    users = load_users()
    uname = username.strip().lower()
    email_clean = email.strip().lower()

    if not uname or len(uname) < 3:
        return False, "Username must be at least 3 characters."
    if not password or len(password) < 4:
        return False, "Password must be at least 4 characters."
    if not email_clean or "@" not in email_clean:
        return False, "Please enter a valid email address."

    # Check duplicates
    for u, details in users.items():
        if u.lower() == uname:
            return False, f"Username '{username}' is already taken."
        if details.get("email", "").lower() == email_clean:
            return False, f"Email '{email}' is already registered."

    # Create new profile
    users[uname] = {
        "username": uname,
        "password_hash": _hash_password(password),
        "full_name": full_name.strip() or uname.capitalize(),
        "email": email_clean,
        "monthly_income": float(monthly_income) if monthly_income > 0 else 60000.0,
        "savings_target": float(savings_target) if savings_target > 0 else 100000.0,
        "role": "Verified User",
        "avatar": "💳",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if save_users(users):
        return True, "Account registered successfully! You can now sign in."
    else:
        return False, "Failed to save user account. Please check file permissions."
