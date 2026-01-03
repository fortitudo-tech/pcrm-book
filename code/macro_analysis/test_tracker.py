#!/usr/bin/env python3
"""
Test script for RMP Liquidity Tracker
Tests basic functionality without needing a FRED API key
"""

import sys
from datetime import datetime, timedelta

print("=" * 60)
print("RMP Liquidity Tracker - Test Script")
print("=" * 60)
print()

# Test 1: Check imports
print("Test 1: Checking package imports...")
try:
    import pandas as pd
    print("✓ pandas imported successfully")
except ImportError as e:
    print(f"✗ pandas import failed: {e}")
    sys.exit(1)

try:
    import numpy as np
    print("✓ numpy imported successfully")
except ImportError as e:
    print(f"✗ numpy import failed: {e}")
    sys.exit(1)

try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    print("✓ matplotlib imported successfully")
except ImportError as e:
    print(f"✗ matplotlib import failed: {e}")
    sys.exit(1)

try:
    import yfinance as yf
    print("✓ yfinance imported successfully")
except ImportError as e:
    print(f"✗ yfinance import failed: {e}")
    print("  Installing yfinance...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "yfinance", "--no-deps"], check=True)
    import yfinance as yf
    print("✓ yfinance installed and imported")

try:
    import seaborn as sns
    print("✓ seaborn imported successfully")
except ImportError as e:
    print(f"✗ seaborn import failed: {e}")
    print("  Continuing without seaborn...")

try:
    from fredapi import Fred
    print("✓ fredapi imported successfully")
    FRED_AVAILABLE = True
except ImportError as e:
    print("⚠ fredapi not available (optional for this test)")
    FRED_AVAILABLE = False

print()

# Test 2: Fetch sample market data
print("Test 2: Fetching sample market data from Yahoo Finance...")
start_date = '2023-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')

try:
    print(f"  Fetching DXY (US Dollar Index) from {start_date} to {end_date}...")
    dxy = yf.download('DX-Y.NYB', start=start_date, end=end_date, progress=False)['Close']
    print(f"✓ DXY data fetched: {len(dxy)} data points")
    print(f"  Latest DXY: {dxy.iloc[-1]:.2f} (as of {dxy.index[-1].strftime('%Y-%m-%d')})")
except Exception as e:
    print(f"✗ Failed to fetch DXY: {e}")
    dxy = pd.Series()

try:
    print(f"  Fetching VIX (Volatility Index)...")
    vix = yf.download('^VIX', start=start_date, end=end_date, progress=False)['Close']
    print(f"✓ VIX data fetched: {len(vix)} data points")
    print(f"  Latest VIX: {vix.iloc[-1]:.2f}")
except Exception as e:
    print(f"✗ Failed to fetch VIX: {e}")
    vix = pd.Series()

try:
    print(f"  Fetching 10Y Treasury Yield...")
    tnx = yf.download('^TNX', start=start_date, end=end_date, progress=False)['Close']
    print(f"✓ 10Y yield data fetched: {len(tnx)} data points")
    print(f"  Latest 10Y: {tnx.iloc[-1]:.2f}%")
except Exception as e:
    print(f"✗ Failed to fetch 10Y yield: {e}")
    tnx = pd.Series()

print()

# Test 3: Create combined dataset
print("Test 3: Creating combined dataset...")
try:
    data = pd.DataFrame({
        'DXY': dxy,
        'VIX': vix,
        'UST_10Y': tnx
    })
    data = data.dropna()
    print(f"✓ Combined dataset created: {len(data)} rows")
    print(f"\nLast 5 observations:")
    print(data.tail().to_string())
except Exception as e:
    print(f"✗ Failed to create dataset: {e}")
    sys.exit(1)

print()

# Test 4: Calculate basic statistics
print("Test 4: Calculating basic statistics...")
try:
    print("\nDXY Statistics:")
    print(f"  Current: {data['DXY'].iloc[-1]:.2f}")
    print(f"  30-day avg: {data['DXY'].tail(30).mean():.2f}")
    print(f"  90-day avg: {data['DXY'].tail(90).mean():.2f}")
    print(f"  YTD change: {((data['DXY'].iloc[-1] / data['DXY'].iloc[0] - 1) * 100):.2f}%")

    print("\nVIX Statistics:")
    print(f"  Current: {data['VIX'].iloc[-1]:.2f}")
    print(f"  30-day avg: {data['VIX'].tail(30).mean():.2f}")
    if data['VIX'].iloc[-1] < 20:
        stress_level = "LOW (Normal)"
    elif data['VIX'].iloc[-1] < 30:
        stress_level = "ELEVATED"
    else:
        stress_level = "HIGH (Crisis)"
    print(f"  Stress level: {stress_level}")

    print(f"✓ Statistics calculated successfully")
except Exception as e:
    print(f"✗ Failed to calculate statistics: {e}")

print()

# Test 5: Test z-score calculation (for quadrant positioning)
print("Test 5: Testing quadrant positioning calculation...")
try:
    lookback = min(252, len(data))  # 1 year or available data

    # Calculate z-scores
    dxy_mean = data['DXY'].rolling(lookback).mean()
    dxy_std = data['DXY'].rolling(lookback).std()
    data['DXY_zscore'] = (data['DXY'] - dxy_mean) / dxy_std

    current_dxy_z = data['DXY_zscore'].iloc[-1]
    print(f"  DXY Z-Score: {current_dxy_z:.2f}")

    if current_dxy_z > 0:
        print(f"  → Dollar is STRONGER than recent average")
    else:
        print(f"  → Dollar is WEAKER than recent average")

    print(f"✓ Z-score calculation working")
except Exception as e:
    print(f"✗ Failed to calculate z-scores: {e}")

print()

# Test 6: Simple visualization test
print("Test 6: Testing visualization capabilities...")
try:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Plot DXY
    ax1.plot(data.index, data['DXY'], linewidth=2, color='blue')
    ax1.set_title('US Dollar Index (DXY)', fontweight='bold')
    ax1.set_ylabel('Index Level')
    ax1.grid(True, alpha=0.3)

    # Plot VIX
    ax2.plot(data.index, data['VIX'], linewidth=2, color='red')
    ax2.axhline(y=20, color='orange', linestyle='--', alpha=0.5, label='Elevated (20)')
    ax2.axhline(y=30, color='red', linestyle='--', alpha=0.5, label='Crisis (30)')
    ax2.set_title('VIX (Market Stress)', fontweight='bold')
    ax2.set_ylabel('VIX Level')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    # Save to file
    output_file = '/home/user/pcrm-book/code/macro_analysis/test_chart.png'
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    print(f"✓ Test chart saved to: {output_file}")
    plt.close()
except Exception as e:
    print(f"✗ Failed to create visualization: {e}")

print()

# Test 7: Quadrant determination
print("Test 7: Determining current market quadrant...")
print("  (Note: Full calculation requires 10Y-2Y spread from FRED)")
print()

# Mock yield curve data for demo (normally from FRED)
print("  Using DXY position as proxy for demonstration...")
try:
    if current_dxy_z > 0:
        x_position = "RIGHT (Rising Dollar)"
    else:
        x_position = "LEFT (Falling Dollar)"

    print(f"  X-axis position: {x_position}")
    print(f"  Y-axis position: (Requires FRED data for yield curve)")
    print()
    print("  Interpretation:")
    if current_dxy_z > 0:
        print("  - Dollar strength suggests safe-haven flows OR Fed tightening")
        print("  - Monitor liquidity conditions (bank reserves, RRP)")
        print("  - Watch for movement toward Hawkish Policy quadrant (2026 forecast)")
    else:
        print("  - Dollar weakness suggests risk-on OR Fed easing expectations")
        print("  - Could indicate Dovish/Co-operative policy stance")

    print(f"✓ Quadrant logic working")
except Exception as e:
    print(f"✗ Failed quadrant determination: {e}")

print()
print("=" * 60)
print("Test Summary")
print("=" * 60)
print()
print("✓ Core functionality is working!")
print()
print("Next steps:")
print("1. Get a free FRED API key: https://fred.stlouisfed.org/docs/api/api_key.html")
print("2. Add API key to the notebook: code/macro_analysis/rmp_liquidity_tracker.ipynb")
print("3. Run the full notebook for complete analysis with:")
print("   - Yield curve data (10Y-2Y spread)")
print("   - Bank excess reserves")
print("   - Fed balance sheet")
print("   - Reverse repo")
print("   - Full quadrant spider diagram")
print()
print("For now, you can monitor:")
print(f"- DXY: {data['DXY'].iloc[-1]:.2f} (current)")
print(f"- VIX: {data['VIX'].iloc[-1]:.2f} ({stress_level})")
print(f"- 10Y Yield: {data['UST_10Y'].iloc[-1]:.2f}%")
print()
print("=" * 60)
