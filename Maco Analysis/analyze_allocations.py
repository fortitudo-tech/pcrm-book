"""
Analyze which quadrant allocations hurt/helped performance

This script tests each quadrant's allocation separately to identify
which specific ETF mappings are working and which need adjustment.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from backtest_strategy import (
    QUADRANT_ALLOCATIONS,
    run_backtest
)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')


def analyze_quadrant_allocations(results_file='backtest_results_10yr.csv'):
    """
    Analyze performance during each quadrant period.

    Parameters:
        results_file: CSV file from original backtest
    """
    print("=" * 70)
    print("QUADRANT ALLOCATION ANALYSIS")
    print("=" * 70)

    # Load results
    results = pd.read_csv(results_file, index_col=0, parse_dates=True)

    # Calculate daily returns
    results['Strategy_Daily_Return'] = results['Strategy_Value'].pct_change() * 100
    results['Benchmark_Daily_Return'] = results['Benchmark_Value'].pct_change() * 100
    results['Alpha_Daily'] = results['Strategy_Daily_Return'] - results['Benchmark_Daily_Return']

    # Analyze each quadrant
    quadrant_performance = {}

    for quadrant in ['Dovish/Co-operative', 'Happiness Zone', 'Hawkish Policy', 'Crisis Zone']:
        quad_data = results[results['Quadrant'] == quadrant].copy()

        if len(quad_data) == 0:
            continue

        days = len(quad_data)
        pct_time = days / len(results) * 100

        # Calculate cumulative returns in this quadrant
        strategy_cumret = ((quad_data['Strategy_Value'].iloc[-1] / quad_data['Strategy_Value'].iloc[0]) - 1) * 100
        benchmark_cumret = ((quad_data['Benchmark_Value'].iloc[-1] / quad_data['Benchmark_Value'].iloc[0]) - 1) * 100

        # Average daily returns
        avg_strategy = quad_data['Strategy_Daily_Return'].mean()
        avg_benchmark = quad_data['Benchmark_Daily_Return'].mean()
        avg_alpha = quad_data['Alpha_Daily'].mean()

        # Volatility
        vol_strategy = quad_data['Strategy_Daily_Return'].std()
        vol_benchmark = quad_data['Benchmark_Daily_Return'].std()

        # Win rate (days strategy beat benchmark)
        wins = (quad_data['Strategy_Daily_Return'] > quad_data['Benchmark_Daily_Return']).sum()
        win_rate = wins / days * 100

        quadrant_performance[quadrant] = {
            'days': days,
            'pct_time': pct_time,
            'strategy_cumret': strategy_cumret,
            'benchmark_cumret': benchmark_cumret,
            'alpha_cumulative': strategy_cumret - benchmark_cumret,
            'avg_daily_strategy': avg_strategy,
            'avg_daily_benchmark': avg_benchmark,
            'avg_daily_alpha': avg_alpha,
            'vol_strategy': vol_strategy,
            'vol_benchmark': vol_benchmark,
            'win_rate': win_rate,
            'allocation': QUADRANT_ALLOCATIONS[quadrant]
        }

    # Print detailed analysis
    print("\nDETAILED QUADRANT PERFORMANCE:\n")

    for quadrant, perf in quadrant_performance.items():
        print("=" * 70)
        print(f"{quadrant}")
        print("=" * 70)
        print(f"Time spent:          {perf['days']} days ({perf['pct_time']:.1f}%)")
        print(f"Cumulative Return:   Strategy: {perf['strategy_cumret']:+.2f}%  |  SPY: {perf['benchmark_cumret']:+.2f}%")
        print(f"Alpha (cumulative):  {perf['alpha_cumulative']:+.2f}%")
        print(f"Avg Daily Return:    Strategy: {perf['avg_daily_strategy']:+.3f}%  |  SPY: {perf['avg_daily_benchmark']:+.3f}%")
        print(f"Avg Daily Alpha:     {perf['avg_daily_alpha']:+.3f}%")
        print(f"Daily Volatility:    Strategy: {perf['vol_strategy']:.3f}%  |  SPY: {perf['vol_benchmark']:.3f}%")
        print(f"Win Rate:            {perf['win_rate']:.1f}%")
        print(f"\nAllocation:")
        for etf, weight in sorted(perf['allocation'].items(), key=lambda x: -x[1]):
            print(f"  {etf:5s}: {weight*100:5.1f}%")
        print()

    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    quadrants = list(quadrant_performance.keys())
    colors = ['blue', 'green', 'orange', 'red']

    # 1. Cumulative alpha by quadrant
    ax1 = axes[0, 0]
    alpha_values = [quadrant_performance[q]['alpha_cumulative'] for q in quadrants]
    bars = ax1.bar(range(len(quadrants)), alpha_values, color=colors)
    ax1.axhline(y=0, color='black', linestyle='--', linewidth=1)
    ax1.set_xticks(range(len(quadrants)))
    ax1.set_xticklabels([q.replace(' ', '\n') for q in quadrants], fontsize=9)
    ax1.set_ylabel('Cumulative Alpha (%)')
    ax1.set_title('Cumulative Alpha by Quadrant\n(Negative = Underperformance)', fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, alpha_values)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%', ha='center', va='bottom' if val > 0 else 'top', fontsize=10)

    # 2. Average daily alpha by quadrant
    ax2 = axes[0, 1]
    daily_alpha = [quadrant_performance[q]['avg_daily_alpha'] for q in quadrants]
    bars = ax2.bar(range(len(quadrants)), daily_alpha, color=colors)
    ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
    ax2.set_xticks(range(len(quadrants)))
    ax2.set_xticklabels([q.replace(' ', '\n') for q in quadrants], fontsize=9)
    ax2.set_ylabel('Avg Daily Alpha (%)')
    ax2.set_title('Average Daily Alpha by Quadrant', fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for bar, val in zip(bars, daily_alpha):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.3f}%', ha='center', va='bottom' if val > 0 else 'top', fontsize=9)

    # 3. Win rate by quadrant
    ax3 = axes[1, 0]
    win_rates = [quadrant_performance[q]['win_rate'] for q in quadrants]
    bars = ax3.bar(range(len(quadrants)), win_rates, color=colors)
    ax3.axhline(y=50, color='black', linestyle='--', linewidth=1, label='50% (Random)')
    ax3.set_xticks(range(len(quadrants)))
    ax3.set_xticklabels([q.replace(' ', '\n') for q in quadrants], fontsize=9)
    ax3.set_ylabel('Win Rate (%)')
    ax3.set_title('Win Rate vs SPY by Quadrant', fontweight='bold')
    ax3.set_ylim([0, 100])
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for bar, val in zip(bars, win_rates):
        ax3.text(bar.get_x() + bar.get_width()/2., val + 2,
                f'{val:.1f}%', ha='center', fontsize=9)

    # 4. Allocation diversity (number of holdings)
    ax4 = axes[1, 1]

    # Calculate effective number of holdings (inverse of Herfindahl index)
    def effective_holdings(allocation):
        weights = [w for k, w in allocation.items() if k != 'CASH']
        if not weights:
            return 0
        hhi = sum(w**2 for w in weights)
        return 1 / hhi if hhi > 0 else 0

    n_holdings = [len([w for k, w in quadrant_performance[q]['allocation'].items() if k != 'CASH'])
                  for q in quadrants]
    eff_holdings = [effective_holdings(quadrant_performance[q]['allocation']) for q in quadrants]

    x = np.arange(len(quadrants))
    width = 0.35

    bars1 = ax4.bar(x - width/2, n_holdings, width, label='Number of ETFs', color='steelblue')
    bars2 = ax4.bar(x + width/2, eff_holdings, width, label='Effective N (Diversity)', color='coral')

    ax4.set_xticks(x)
    ax4.set_xticklabels([q.replace(' ', '\n') for q in quadrants], fontsize=9)
    ax4.set_ylabel('Count')
    ax4.set_title('Portfolio Concentration by Quadrant', fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')

    plt.suptitle('Quadrant Allocation Performance Analysis\n(Identifying Problem Allocations)',
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('quadrant_allocation_analysis.png', dpi=300, bbox_inches='tight')
    print("\n[OK] Analysis chart saved to quadrant_allocation_analysis.png")
    plt.close()

    # Identify worst performers
    print("\n" + "=" * 70)
    print("SUMMARY: WORST PERFORMING QUADRANTS")
    print("=" * 70)

    sorted_quads = sorted(quadrant_performance.items(),
                         key=lambda x: x[1]['alpha_cumulative'])

    for i, (quadrant, perf) in enumerate(sorted_quads, 1):
        print(f"{i}. {quadrant}")
        print(f"   Alpha: {perf['alpha_cumulative']:+.2f}% | Daily: {perf['avg_daily_alpha']:+.3f}% | Win Rate: {perf['win_rate']:.1f}%")
        if perf['alpha_cumulative'] < -10:
            print(f"   WARNING: MAJOR UNDERPERFORMANCE - Review allocation strategy")

    print("\n" + "=" * 70)
    print("RECOMMENDATIONS:")
    print("=" * 70)

    for quadrant, perf in quadrant_performance.items():
        if perf['alpha_cumulative'] < -10:
            print(f"\n{quadrant}:")
            print(f"  Problem: Cumulative alpha of {perf['alpha_cumulative']:.2f}%")
            print(f"  Current allocation emphasizes:")
            top_3 = sorted(perf['allocation'].items(), key=lambda x: -x[1])[:3]
            for etf, weight in top_3:
                if etf != 'CASH':
                    print(f"    - {etf} ({weight*100:.0f}%)")
            print(f"  Consider: Increasing SPY weight, reducing sector concentration")


if __name__ == "__main__":
    analyze_quadrant_allocations('backtest_results_10yr.csv')
