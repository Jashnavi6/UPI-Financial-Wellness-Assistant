"""
Path configuration helper for UPI Financial Wellness Assistant.
Ensures seamless operation both in local workspace (./data) and external path (C:/Users/jashn/data).
Also sets console output encoding to UTF-8 on Windows.
"""

import os
import sys

# Ensure UTF-8 console output for terminal printing on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

_here = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_here) if os.path.basename(_here) in ("src", "scripts") else _here
LOCAL_DATA_DIR = os.path.join(BASE_DIR, "data")
SYSTEM_DATA_DIR = "C:/Users/jashn/data"


def get_data_path(relative_subpath, for_writing=False):
    """
    Resolves data path. If local exists or system path is inaccessible, returns local path.
    """
    local_path = os.path.normpath(os.path.join(LOCAL_DATA_DIR, relative_subpath))
    system_path = os.path.normpath(os.path.join(SYSTEM_DATA_DIR, relative_subpath))

    if for_writing:
        try:
            os.makedirs(os.path.dirname(system_path), exist_ok=True)
            with open(system_path, "a") as f:
                pass
            return system_path
        except Exception:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            return local_path

    # For reading:
    if os.path.exists(local_path):
        return local_path
    try:
        if os.path.exists(system_path):
            return system_path
    except Exception:
        pass
    return local_path
