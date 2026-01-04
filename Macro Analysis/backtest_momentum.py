"""
Momentum-Enhanced Strategy

Add momentum filter to prevent rotations during strong trends.
Only rotate when:
1. Quadrant changes AND
2. Momentum confirms the direction
"""

import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
from backtest_improved import (
    calculate_quadrant_with_bands,
    apply_holding_period_filter
)
from rmp_liquidity_tracker import (
    fetch_all_data,
    calculate_momentum_indicators
)
from backtest_strategy import QUADRANT_ALLOCATIONS, fetch_etf_prices


def add_momentum_indicators(df, spy_prices):
    """Add momentum indicators to macro data."""
    result = df.copy()

    # Align SPY prices with macro data
    spy_aligned = spy_prices.reindex(df.index, method='ffill')

    # 200-day moving average
    result['SPY_Price'] = spy_aligned
    result['SPY_MA200'] = spy_aligned.rolling(200, min_periods=200).mean()
    result['SPY_Uptrend'] = spy_aligned > result['SPY_MA200']

    # 50-day vs 200-day crossover
    result['SPY_MA50'] = spy_aligned.rolling(50, min_periods=50).mean()
    result['SPY_Golden_Cross'] = result['SPY_MA50'] > result['SPY_MA200']

    # Rate of change (3-month momentum)
    result['SPY_ROC_3M'] = spy_aligned.pct_change(63) * 100

    return result


def quadrant_risk_score(quadrant):
    """Assign risk score to each quadrant (higher = more bullish)."""
    scores = {
        'Happiness Zone': 4,        # Most bullish
        'Dovish/Co-operative': 3,   # Moderately bullish
        'Hawkish Policy': 2,        # Neutral/defensive
        'Crisis Zone': 1,           # Most defensive
        'Unknown': 2.5
    }
    return scores.get(quadrant, 2.5)


def should_rotate_with_momentum(current_quad, new_quad, spy_uptrend, spy_roc):
    """
    Decide whether to rotate based on momentum confirmation.

    Rules:
    1. If in uptrend and moving to MORE bullish quadrant -> Rotate
    2. If in downtrend and moving to MORE defensive quadrant -> Rotate
    3. If fighting the trend -> Don't rotate (stay in current)
    4. If momentum is very strong (>20% 3M return) -> Stay aggressive regardless
    """
    if current_quad == new_quad:
        return False

    current_risk = quadrant_risk_score(current_quad)
    new_risk = quadrant_risk_score(new_quad)

    # Very strong momentum -> stay aggressive
    if spy_roc > 20 and new_risk < current_risk:
        return False  # Don't get defensive during melt-ups

    # Very weak momentum -> get defensive
    if spy_roc < -15 and new_risk > current_risk:
        return False  # Don't get aggressive during crashes

    # Normal case: align with trend
    if spy_uptrend:
        # In uptrend: allow rotations to more bullish quadrants
        return new_risk >= current_risk
    else:
        # In downtrend: allow rotations to more defensive quadrants
        return new_risk <= current_risk


def run_momentum_backtest(start_date='2015-01-01', end_date=None,
                          initial_capital=100000,
                          rebalance_frequency='quarterly',
                          transaction_cost=0.0005,
                          z_threshold=1.0,
                          min_holding_days=30):
    """Run backtest with momentum filter."""
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')

    print("=" * 70)
    print("MOMENTUM-ENHANCED QUADRANT STRATEGY")
    print("=" * 70)
    print(f"Period: {start_date} to {end_date}")
    print(f"Initial Capital: ${initial_capital:,.0f}")
    print(f"Rebalance Frequency: {rebalance_frequency}")
    print(f"Transaction Cost: {transaction_cost*100:.2f}%")
    print(f"Z-score Threshold: {z_threshold}")
    print(f"Min Holding Days: {min_holding_days}")
    print(f"Momentum Filter: SPY 200-day MA + 3M ROC\n")

    # Fetch macro data
    print("Fetching macro data...")
    macro_data = fetch_all_data(start_date=start_date, end_date=end_date)
    macro_data = calculate_quadrant_with_bands(macro_data, z_threshold=z_threshold)

    if min_holding_days > 0:
        macro_data['Quadrant_Raw'] = macro_data['Quadrant'].copy()
        macro_data['Quadrant'] = apply_holding_period_filter(
            macro_data['Quadrant'], min_holding_days)

    macro_data = calculate_momentum_indicators(macro_data)

    # Fetch ETF prices
    etf_prices = fetch_etf_prices(start_date, end_date)

    # Add momentum indicators
    macro_data = add_momentum_indicators(macro_data, etf_prices['SPY'])

    # Align dates
    common_dates = macro_data.index.intersection(etf_prices.index)
    macro_data = macro_data.loc[common_dates]
    etf_prices = etf_prices.loc[common_dates]

    print(f"\n[OK] Backtest data prepared: {len(common_dates)} trading days\n")

    # Initialize
    results = []
    strategy_capital = initial_capital
    strategy_holdings = {}
    last_rebalance_date = None

    spy_shares = initial_capital / etf_prices['SPY'].iloc[0]

    trades = 0
    quadrant_changes = 0
    momentum_blocks = 0
    last_quadrant = None
    active_quadrant = macro_data['Quadrant'].iloc[0]  # Track what we're actually using

    def should_rebalance(current_date, last_date, frequency):
        if last_date is None:
            return True
        if frequency == 'quarterly':
            return (current_date.month - 1) // 3 != (last_date.month - 1) // 3
        elif frequency == 'monthly':
            return current_date.month != last_date.month
        return False

    # Main loop
    for date in common_dates:
        current_quadrant = macro_data.loc[date, 'Quadrant']
        spy_uptrend = macro_data.loc[date, 'SPY_Uptrend']
        spy_roc = macro_data.loc[date, 'SPY_ROC_3M']

        # Check if momentum allows rotation
        if current_quadrant != active_quadrant:
            if not pd.isna(spy_uptrend) and not pd.isna(spy_roc):
                if should_rotate_with_momentum(active_quadrant, current_quadrant,
                                               spy_uptrend, spy_roc):
                    # Momentum confirms -> rotate
                    active_quadrant = current_quadrant
                    if last_quadrant is not None:
                        quadrant_changes += 1
                else:
                    # Momentum blocks rotation
                    momentum_blocks += 1
            else:
                # No momentum data yet, allow rotation
                active_quadrant = current_quadrant

        last_quadrant = current_quadrant

        needs_rebalance = should_rebalance(date, last_rebalance_date, rebalance_frequency)

        if needs_rebalance:
            target_allocation = QUADRANT_ALLOCATIONS.get(
                active_quadrant, QUADRANT_ALLOCATIONS['Unknown'])

            portfolio_value = strategy_capital
            for etf, shares in strategy_holdings.items():
                if etf in etf_prices.columns and not pd.isna(etf_prices.loc[date, etf]):
                    portfolio_value += shares * etf_prices.loc[date, etf]

            # Sell all
            for etf, shares in strategy_holdings.items():
                if etf in etf_prices.columns and not pd.isna(etf_prices.loc[date, etf]):
                    proceeds = shares * etf_prices.loc[date, etf]
                    strategy_capital += proceeds * (1 - transaction_cost)
                    trades += 1

            strategy_holdings = {}

            # Buy new
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

        # Calculate values
        strategy_value = strategy_capital
        for etf, shares in strategy_holdings.items():
            if etf in etf_prices.columns and not pd.isna(etf_prices.loc[date, etf]):
                strategy_value += shares * etf_prices.loc[date, etf]

        benchmark_value = spy_shares * etf_prices.loc[date, 'SPY']

        results.append({
            'Date': date,
            'Quadrant': current_quadrant,
            'Active_Quadrant': active_quadrant,
            'Strategy_Value': strategy_value,
            'Benchmark_Value': benchmark_value,
            'Strategy_Return': (strategy_value / initial_capital - 1) * 100,
            'Benchmark_Return': (benchmark_value / initial_capital - 1) * 100,
            'Outperformance': (strategy_value / benchmark_value - 1) * 100,
        })

    df_results = pd.DataFrame(results)
    df_results.set_index('Date', inplace=True)

    # Calculate metrics
    final_strategy = df_results['Strategy_Value'].iloc[-1]
    final_benchmark = df_results['Benchmark_Value'].iloc[-1]

    strategy_return = (final_strategy / initial_capital - 1) * 100
    benchmark_return = (final_benchmark / initial_capital - 1) * 100

    years = (df_results.index[-1] - df_results.index[0]).days / 365.25
    strategy_cagr = ((final_strategy / initial_capital) ** (1/years) - 1) * 100
    benchmark_cagr = ((final_benchmark / initial_capital) ** (1/years) - 1) * 100

    strategy_daily_returns = df_results['Strategy_Value'].pct_change()
    strategy_vol = strategy_daily_returns.std() * np.sqrt(252) * 100
    strategy_sharpe = strategy_cagr / strategy_vol if strategy_vol > 0 else 0

    def calculate_max_drawdown(values):
        cummax = values.cummax()
        drawdown = (values - cummax) / cummax * 100
        return drawdown.min()

    strategy_max_dd = calculate_max_drawdown(df_results['Strategy_Value'])

    print("=" * 70)
    print("BACKTEST RESULTS")
    print("=" * 70)
    print(f"\nPeriod: {years:.2f} years")
    print(f"Number of rebalances: {trades // 2}")
    print(f"Quadrant changes (raw): {(df_results['Quadrant'] != df_results['Quadrant'].shift()).sum()}")
    print(f"Actual rotations (after momentum filter): {quadrant_changes}")
    print(f"Rotations blocked by momentum: {momentum_blocks}")
    print()

    print("STRATEGY PERFORMANCE:")
    print(f"  Final Value:        ${final_strategy:,.2f}")
    print(f"  Total Return:       {strategy_return:.2f}%")
    print(f"  CAGR:              {strategy_cagr:.2f}%")
    print(f"  Volatility:        {strategy_vol:.2f}%")
    print(f"  Sharpe Ratio:      {strategy_sharpe:.2f}")
    print(f"  Max Drawdown:      {strategy_max_dd:.2f}%")
    print()

    print("BENCHMARK (SPY):")
    print(f"  Final Value:        ${final_benchmark:,.2f}")
    print(f"  CAGR:              {benchmark_cagr:.2f}%")
    print()

    print("RELATIVE PERFORMANCE:")
    print(f"  Alpha:             {strategy_cagr - benchmark_cagr:+.2f}%")
    print()
    print("=" * 70)

    df_results.attrs['cagr'] = strategy_cagr
    df_results.attrs['alpha'] = strategy_cagr - benchmark_cagr
    df_results.attrs['sharpe'] = strategy_sharpe
    df_results.attrs['max_dd'] = strategy_max_dd

    return df_results


if __name__ == "__main__":
    # Test 2015-2026
    print("\n" + "="*70)
    print("TEST 1: MOMENTUM FILTER (2015-2026)")
    print("="*70 + "\n")

    results_2015 = run_momentum_backtest(
        start_date='2015-01-01',
        end_date=None,
        z_threshold=1.0,
        min_holding_days=30,
        rebalance_frequency='quarterly',
        transaction_cost=0.0005
    )

    results_2015.to_csv('momentum_strategy_2015_2026.csv')
    print("\n[OK] Results saved to momentum_strategy_2015_2026.csv")

    # Test 2000-2014
    print("\n\n" + "="*70)
    print("TEST 2: MOMENTUM FILTER (2000-2014)")
    print("="*70 + "\n")

    results_2000 = run_momentum_backtest(
        start_date='2000-01-01',
        end_date='2014-12-31',
        z_threshold=1.0,
        min_holding_days=30,
        rebalance_frequency='quarterly',
        transaction_cost=0.0005
    )

    results_2000.to_csv('momentum_strategy_2000_2014.csv')
    print("\n[OK] Results saved to momentum_strategy_2000_2014.csv")

    print("\n\n" + "="*70)
    print("MOMENTUM FILTER COMPARISON")
    print("="*70)
    print(f"\n2015-2026:")
    print(f"  Alpha: {results_2015.attrs['alpha']:+.2f}%")
    print(f"  Sharpe: {results_2015.attrs['sharpe']:.2f}")

    print(f"\n2000-2014:")
    print(f"  Alpha: {results_2000.attrs['alpha']:+.2f}%")
    print(f"  Sharpe: {results_2000.attrs['sharpe']:.2f}")

    print("\n[OK] Momentum strategy tests complete!")
