"""
Full 10-year backtest - Results only (no plots for now)
"""
from backtest_strategy import run_backtest

if __name__ == "__main__":
    results = run_backtest(
        start_date='2015-01-01',
        end_date=None,
        initial_capital=100000,
        rebalance_frequency='monthly',
        transaction_cost=0.001
    )

    # Save results
    results.to_csv('backtest_results_10yr.csv')
    print("\n[OK] Results saved to backtest_results_10yr.csv")

    # Print summary statistics by quadrant
    print("\n" + "="*70)
    print("PERFORMANCE BY QUADRANT")
    print("="*70)

    for quadrant in results['Quadrant'].unique():
        if quadrant != 'Unknown':
            quad_data = results[results['Quadrant'] == quadrant]
            days = len(quad_data)
            pct_time = days / len(results) * 100

            if days > 1:
                quad_returns = quad_data['Strategy_Value'].pct_change()
                avg_daily_return = quad_returns.mean() * 100

                print(f"\n{quadrant}:")
                print(f"  Days in quadrant: {days} ({pct_time:.1f}% of time)")
                print(f"  Avg daily return: {avg_daily_return:.3f}%")
