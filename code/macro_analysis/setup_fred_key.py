"""
Automatic FRED API Key Setup Script
This script updates the notebook with your FRED API key
Run with: python setup_fred_key.py
"""

import json
import os

print("=" * 70)
print("FRED API Key Setup for RMP Liquidity Tracker")
print("=" * 70)
print()

# Get API key from user
print("Please enter your FRED API key:")
print("(Get one free at: https://fred.stlouisfed.org/docs/api/api_key.html)")
print()
api_key = input("FRED API Key: ").strip()

if not api_key or api_key == "":
    print("Error: No API key provided!")
    exit(1)

# Check if notebook exists
notebook_file = "rmp_liquidity_tracker.ipynb"
if not os.path.exists(notebook_file):
    print(f"Error: {notebook_file} not found!")
    print("Please download it first with:")
    print(f"  curl -o {notebook_file} https://raw.githubusercontent.com/Jerempire/pcrm-book/claude/add-rmp-liquidity-program-Nee07/code/macro_analysis/{notebook_file}")
    exit(1)

print()
print(f"Reading {notebook_file}...")

# Read the notebook
with open(notebook_file, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Update the API key in the notebook
updated = False
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = cell.get('source', [])
        for i, line in enumerate(source):
            if 'FRED_API_KEY' in line and 'YOUR_FRED_API_KEY_HERE' in line:
                # Replace the placeholder with actual key
                source[i] = f"FRED_API_KEY = '{api_key}'  # Your FRED API key\n"
                updated = True
                print(f"✓ Updated FRED_API_KEY in cell")

            # Uncomment the fred initialization
            if line.strip() == "# fred = Fred(api_key=FRED_API_KEY)":
                source[i] = "fred = Fred(api_key=FRED_API_KEY)\n"
                print(f"✓ Uncommented FRED initialization")

# Save the updated notebook
if updated:
    with open(notebook_file, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)

    print()
    print("=" * 70)
    print("SUCCESS! Notebook updated with your FRED API key!")
    print("=" * 70)
    print()
    print("Next steps:")
    print(f"1. Open the notebook: jupyter lab {notebook_file}")
    print("2. In the notebook, find the commented cells (lines starting with #)")
    print("3. Uncomment the data fetching cells by removing the # symbols")
    print("4. Run all cells: Cell → Run All")
    print()
    print("Or run individual cells step by step to see each stage!")
    print()
else:
    print()
    print("Warning: Could not find FRED_API_KEY line to update.")
    print("You may need to edit the notebook manually.")
    print()

print("=" * 70)
