"""
Final Visualization: Compare All Strategy Improvements
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')

# Results data
results_data = {
    '2015-2026': {
        'SPY Benchmark': {'cagr': 13.44, 'sharpe': 0.76, 'max_dd': -33.72, 'alpha': 0.00},
        'Original': {'cagr': 8.34, 'sharpe': 0.66, 'max_dd': -30.45, 'alpha': -5.10},
        'V5: Quarterly': {'cagr': 9.87, 'sharpe': 0.87, 'max_dd': -18.49, 'alpha': -3.57},
        'Simplified': {'cagr': 5.40, 'sharpe': 0.52, 'max_dd': -23.90, 'alpha': -8.04},
        'Momentum Filter': {'cagr': 9.38, 'sharpe': 0.72, 'max_dd': -27.03, 'alpha': -4.06},
    },
    '2000-2014': {
        'SPY Benchmark': {'cagr': 4.31, 'sharpe': 0.21, 'max_dd': -55.19, 'alpha': 0.00},
        'Simplified': {'cagr': 1.95, 'sharpe': 0.13, 'max_dd': -49.15, 'alpha': -2.36},
        'Momentum Filter': {'cagr': 4.98, 'sharpe': 0.28, 'max_dd': -43.71, 'alpha': 0.67},
    }
}

# Create figure
fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

# Period 1: 2015-2026
strategies_2015 = list(results_data['2015-2026'].keys())
colors_2015 = ['black', 'red', 'orange', 'purple', 'green']

# 1. Alpha comparison 2015-2026
ax1 = fig.add_subplot(gs[0, 0])
alphas_2015 = [results_data['2015-2026'][s]['alpha'] for s in strategies_2015]
bars = ax1.barh(strategies_2015, alphas_2015, color=colors_2015, alpha=0.7)
ax1.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax1.set_xlabel('Alpha (%)', fontweight='bold')
ax1.set_title('2015-2026: Alpha vs SPY', fontweight='bold', fontsize=12)
ax1.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (bar, val) in enumerate(zip(bars, alphas_2015)):
    color = 'green' if val > 0 else 'red'
    ax1.text(val, bar.get_y() + bar.get_height()/2, f'{val:+.2f}%',
            ha='left' if val > 0 else 'right', va='center', fontweight='bold',
            color=color, fontsize=9)

# 2. Sharpe ratio comparison 2015-2026
ax2 = fig.add_subplot(gs[0, 1])
sharpes_2015 = [results_data['2015-2026'][s]['sharpe'] for s in strategies_2015]
bars = ax2.barh(strategies_2015, sharpes_2015, color=colors_2015, alpha=0.7)
ax2.set_xlabel('Sharpe Ratio', fontweight='bold')
ax2.set_title('2015-2026: Risk-Adjusted Returns', fontweight='bold', fontsize=12)
ax2.grid(True, alpha=0.3, axis='x')

# Add value labels
for bar, val in zip(bars, sharpes_2015):
    ax2.text(val + 0.02, bar.get_y() + bar.get_height()/2, f'{val:.2f}',
            ha='left', va='center', fontsize=9)

# 3. Max drawdown comparison 2015-2026
ax3 = fig.add_subplot(gs[0, 2])
maxdds_2015 = [results_data['2015-2026'][s]['max_dd'] for s in strategies_2015]
bars = ax3.barh(strategies_2015, maxdds_2015, color=colors_2015, alpha=0.7)
ax3.set_xlabel('Max Drawdown (%)', fontweight='bold')
ax3.set_title('2015-2026: Downside Risk', fontweight='bold', fontsize=12)
ax3.grid(True, alpha=0.3, axis='x')

# Add value labels
for bar, val in zip(bars, maxdds_2015):
    ax3.text(val - 1, bar.get_y() + bar.get_height()/2, f'{val:.1f}%',
            ha='right', va='center', fontsize=9, color='white', fontweight='bold')

# Period 2: 2000-2014
strategies_2000 = list(results_data['2000-2014'].keys())
colors_2000 = ['black', 'purple', 'green']

# 4. Alpha comparison 2000-2014
ax4 = fig.add_subplot(gs[1, 0])
alphas_2000 = [results_data['2000-2014'][s]['alpha'] for s in strategies_2000]
bars = ax4.barh(strategies_2000, alphas_2000, color=colors_2000, alpha=0.7)
ax4.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax4.set_xlabel('Alpha (%)', fontweight='bold')
ax4.set_title('2000-2014: Alpha vs SPY', fontweight='bold', fontsize=12)
ax4.grid(True, alpha=0.3, axis='x')

# Add value labels - highlight positive alpha
for bar, val in zip(bars, alphas_2000):
    color = 'green' if val > 0 else 'red'
    style = 'italic' if val > 0 else 'normal'
    weight = 'bold'
    ax4.text(val, bar.get_y() + bar.get_height()/2, f'{val:+.2f}%',
            ha='left' if val > 0 else 'right', va='center',
            color=color, fontsize=10, fontweight=weight, fontstyle=style)

# Add annotation for positive alpha
if any(a > 0 for a in alphas_2000):
    ax4.text(0.98, 0.95, 'POSITIVE ALPHA!',
            transform=ax4.transAxes, ha='right', va='top',
            bbox=dict(boxstyle='round', facecolor='green', alpha=0.3),
            fontsize=11, fontweight='bold', color='darkgreen')

# 5. Sharpe ratio comparison 2000-2014
ax5 = fig.add_subplot(gs[1, 1])
sharpes_2000 = [results_data['2000-2014'][s]['sharpe'] for s in strategies_2000]
bars = ax5.barh(strategies_2000, sharpes_2000, color=colors_2000, alpha=0.7)
ax5.set_xlabel('Sharpe Ratio', fontweight='bold')
ax5.set_title('2000-2014: Risk-Adjusted Returns', fontweight='bold', fontsize=12)
ax5.grid(True, alpha=0.3, axis='x')

# Add value labels
for bar, val in zip(bars, sharpes_2000):
    ax5.text(val + 0.01, bar.get_y() + bar.get_height()/2, f'{val:.2f}',
            ha='left', va='center', fontsize=9)

# 6. Max drawdown comparison 2000-2014
ax6 = fig.add_subplot(gs[1, 2])
maxdds_2000 = [results_data['2000-2014'][s]['max_dd'] for s in strategies_2000]
bars = ax6.barh(strategies_2000, maxdds_2000, color=colors_2000, alpha=0.7)
ax6.set_xlabel('Max Drawdown (%)', fontweight='bold')
ax6.set_title('2000-2014: Downside Risk', fontweight='bold', fontsize=12)
ax6.grid(True, alpha=0.3, axis='x')

# Add value labels
for bar, val in zip(bars, maxdds_2000):
    ax6.text(val - 1.5, bar.get_y() + bar.get_height()/2, f'{val:.1f}%',
            ha='right', va='center', fontsize=9, color='white', fontweight='bold')

plt.suptitle('Complete Strategy Comparison: All Improvements Across Two Decades',
             fontsize=16, fontweight='bold', y=0.98)

plt.savefig('final_comparison.png', dpi=300, bbox_inches='tight')
print("[OK] Final comparison chart saved to final_comparison.png")
plt.close()

# Create summary table
print("\n" + "="*80)
print("COMPLETE RESULTS SUMMARY")
print("="*80)

print("\n2015-2026 (BULL MARKET ERA):")
print("-" * 80)
print(f"{'Strategy':<20} {'CAGR':>8} {'Alpha':>8} {'Sharpe':>8} {'Max DD':>10}")
print("-" * 80)
for strategy in strategies_2015:
    data = results_data['2015-2026'][strategy]
    print(f"{strategy:<20} {data['cagr']:>7.2f}% {data['alpha']:>7.2f}% {data['sharpe']:>8.2f} {data['max_dd']:>9.2f}%")

print("\n2000-2014 (VOLATILE MARKET ERA):")
print("-" * 80)
print(f"{'Strategy':<20} {'CAGR':>8} {'Alpha':>8} {'Sharpe':>8} {'Max DD':>10}")
print("-" * 80)
for strategy in strategies_2000:
    data = results_data['2000-2014'][strategy]
    marker = " <-- BEATS SPY!" if data['alpha'] > 0 else ""
    print(f"{strategy:<20} {data['cagr']:>7.2f}% {data['alpha']:>7.2f}% {data['sharpe']:>8.2f} {data['max_dd']:>9.2f}%{marker}")

print("\n" + "="*80)
print("KEY INSIGHTS:")
print("="*80)
print("1. Momentum Filter achieved +0.67% alpha in 2000-2014 (FIRST POSITIVE ALPHA!)")
print("2. Quarterly rebalancing (V5) best for 2015-2026 (-3.57% alpha, Sharpe 0.87)")
print("3. Simplified strategy failed in bull market (-8.04%) but better in volatile (-2.36%)")
print("4. Framework WORKS in volatile markets, FAILS in secular bull markets")
print("5. All strategies reduced max drawdown vs SPY")
print("="*80)

print("\n[OK] Complete analysis finished!")
