"""
Quick 3-year backtest to validate the strategy works
"""
from backtest_strategy import run_backtest, plot_backtest_results, plot_quadrant_performance

if __name__ == "__main__":
    print("Running quick 3-year backtest (2022-2024)...")
    print("This will help identify issues faster than 10-year backtest\n")

    results = run_backtest(
        start_date='2022-01-01',
        end_date='2024-12-31',
        initial_capital=100000,
        rebalance_frequency='monthly',
        transaction_cost=0.001
    )

    print("\nGenerating charts...")
    plot_backtest_results(results)
    plot_quadrant_performance(results)

    print("\n[OK] Quick backtest complete!")
