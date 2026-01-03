"""
Quick test to verify your environment is ready
Save this as: quick_test.py
Run with: python quick_test.py
"""

import sys

print("=" * 60)
print("RMP Liquidity Tracker - Environment Test")
print("=" * 60)
print()

# Test Python version
print(f"Python version: {sys.version}")
print()

# Test imports
packages = {
    'pandas': 'pandas',
    'numpy': 'numpy',
    'matplotlib': 'matplotlib',
    'fredapi': 'fredapi (optional for demo)',
    'pandas_datareader': 'pandas_datareader (optional)'
}

print("Testing package imports...")
for package, display_name in packages.items():
    try:
        __import__(package)
        print(f"  ✓ {display_name}")
    except ImportError:
        print(f"  ✗ {display_name} - NOT INSTALLED")

print()
print("=" * 60)
print("Environment Check Complete!")
print("=" * 60)
print()
print("Next steps:")
print("1. Get the notebook and Python files from the repository")
print("2. Add your FRED API key to the notebook")
print("3. Run: python demo_tracker.py")
print()

print("Files you need (download from GitHub or copy from repo):")
print("  - rmp_liquidity_tracker.ipynb")
print("  - demo_tracker.py")
print("  - MARKETS_TO_TRACK.md")
print("  - QUICKSTART.md")
print()
