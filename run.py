"""
Standard Python Entry Point for UPI Financial Wellness Assistant.
Run this directly with Python or click the ▶ Play button in VS Code:
    python run.py
"""

import os
import sys

if __name__ == "__main__":
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    local_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(local_dir, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    os.environ["STREAMLIT_CONFIG_DIR"] = os.path.join(local_dir, ".streamlit")
    from streamlit.web import cli as stcli
    app_path = os.path.join(local_dir, "app.py")
    sys.argv = [
        "streamlit", 
        "run", 
        app_path, 
        "--browser.gatherUsageStats=false", 
        "--server.headless=true"
    ]
    sys.exit(stcli.main())
