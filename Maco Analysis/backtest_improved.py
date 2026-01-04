"""
Improved Backtest with Multiple Strategy Variants

Tests 3 improvements:
1. Z-score bands (require stronger signal to switch quadrants)
2. Holding period requirements (prevent whipsaw)
3. Alternative rebalancing frequencies and transaction costs
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import yfinance as yf
from rmp_liquidity_tracker import (
    fetch_all_data,
    calculate_momentum_indicators
)
from backtest_strategy import (
    QUADRANT_ALLOCATIONS,
    fetch_etf_prices,
    plot_backtest_results
)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def calculate_quadrant_with_bands(df, lookback_period=252, z_threshold=0.5):
    """
    Calculate quadrant position with z-score bands to reduce whipsaw.

    Parameters:
        df: DataFrame with market indicators
        lookback_period: Period for z-score normalization
        z_threshold: Minimum absolute z-score to assign strong signal (default: 0.5)

    Returns:
        DataFrame with quadrant assignments
    """
    result = df.copy()

    # Calculate z-scores (same as original)
    if 'DXY' in result.columns:
        dxy_valid = result['DXY'].dropna()
        if len(dxy_valid) >= lookback_period:
            dxy_mean = dxy_valid.rolling(lookback_period, min_periods=lookback_period).mean()
            dxy_std = dxy_valid.rolling(lookback_period, min_periods=lookback_period).std()
            dxy_zscore = (dxy_valid - dxy_mean) / dxy_std
            result['DXY_zscore'] = dxy_zscore.reindex(result.index)
        else:
            result['DXY_zscore'] = np.nan
    else:
        result['DXY_zscore'] = np.nan

    if 'Yield_Curve_10Y2Y' in result.columns:
        yc_valid = result['Yield_Curve_10Y2Y'].dropna()
        if len(yc_valid) >= lookback_period:
            yc_mean = yc_valid.rolling(lookback_period, min_periods=lookback_period).mean()
            yc_std = yc_valid.rolling(lookback_period, min_periods=lookback_period).std()
            yc_zscore = (yc_valid - yc_mean) / yc_std
            result['YieldCurve_zscore'] = yc_zscore.reindex(result.index)
        else:
            result['YieldCurve_zscore'] = np.nan
    else:
        result['YieldCurve_zscore'] = np.nan

    # Assign quadrants with threshold bands
    def assign_quadrant_with_threshold(row, threshold):
        x, y = row.get('DXY_zscore'), row.get('YieldCurve_zscore')

        if pd.isna(x) or pd.isna(y):
            return 'Unknown'

        # Require stronger signals - only assign if z-score exceeds threshold
        x_strong = x if abs(x) >= threshold else 0
        y_strong = y if abs(y) >= threshold else 0

        if x_strong >= 0 and y_strong >= 0:
            return 'Happiness Zone'
        elif x_strong >= 0 and y_strong < 0:
            return 'Hawkish Policy'
        elif x_strong < 0 and y_strong < 0:
            return 'Crisis Zone'
        elif x_strong < 0 and y_strong >= 0:
            return 'Dovish/Co-operative'
        else:
            # Neutral zone - both z-scores weak
            return 'Unknown'

    result['Quadrant'] = result.apply(lambda row: assign_quadrant_with_threshold(row, z_threshold), axis=1)

    return result


def apply_holding_period_filter(quadrants, min_days=20):
    """
    Apply holding period requirement - only switch quadrants if new quadrant
    persists for min_days.

    Parameters:
        quadrants: Series of quadrant assignments by date
        min_days: Minimum days to confirm new quadrant

    Returns:
        Series with filtered quadrant assignments
    """
    filtered = quadrants.copy()
    current_quadrant = quadrants.iloc[0]
    days_in_new = 0
    pending_quadrant = None

    for i in range(1, len(quadrants)):
        new_quadrant = quadrants.iloc[i]

        if new_quadrant == current_quadrant:
            # Stay in current quadrant
            days_in_new = 0
            pending_quadrant = None
        elif new_quadrant == pending_quadrant:
            # Continue accumulating days in new quadrant
            days_in_new += 1
            if days_in_new >= min_days:
                # Confirmed - switch
                current_quadrant = new_quadrant
                days_in_new = 0
                pending_quadrant = None
        else:
            # New quadrant appeared
            pending_quadrant = new_quadrant
            days_in_new = 1

        filtered.iloc[i] = current_quadrant

    return filtered


def run_improved_backtest(start_date='2015-01-01', end_date=None, initial_capital=100000,
                          rebalance_frequency='monthly', transaction_cost=0.001,
                          z_threshold=0.5, min_holding_days=20,
                          strategy_name="Improved Strategy"):
    """
    Run backtest with improvements.

    Parameters:
        start_date: Start date for backtest
        end_date: End date for backtest (default: today)
        initial_capital: Starting capital in USD
        rebalance_frequency: 'daily', 'weekly', or 'monthly'
        transaction_cost: Transaction cost as fraction (0.001 = 0.1%)
        z_threshold: Minimum z-score magnitude to assign quadrant (0 = no threshold)
        min_holding_days: Minimum days before switching quadrants (0 = no filter)
        strategy_name: Name for reporting

    Returns:
        DataFrame with backtest results
    """
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')

    print("=" * 70)
    print(f"BACKTESTING: {strategy_name}")
    print("=" * 70)
    print(f"Period: {start_date} to {end_date}")
    print(f"Initial Capital: ${initial_capital:,.0f}")
    print(f"Rebalance Frequency: {rebalance_frequency}")
    print(f"Transaction Cost: {transaction_cost*100:.2f}%")
    print(f"Z-score Threshold: {z_threshold}")
    print(f"Min Holding Days: {min_holding_days}\n")

    # Fetch macro data
    print("Fetching macro data...")
    macro_data = fetch_all_data(start_date=start_date, end_date=end_date)

    # Calculate quadrants with bands
    macro_data = calculate_quadrant_with_bands(macro_data, z_threshold=z_threshold)

    # Apply holding period filter if specified
    if min_holding_days > 0:
        macro_data['Quadrant'] = apply_holding_period_filter(macro_data['Quadrant'], min_holding_days)

    macro_data = calculate_momentum_indicators(macro_data)

    # Fetch ETF prices
    etf_prices = fetch_etf_prices(start_date, end_date)

    # Align dates
    common_dates = macro_data.index.intersection(etf_prices.index)
    macro_data = macro_data.loc[common_dates]
    etf_prices = etf_prices.loc[common_dates]

    print(f"\n[OK] Backtest data prepared: {len(common_dates)} trading days\n")

    # Initialize portfolios
    results = []

    # Strategy portfolio
    strategy_capital = initial_capital
    strategy_holdings = {}
    last_rebalance_date = None

    # Benchmark portfolio (buy-and-hold SPY)
    spy_shares = initial_capital / etf_prices['SPY'].iloc[0]

    # Track statistics
    trades = 0
    quadrant_changes = 0
    last_quadrant = None

    # Rebalance schedule
    def should_rebalance(current_date, last_date, frequency):
        if last_date is None:
            return True
        if frequency == 'daily':
            return True
        elif frequency == 'weekly':
            return (current_date - last_date).days >= 7
        elif frequency == 'monthly':
            return current_date.month != last_date.month
        elif frequency == 'quarterly':
            return (current_date.month - 1) // 3 != (last_date.month - 1) // 3
        return False

    # Main backtest loop
    for date in common_dates:
        current_quadrant = macro_data.loc[date, 'Quadrant']

        # Track quadrant changes
        if last_quadrant is not None and current_quadrant != last_quadrant:
            quadrant_changes += 1
        last_quadrant = current_quadrant

        # Check if rebalancing is needed
        needs_rebalance = should_rebalance(date, last_rebalance_date, rebalance_frequency)

        if needs_rebalance:
            # Get target allocation for current quadrant
            target_allocation = QUADRANT_ALLOCATIONS.get(current_quadrant,
                                                         QUADRANT_ALLOCATIONS['Unknown'])

            # Calculate current portfolio value
            portfolio_value = strategy_capital
            for etf, shares in strategy_holdings.items():
                if etf in etf_prices.columns and not pd.isna(etf_prices.loc[date, etf]):
                    portfolio_value += shares * etf_prices.loc[date, etf]

            # Sell all current holdings
            for etf, shares in strategy_holdings.items():
                if etf in etf_prices.columns and not pd.isna(etf_prices.loc[date, etf]):
                    proceeds = shares * etf_prices.loc[date, etf]
                    strategy_capital += proceeds * (1 - transaction_cost)
                    trades += 1

            strategy_holdings = {}

            # Buy new allocation
            for etf, weight in target_allocation.items():
                if etf == 'CASH':
                    continue

                if etf in etf_prices.columns and not pd.isna(etf_prices.loc[date, etf]):
                    target_value = portfolio_value * weight
                    cost_with_fees = target_value * (1 + transaction_cost)

                    if strategy_capital >= cost_with_fees:
                        shares = target_value / etf_prices.loc[date, etf]
                        strategy_holdings[etf] = shares
                        strategy_capital -= cost_with_fees
                        trades += 1

            last_rebalance_date = date

        # Calculate strategy portfolio value
        strategy_value = strategy_capital
        for etf, shares in strategy_holdings.items():
            if etf in etf_prices.columns and not pd.isna(etf_prices.loc[date, etf]):
                strategy_value += shares * etf_prices.loc[date, etf]

        # Calculate benchmark value
        benchmark_value = spy_shares * etf_prices.loc[date, 'SPY']

        # Store results
        results.append({
            'Date': date,
            'Quadrant': current_quadrant,
            'Strategy_Value': strategy_value,
            'Benchmark_Value': benchmark_value,
            'Strategy_Return': (strategy_value / initial_capital - 1) * 100,
            'Benchmark_Return': (benchmark_value / initial_capital - 1) * 100,
            'Outperformance': (strategy_value / benchmark_value - 1) * 100,
            'DXY_zscore': macro_data.loc[date, 'DXY_zscore'],
            'YieldCurve_zscore': macro_data.loc[date, 'YieldCurve_zscore'],
        })

    # Create results DataFrame
    df_results = pd.DataFrame(results)
    df_results.set_index('Date', inplace=True)

    # Calculate performance metrics
    print("=" * 70)
    print("BACKTEST RESULTS")
    print("=" * 70)

    final_strategy = df_results['Strategy_Value'].iloc[-1]
    final_benchmark = df_results['Benchmark_Value'].iloc[-1]

    strategy_return = (final_strategy / initial_capital - 1) * 100
    benchmark_return = (final_benchmark / initial_capital - 1) * 100
    outperformance = strategy_return - benchmark_return

    # Calculate annualized returns
    years = (df_results.index[-1] - df_results.index[0]).days / 365.25
    strategy_cagr = ((final_strategy / initial_capital) ** (1/years) - 1) * 100
    benchmark_cagr = ((final_benchmark / initial_capital) ** (1/years) - 1) * 100

    # Calculate volatility (annualized)
    strategy_daily_returns = df_results['Strategy_Value'].pct_change()
    benchmark_daily_returns = df_results['Benchmark_Value'].pct_change()

    strategy_vol = strategy_daily_returns.std() * np.sqrt(252) * 100
    benchmark_vol = benchmark_daily_returns.std() * np.sqrt(252) * 100

    # Calculate Sharpe ratio (assuming 0% risk-free rate)
    strategy_sharpe = strategy_cagr / strategy_vol if strategy_vol > 0 else 0
    benchmark_sharpe = benchmark_cagr / benchmark_vol if benchmark_vol > 0 else 0

    # Calculate maximum drawdown
    def calculate_max_drawdown(values):
        cummax = values.cummax()
        drawdown = (values - cummax) / cummax * 100
        return drawdown.min()

    strategy_max_dd = calculate_max_drawdown(df_results['Strategy_Value'])
    benchmark_max_dd = calculate_max_drawdown(df_results['Benchmark_Value'])

    print(f"\nPeriod: {years:.2f} years ({df_results.index[0].date()} to {df_results.index[-1].date()})")
    print(f"Number of rebalances: {trades // 2}")
    print(f"Quadrant changes: {quadrant_changes}")
    print()

    print("STRATEGY PERFORMANCE:")
    print(f"  Final Value:        ${final_strategy:,.2f}")
    print(f"  Total Return:       {strategy_return:.2f}%")
    print(f"  CAGR:              {strategy_cagr:.2f}%")
    print(f"  Volatility:        {strategy_vol:.2f}%")
    print(f"  Sharpe Ratio:      {strategy_sharpe:.2f}")
    print(f"  Max Drawdown:      {strategy_max_dd:.2f}%")
    print()

    print("BENCHMARK (SPY) PERFORMANCE:")
    print(f"  Final Value:        ${final_benchmark:,.2f}")
    print(f"  Total Return:       {benchmark_return:.2f}%")
    print(f"  CAGR:              {benchmark_cagr:.2f}%")
    print(f"  Volatility:        {benchmark_vol:.2f}%")
    print(f"  Sharpe Ratio:      {benchmark_sharpe:.2f}")
    print(f"  Max Drawdown:      {benchmark_max_dd:.2f}%")
    print()

    print("RELATIVE PERFORMANCE:")
    print(f"  Outperformance:    {outperformance:.2f}%")
    print(f"  CAGR Difference:   {strategy_cagr - benchmark_cagr:.2f}%")
    print(f"  Alpha:             {strategy_cagr - benchmark_cagr:.2f}%")
    print()

    print("=" * 70)

    # Store metrics in results
    df_results.attrs['strategy_name'] = strategy_name
    df_results.attrs['final_value'] = final_strategy
    df_results.attrs['cagr'] = strategy_cagr
    df_results.attrs['volatility'] = strategy_vol
    df_results.attrs['sharpe'] = strategy_sharpe
    df_results.attrs['max_dd'] = strategy_max_dd
    df_results.attrs['alpha'] = strategy_cagr - benchmark_cagr
    df_results.attrs['trades'] = trades
    df_results.attrs['quadrant_changes'] = quadrant_changes

    return df_results


def compare_strategies(results_list, strategy_names):
    """
    Compare multiple strategy variants.

    Parameters:
        results_list: List of result DataFrames
        strategy_names: List of strategy names
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']

    # 1. Portfolio values over time
    ax1 = axes[0, 0]
    for i, (results, name) in enumerate(zip(results_list, strategy_names)):
        ax1.plot(results.index, results['Strategy_Value'], label=name,
                linewidth=2, color=colors[i % len(colors)])
    ax1.plot(results_list[0].index, results_list[0]['Benchmark_Value'],
            label='SPY Benchmark', linewidth=2, color='black', linestyle='--')
    ax1.set_title('Portfolio Value Comparison', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Portfolio Value ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

    # 2. Cumulative returns
    ax2 = axes[0, 1]
    for i, (results, name) in enumerate(zip(results_list, strategy_names)):
        ax2.plot(results.index, results['Strategy_Return'], label=name,
                linewidth=2, color=colors[i % len(colors)])
    ax2.plot(results_list[0].index, results_list[0]['Benchmark_Return'],
            label='SPY Benchmark', linewidth=2, color='black', linestyle='--')
    ax2.set_title('Cumulative Returns Comparison', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Return (%)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. Performance metrics comparison
    ax3 = axes[1, 0]
    metrics = ['CAGR', 'Volatility', 'Sharpe', 'Max DD', 'Alpha']
    x = np.arange(len(metrics))
    width = 0.15

    for i, results in enumerate(results_list):
        values = [
            results.attrs['cagr'],
            results.attrs['volatility'],
            results.attrs['sharpe'] * 5,  # Scale for visibility
            abs(results.attrs['max_dd']),
            results.attrs['alpha']
        ]
        ax3.bar(x + i*width, values, width, label=strategy_names[i],
               color=colors[i % len(colors)])

    # Add benchmark
    bench_cagr = ((results_list[0]['Benchmark_Value'].iloc[-1] / 100000) ** (1/11) - 1) * 100
    bench_vol = results_list[0]['Benchmark_Value'].pct_change().std() * np.sqrt(252) * 100
    bench_sharpe = bench_cagr / bench_vol
    bench_dd = ((results_list[0]['Benchmark_Value'] - results_list[0]['Benchmark_Value'].cummax()) /
                results_list[0]['Benchmark_Value'].cummax() * 100).min()

    bench_values = [bench_cagr, bench_vol, bench_sharpe * 5, abs(bench_dd), 0]
    ax3.bar(x + len(results_list)*width, bench_values, width, label='SPY Benchmark',
           color='black', alpha=0.5)

    ax3.set_ylabel('Value')
    ax3.set_title('Performance Metrics Comparison', fontsize=12, fontweight='bold')
    ax3.set_xticks(x + width * len(results_list) / 2)
    ax3.set_xticklabels(metrics)
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

    # 4. Trading activity comparison
    ax4 = axes[1, 1]
    trades = [r.attrs['trades'] // 2 for r in results_list]
    quad_changes = [r.attrs['quadrant_changes'] for r in results_list]

    x = np.arange(len(strategy_names))
    width = 0.35

    ax4.bar(x - width/2, trades, width, label='Rebalances', color='steelblue')
    ax4.bar(x + width/2, quad_changes, width, label='Quadrant Changes', color='coral')

    ax4.set_ylabel('Count')
    ax4.set_title('Trading Activity Comparison', fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(strategy_names, rotation=15, ha='right')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')

    plt.suptitle('Strategy Comparison Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('strategy_comparison.png', dpi=300, bbox_inches='tight')
    print("\n[OK] Comparison chart saved to strategy_comparison.png")
    plt.close()


# =============================================================================
# Main Execution - Test Multiple Variants
# =============================================================================

if __name__ == "__main__":

    results_list = []
    strategy_names = []

    # Original strategy (for comparison)
    print("\n" + "="*70)
    print("RUNNING STRATEGY VARIANTS")
    print("="*70 + "\n")

    # Variant 1: Original (z-threshold=0, no holding period)
    r1 = run_improved_backtest(
        start_date='2015-01-01',
        z_threshold=0.0,
        min_holding_days=0,
        rebalance_frequency='monthly',
        transaction_cost=0.001,
        strategy_name="V1: Original Strategy"
    )
    results_list.append(r1)
    strategy_names.append("Original")

    # Variant 2: Z-score bands (threshold=0.5)
    r2 = run_improved_backtest(
        start_date='2015-01-01',
        z_threshold=0.5,
        min_holding_days=0,
        rebalance_frequency='monthly',
        transaction_cost=0.001,
        strategy_name="V2: Z-score Bands (0.5)"
    )
    results_list.append(r2)
    strategy_names.append("Z-Band 0.5")

    # Variant 3: Holding period filter (20 days)
    r3 = run_improved_backtest(
        start_date='2015-01-01',
        z_threshold=0.0,
        min_holding_days=20,
        rebalance_frequency='monthly',
        transaction_cost=0.001,
        strategy_name="V3: 20-Day Holding Filter"
    )
    results_list.append(r3)
    strategy_names.append("20-Day Hold")

    # Variant 4: Combined (z-band + holding period)
    r4 = run_improved_backtest(
        start_date='2015-01-01',
        z_threshold=0.5,
        min_holding_days=20,
        rebalance_frequency='monthly',
        transaction_cost=0.001,
        strategy_name="V4: Combined (Z-band + Hold)"
    )
    results_list.append(r4)
    strategy_names.append("Combined")

    # Variant 5: Quarterly rebalancing + lower costs
    r5 = run_improved_backtest(
        start_date='2015-01-01',
        z_threshold=0.5,
        min_holding_days=20,
        rebalance_frequency='quarterly',
        transaction_cost=0.0005,
        strategy_name="V5: Quarterly + Low Cost"
    )
    results_list.append(r5)
    strategy_names.append("Quarterly")

    # Compare all strategies
    print("\n\nGenerating comparison analysis...")
    compare_strategies(results_list, strategy_names)

    # Save all results
    for i, (results, name) in enumerate(zip(results_list, strategy_names)):
        filename = f'backtest_variant_{i+1}.csv'
        results.to_csv(filename)
        print(f"[OK] {name} results saved to {filename}")

    print("\n[OK] All backtests complete!")
