#!/usr/bin/env python3
"""
Demo script showing the RMP Liquidity Tracker with mock data
This demonstrates the full functionality without needing network access
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("RMP LIQUIDITY TRACKER - DEMO WITH MOCK DATA")
print("=" * 70)
print()
print("This demo shows all functionality using simulated market data.")
print("With real data (FRED API + internet), you'll get actual market values.")
print()

# Generate mock data for demonstration
print("Step 1: Generating mock market data (simulating 2023-2024)...")
dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
n = len(dates)

# Simulate realistic market data
np.random.seed(42)

# DXY (US Dollar) - trending up in 2024
dxy_trend = np.linspace(102, 107, n)  # +5% appreciation
dxy = dxy_trend + np.random.normal(0, 0.5, n).cumsum() * 0.3

# Yield Curve (10Y-2Y spread) - flattening then inverting then normalizing
half_n = n // 2
curve_base = np.concatenate([
    np.linspace(50, -50, half_n),  # Flattening to inversion
    np.linspace(-50, 30, n - half_n)   # Recovery (handles odd n)
])
yield_curve = curve_base + np.random.normal(0, 10, n)

# Bank Reserves - declining (liquidity tightening)
reserves_trend = np.linspace(3500, 3100, n)  # Billions
reserves = reserves_trend + np.random.normal(0, 50, n)

# VIX - with occasional spikes
vix_base = 15 + np.random.gamma(2, 2, n)
# Add some stress events
stress_periods = np.random.choice(n, size=5, replace=False)
for period in stress_periods:
    vix_base[max(0, period-10):min(n, period+10)] += np.random.uniform(10, 20)

# Fed Balance Sheet - QT (declining)
fed_bs = np.linspace(8500, 7800, n)  # Billions

# RRP - volatile
rrp = np.abs(1500 + np.random.normal(0, 200, n).cumsum() * 0.5)

# Create DataFrame
data = pd.DataFrame({
    'DXY': dxy,
    'Yield_Curve_10Y2Y': yield_curve,
    'Bank_Excess_Reserves': reserves,
    'VIX': vix_base,
    'Fed_Balance_Sheet': fed_bs,
    'Reverse_Repo': rrp,
    'UST_10Y_Yield': 3.8 + yield_curve/100,  # Approximation
    'UST_2Y_Yield': 3.8 - yield_curve/100
}, index=dates)

# Calculate net liquidity (simplified - no TGA for demo)
data['Net_Liquidity'] = data['Fed_Balance_Sheet'] - data['Reverse_Repo']

print(f"✓ Generated {len(data)} days of mock data")
print()

# Step 2: Calculate quadrant positions
print("Step 2: Calculating quadrant positions...")

lookback = 252  # 1 year
data['DXY_zscore'] = (data['DXY'] - data['DXY'].rolling(lookback).mean()) / data['DXY'].rolling(lookback).std()
data['YieldCurve_zscore'] = (data['Yield_Curve_10Y2Y'] - data['Yield_Curve_10Y2Y'].rolling(lookback).mean()) / data['Yield_Curve_10Y2Y'].rolling(lookback).std()

def assign_quadrant(row):
    x, y = row['DXY_zscore'], row['YieldCurve_zscore']
    if pd.isna(x) or pd.isna(y):
        return 'Unknown'
    if x >= 0 and y >= 0:
        return 'Happiness Zone'
    elif x >= 0 and y < 0:
        return 'Hawkish Policy'
    elif x < 0 and y < 0:
        return 'Crisis Zone'
    else:
        return 'Dovish/Co-operative'

data['Quadrant'] = data.apply(assign_quadrant, axis=1)

print(f"✓ Quadrant positions calculated")
print()

# Show current position
current = data.iloc[-1]
print("Current Market Position (Mock Data - Dec 31, 2024):")
print("=" * 70)
print(f"  Quadrant: {current['Quadrant']}")
print(f"  DXY: {current['DXY']:.2f} (z-score: {current['DXY_zscore']:.2f})")
print(f"  10Y-2Y Spread: {current['Yield_Curve_10Y2Y']:.1f} bps (z-score: {current['YieldCurve_zscore']:.2f})")
print(f"  Bank Reserves: ${current['Bank_Excess_Reserves']:.0f}B")
print(f"  VIX: {current['VIX']:.1f}")
print(f"  Net Liquidity: ${current['Net_Liquidity']:.0f}B")
print()

# Interpretation
print("Interpretation:")
if current['Quadrant'] == 'Hawkish Policy':
    print("  ► You are in the HAWKISH POLICY quadrant (Bottom Right)")
    print("    - Rising dollar + Flattening curve")
    print("    - This matches the 2026 forecast direction!")
    print("    - Indicates tight monetary conditions")
    print("    - RMP interventions likely needed to support liquidity")
elif current['Quadrant'] == 'Happiness Zone':
    print("  ► You are in the HAPPINESS ZONE (Top Right)")
    print("    - Rising dollar + Steepening curve")
    print("    - Strong capital inflows")
    print("    - Favorable for risk assets")

print()

# Step 3: Create visualizations
print("Step 3: Creating visualizations...")
print()

# 3a: Quadrant Spider Diagram
print("  Creating quadrant spider diagram...")
fig, ax = plt.subplots(figsize=(12, 10))

# Filter recent data
recent_months = 12
cutoff_date = data.index[-1] - pd.DateOffset(months=recent_months)
df_recent = data[data.index >= cutoff_date].copy()

# Plot path
points = ax.scatter(df_recent['DXY_zscore'], df_recent['YieldCurve_zscore'],
                   c=range(len(df_recent)), cmap='plasma', s=50,
                   alpha=0.7, edgecolors='black', linewidth=0.5)

ax.plot(df_recent['DXY_zscore'], df_recent['YieldCurve_zscore'],
        '-', alpha=0.4, color='blue', linewidth=1.5)

# Mark current position
ax.scatter(current['DXY_zscore'], current['YieldCurve_zscore'],
          s=300, marker='*', color='red', edgecolors='black',
          linewidth=2, zorder=5, label='Current Position')

# Add quadrant labels
quadrant_labels = [
    (1.5, 1.5, "Happiness Zone\n(Strong Inflows)", 'green'),
    (1.5, -1.5, "Hawkish Policy\n(Tight Monetary)", 'orange'),
    (-1.5, -1.5, "Crisis Zone\n(Capital Flight)", 'red'),
    (-1.5, 1.5, "Dovish/Co-op\n(Loose Policy)", 'blue')
]

for x, y, label, color in quadrant_labels:
    ax.text(x, y, label, fontsize=11, ha='center', va='center',
           bbox=dict(boxstyle='round', facecolor=color, alpha=0.2))

# Axes
ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.3)
ax.axvline(x=0, color='black', linestyle='-', linewidth=1, alpha=0.3)

ax.set_xlabel('Exchange Rate (DXY) →\nFalling ← | → Rising', fontsize=12, fontweight='bold')
ax.set_ylabel('Yield Curve (10Y-2Y) →\nFlattening ← | → Steepening', fontsize=12, fontweight='bold')
ax.set_title('Macro-Valuation Quadrant Spider Diagram\n(Demo with Mock Data)',
            fontsize=14, fontweight='bold', pad=20)

plt.colorbar(points, ax=ax, label='Time (Recent to Latest)')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper left')
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)

plt.tight_layout()
output1 = '/home/user/pcrm-book/code/macro_analysis/demo_spider_diagram.png'
plt.savefig(output1, dpi=150, bbox_inches='tight')
print(f"  ✓ Spider diagram saved: demo_spider_diagram.png")
plt.close()

# 3b: Liquidity Dashboard
print("  Creating liquidity dashboard...")
fig, axes = plt.subplots(3, 2, figsize=(16, 12))

# 1. Bank Excess Reserves
ax = axes[0, 0]
ax.plot(data.index, data['Bank_Excess_Reserves'], linewidth=2, color='blue')
ax.fill_between(data.index, data['Bank_Excess_Reserves'], alpha=0.3, color='blue')
ax.axhline(y=3000, color='red', linestyle='--', alpha=0.5, label='Critical Level ($3T)')
ax.set_title('Bank Excess Reserves', fontweight='bold')
ax.set_ylabel('Billions USD')
ax.legend()
ax.grid(True, alpha=0.3)

# 2. Fed Balance Sheet vs RRP
ax = axes[0, 1]
ax.plot(data.index, data['Fed_Balance_Sheet']/1000, label='Fed Balance Sheet', linewidth=2)
ax.plot(data.index, data['Reverse_Repo']/1000, label='Reverse Repo', linewidth=2)
ax.set_title('Fed Balance Sheet vs Reverse Repo', fontweight='bold')
ax.set_ylabel('Trillions USD')
ax.legend()
ax.grid(True, alpha=0.3)

# 3. Net Liquidity
ax = axes[1, 0]
ax.plot(data.index, data['Net_Liquidity']/1000, linewidth=2, color='green')
ax.fill_between(data.index, data['Net_Liquidity']/1000, alpha=0.3, color='green')
ax.set_title('Net Liquidity (Fed BS - RRP)', fontweight='bold')
ax.set_ylabel('Trillions USD')
ax.grid(True, alpha=0.3)

# 4. Yield Curve
ax = axes[1, 1]
ax.plot(data.index, data['Yield_Curve_10Y2Y'], linewidth=2, color='purple')
ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax.fill_between(data.index, data['Yield_Curve_10Y2Y'], 0,
                 where=data['Yield_Curve_10Y2Y']>0, alpha=0.3, color='green')
ax.fill_between(data.index, data['Yield_Curve_10Y2Y'], 0,
                 where=data['Yield_Curve_10Y2Y']<=0, alpha=0.3, color='red')
ax.set_title('Yield Curve (10Y-2Y Spread)', fontweight='bold')
ax.set_ylabel('Basis Points')
ax.grid(True, alpha=0.3)

# 5. VIX
ax = axes[2, 0]
ax.plot(data.index, data['VIX'], linewidth=2, color='red')
ax.axhline(y=20, color='orange', linestyle='--', alpha=0.5, label='Elevated')
ax.axhline(y=30, color='red', linestyle='--', alpha=0.5, label='Crisis')
ax.fill_between(data.index, data['VIX'], 20,
                 where=data['VIX']>20, alpha=0.2, color='orange')
ax.fill_between(data.index, data['VIX'], 30,
                 where=data['VIX']>30, alpha=0.3, color='red')
ax.set_title('VIX (Market Stress)', fontweight='bold')
ax.set_ylabel('VIX Level')
ax.legend()
ax.grid(True, alpha=0.3)

# 6. DXY
ax = axes[2, 1]
ax.plot(data.index, data['DXY'], linewidth=2, color='darkgreen')
ax.fill_between(data.index, data['DXY'], alpha=0.3, color='darkgreen')
# Show +5% projection line
projection_start = data['DXY'].iloc[len(data)//2]
projection_end = projection_start * 1.05
ax.plot([data.index[len(data)//2], data.index[-1]],
        [projection_start, projection_end],
        'r--', linewidth=2, alpha=0.7, label='2026 Forecast (+5%)')
ax.set_title('US Dollar Index (DXY)', fontweight='bold')
ax.set_ylabel('Index Level')
ax.legend()
ax.grid(True, alpha=0.3)

plt.suptitle('Liquidity & Macro Dashboard (Demo)', fontsize=16, fontweight='bold', y=1.00)
plt.tight_layout()

output2 = '/home/user/pcrm-book/code/macro_analysis/demo_dashboard.png'
plt.savefig(output2, dpi=150, bbox_inches='tight')
print(f"  ✓ Dashboard saved: demo_dashboard.png")
plt.close()

print()

# Summary statistics
print("Step 4: Summary Statistics...")
print("=" * 70)
print()

# Quadrant distribution
quadrant_counts = data['Quadrant'].value_counts()
print("Time spent in each quadrant (2023-2024):")
for quadrant, count in quadrant_counts.items():
    if quadrant != 'Unknown':
        pct = (count / len(data[data['Quadrant'] != 'Unknown'])) * 100
        print(f"  {quadrant:20s}: {pct:5.1f}% ({count} days)")

print()

# Trends
print("Key Trends:")
dxy_change = ((data['DXY'].iloc[-1] / data['DXY'].iloc[0]) - 1) * 100
reserves_change = data['Bank_Excess_Reserves'].iloc[-1] - data['Bank_Excess_Reserves'].iloc[0]
liquidity_change = data['Net_Liquidity'].iloc[-1] - data['Net_Liquidity'].iloc[0]

dxy_trend = "strengthening" if dxy_change > 0 else "weakening"
reserves_trend = "declining" if reserves_change < 0 else "rising"
liquidity_trend = "tightening" if liquidity_change < 0 else "loosening"
print(f"  DXY Change: {dxy_change:+.2f}% ({dxy_trend})")
print(f"  Bank Reserves: ${reserves_change:+.0f}B ({reserves_trend})")
print(f"  Net Liquidity: ${liquidity_change:+.0f}B ({liquidity_trend})")

print()
print("=" * 70)
print("DEMO COMPLETE!")
print("=" * 70)
print()
print("✓✓✓ All functionality demonstrated successfully! ✓✓✓")
print()
print("Generated files:")
print(f"  1. {output1}")
print(f"  2. {output2}")
print()
print("This demo used mock data. With real FRED API access, you'll get:")
print("  ✓ Real-time market data")
print("  ✓ Historical accuracy")
print("  ✓ Daily updates")
print("  ✓ Fed policy tracking")
print()
print("Next steps:")
print("  1. Check the generated PNG files in code/macro_analysis/")
print("  2. Read MARKETS_TO_TRACK.md for the full tracking guide")
print("  3. Get a FRED API key (free): https://fred.stlouisfed.org/docs/api/api_key.html")
print("  4. Open rmp_liquidity_tracker.ipynb and add your API key")
print("  5. Start tracking real markets!")
print()
print("=" * 70)
