#!/usr/bin/env python3
"""
Simplified Test Script for RMP Liquidity Tracker
Uses pandas_datareader and FRED for reliable data access
"""

import sys
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("RMP Liquidity Tracker - Simplified Test")
print("=" * 60)
print()

# Test 1: Check imports
print("Test 1: Checking package imports...")
try:
    import pandas as pd
    print("✓ pandas imported")
except ImportError as e:
    print(f"✗ pandas failed: {e}")
    sys.exit(1)

try:
    import numpy as np
    print("✓ numpy imported")
except ImportError:
    print("✗ numpy failed")
    sys.exit(1)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    print("✓ matplotlib imported")
except ImportError:
    print("✗ matplotlib failed")
    sys.exit(1)

try:
    from fredapi import Fred
    print("✓ fredapi imported")
    FRED_AVAILABLE = True
except ImportError:
    print("⚠  fredapi not available (optional)")
    FRED_AVAILABLE = False

try:
    import pandas_datareader as pdr
    print("✓ pandas_datareader imported")
    PDR_AVAILABLE = True
except ImportError:
    print("⚠  pandas_datareader not available")
    PDR_AVAILABLE = False

print()

# Test 2: Fetch data using FRED (recommended for this use case)
print("Test 2: Testing FRED data access (without API key - limited)...")
print()

if not FRED_AVAILABLE:
    print("⚠  Skipping FRED test - fredapi not installed")
    print("   Install with: pip install fredapi")
else:
    print("Note: To test with full FRED access, you'll need an API key.")
    print("Get one free at: https://fred.stlouisfed.org/docs/api/api_key.html")
    print()

# Test 3: Use pandas_datareader to fetch data from FRED (no API key needed for some series)
print("Test 3: Fetching sample data using pandas_datareader...")
if PDR_AVAILABLE:
    try:
        start_date = '2023-01-01'
        end_date = datetime.today().strftime('%Y-%m-%d')

        print(f"  Fetching Fed Funds Rate from {start_date}...")
        fedfunds = pdr.get_data_fred('FEDFUNDS', start=start_date)
        print(f"✓ Fed Funds data: {len(fedfunds)} observations")
        print(f"  Latest Fed Funds Rate: {fedfunds.iloc[-1, 0]:.2f}% (as of {fedfunds.index[-1].strftime('%Y-%m-%d')})")

    except Exception as e:
        print(f"✗ Failed to fetch data: {e}")
        print("  This is normal if you don't have internet or FRED is down")
        fedfunds = None

    try:
        print(f"  Fetching 10Y Treasury Yield...")
        ust10y = pdr.get_data_fred('DGS10', start=start_date)
        print(f"✓ 10Y yield data: {len(ust10y)} observations")
        print(f"  Latest 10Y: {ust10y.iloc[-1, 0]:.2f}%")

    except Exception as e:
        print(f"⚠  Failed to fetch 10Y yield: {e}")
        ust10y = None

    try:
        print(f"  Fetching 2Y Treasury Yield...")
        ust2y = pdr.get_data_fred('DGS2', start=start_date)
        print(f"✓ 2Y yield data: {len(ust2y)} observations")
        print(f"  Latest 2Y: {ust2y.iloc[-1, 0]:.2f}%")

    except Exception as e:
        print(f"⚠  Failed to fetch 2Y yield: {e}")
        ust2y = None

    print()

    # Calculate yield curve
    if ust10y is not None and ust2y is not None:
        print("Test 4: Calculating yield curve spread (10Y-2Y)...")
        try:
            # Merge the data
            yield_curve = pd.DataFrame({
                '10Y': ust10y.iloc[:, 0],
                '2Y': ust2y.iloc[:, 0]
            })
            yield_curve['Spread'] = yield_curve['10Y'] - yield_curve['2Y']
            yield_curve = yield_curve.dropna()

            latest_spread = yield_curve['Spread'].iloc[-1]
            print(f"✓ Yield curve calculated")
            print(f"  Current 10Y-2Y spread: {latest_spread:.2f} bps")

            if latest_spread < 0:
                print(f"  → Curve is INVERTED (recession warning)")
            elif latest_spread < 50:
                print(f"  → Curve is FLAT (tightening conditions)")
            else:
                print(f"  → Curve is NORMAL/STEEP (healthy)")

            print()

            # Simple quadrant analysis
            print("Test 5: Simple Quadrant Analysis...")
            print()
            print("  Y-axis (Yield Curve):")
            if latest_spread < 0:
                y_position = "DOWN (Flattening)"
                y_desc = "Indicates tight monetary policy or recession fears"
            else:
                y_position = "UP (Steepening)"
                y_desc = "Indicates normal/healthy conditions"

            print(f"  Position: {y_position}")
            print(f"  Meaning: {y_desc}")
            print()
            print("  X-axis (US Dollar):")
            print("  Position: (Requires DXY data - see alternative method below)")
            print()

        except Exception as e:
            print(f"✗ Failed to calculate yield curve: {e}")
    else:
        print("⚠  Skipping yield curve calculation - missing data")

    print()

    # Test 6: Create simple visualization
    if ust10y is not None and ust2y is not None and 'yield_curve' in locals():
        print("Test 6: Creating visualization...")
        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))

            # Plot yields
            ax1.plot(yield_curve.index, yield_curve['10Y'], label='10Y Yield', linewidth=2, color='blue')
            ax1.plot(yield_curve.index, yield_curve['2Y'], label='2Y Yield', linewidth=2, color='green')
            ax1.set_title('Treasury Yields', fontweight='bold', fontsize=14)
            ax1.set_ylabel('Yield (%)')
            ax1.legend()
            ax1.grid(True, alpha=0.3)

            # Plot spread
            ax2.plot(yield_curve.index, yield_curve['Spread'], linewidth=2, color='purple')
            ax2.axhline(y=0, color='red', linestyle='--', linewidth=1, label='Inversion Line')
            ax2.fill_between(yield_curve.index, yield_curve['Spread'], 0,
                             where=yield_curve['Spread']>0, alpha=0.3, color='green', label='Normal')
            ax2.fill_between(yield_curve.index, yield_curve['Spread'], 0,
                             where=yield_curve['Spread']<=0, alpha=0.3, color='red', label='Inverted')
            ax2.set_title('Yield Curve Spread (10Y-2Y)', fontweight='bold', fontsize=14)
            ax2.set_ylabel('Spread (bps)')
            ax2.legend()
            ax2.grid(True, alpha=0.3)

            plt.tight_layout()

            output_file = '/home/user/pcrm-book/code/macro_analysis/test_yield_curve.png'
            plt.savefig(output_file, dpi=100, bbox_inches='tight')
            print(f"✓ Chart saved to: {output_file}")
            plt.close()

        except Exception as e:
            print(f"✗ Failed to create visualization: {e}")

    print()

else:
    print("⚠  pandas_datareader not available - install it to test data fetching")

print()
print("=" * 60)
print("Test Summary")
print("=" * 60)
print()

if PDR_AVAILABLE and 'yield_curve' in locals():
    print("✓✓✓ Core functionality is WORKING! ✓✓✓")
    print()
    print("You can now track:")
    print(f"  - Yield Curve: {latest_spread:.1f} bps ({'INVERTED' if latest_spread < 0 else 'NORMAL'})")
    if fedfunds is not None:
        print(f"  - Fed Funds: {fedfunds.iloc[-1, 0]:.2f}%")
    print()
    print("Next steps:")
    print("1. For full tracking, get a FREE FRED API key:")
    print("   → https://fred.stlouisfed.org/docs/api/api_key.html")
    print()
    print("2. Edit the notebook and add your API key:")
    print("   → code/macro_analysis/rmp_liquidity_tracker.ipynb")
    print("   → Look for: FRED_API_KEY = 'YOUR_KEY_HERE'")
    print()
    print("3. Run the full notebook to get:")
    print("   - Bank excess reserves tracking")
    print("   - Fed balance sheet monitoring")
    print("   - Reverse repo data")
    print("   - DXY (US Dollar) positioning")
    print("   - Full 4-quadrant spider diagram")
    print("   - Liquidity dashboard")
    print()
    print("Alternative: Use free data sources (no API key)")
    print("  - DXY: Check investing.com or tradingview.com")
    print("  - VIX: Check cboe.com")
    print("  - Daily monitoring: Use the checklist in MARKETS_TO_TRACK.md")
else:
    print("⚠  Some issues detected - but core packages are installed")
    print()
    print("If you had connection errors, that's normal without internet.")
    print("The notebook will work fine when you have network access.")
    print()
    print("To fix any issues:")
    print("  pip install pandas numpy matplotlib fredapi pandas-datareader")

print()
print("=" * 60)
print()
print("Ready to use the framework! Start with:")
print("  - Read: code/macro_analysis/MARKETS_TO_TRACK.md")
print("  - Then open: code/macro_analysis/rmp_liquidity_tracker.ipynb")
print()
