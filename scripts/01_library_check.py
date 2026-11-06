import os
import sys

# Ensure root and src directories are in sys.path
_current = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(_current) if os.path.basename(_current) == "scripts" else _current
_src = os.path.join(_root, "src")
for _p in (_root, _src):
    if _p not in sys.path:
        sys.path.insert(0, _p)

print("=" * 60)
print("STEP 2 - LIBRARY CHECK")
print("=" * 60)

libraries = ["pandas", "numpy", "matplotlib", "sklearn", "streamlit", "plotly"]
for lib in libraries:
    try:
        __import__(lib)
        print(f"✓ {lib} is installed")
    except ImportError:
        print(f"✗ {lib} is NOT installed")
print("\nLibrary checking completed!")
