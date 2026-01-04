"""
Simplified Strategy: SPY + Tactical Hedges Only

Instead of complex sector rotations, use quadrants to adjust hedges
around a core SPY position.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf
from backtest_improved import (
    calculate_quadrant_with_bands,
    apply_holding_period_filter,
    run_improved_backtest
)
from rmp_liquidity_tracker import (
    fetch_all_data,
    calculate_momentum_indicators
)

# Simplified allocations - mostly SPY with tactical hedges
SIMPLIFIED_ALLOCATIONS = {
    'Happiness Zone': {  # Full risk-on
        'SPY': 1.00,
    },
    'Dovish/Co-operative': {  # Slight defensive tilt
        'SPY': 0.85,
        'GLD': 0.15,  # Weak dollar = gold hedge
    },
    'Hawkish Policy': {  # Moderate defensive
        'SPY': 0.70,
        'SHY': 0.30,  # Cash buffer for tight policy
    },
    'Crisis Zone': {  # Maximum defensive
        'SPY': 0.50,
        'TLT': 0.30,  # Flight to quality
        'GLD': 0.20,
    },
    'Unknown': {  # Neutral positioning
        'SPY': 0.80,
        'SHY': 0.20,
    }
}


def fetch_simplified_etf_prices(start_date, end_date):
    """Fetch prices for simplified strategy (only 4 ETFs)."""
    etfs = ['SPY', 'GLD', 'SHY', 'TLT']

    print(f"Fetching prices for {len(etfs)} ETFs...")

    prices = {}
    for etf in etfs:
        try:
            print(f"  Downloading {etf}...")
            data = yf.download(etf, start=start_date, end=end_date, progress=False)
            if not data.empty:
                if isinstance(data.columns, pd.MultiIndex):
                    close_cols = [col for col in data.columns if col[0] == 'Adj Close']
                    if close_cols:
                        prices[etf] = data[close_cols[0]]
                    else:
                        close_cols = [col for col in data.columns if col[0] == 'Close']
                        if close_cols:
                            prices[etf] = data[close_cols[0]]
                elif 'Adj Close' in data.columns:
                    prices[etf] = data['Adj Close']
                elif 'Close' in data.columns:
                    prices[etf] = data['Close']
        except Exception as e:
            print(f"  Error fetching {etf}: {e}")

    df = pd.DataFrame(prices)
    df = df.ffill()

    return df


def run_simplified_backtest(start_date='2015-01-01', end_date=None,
                            initial_capital=100000,
                            rebalance_frequency='quarterly',
                            transaction_cost=0.0005,
                            z_threshold=1.0,
                            min_holding_days=30):
    """
    Run backtest with simplified SPY-centric allocations.
    """
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')

    print("=" * 70)
    print("SIMPLIFIED STRATEGY: SPY + TACTICAL HEDGES")
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
    macro_data = calculate_quadrant_with_bands(macro_data, z_threshold=z_threshold)

    if min_holding_days > 0:
        macro_data['Quadrant'] = apply_holding_period_filter(
            macro_data['Quadrant'], min_holding_days)

    macro_data = calculate_momentum_indicators(macro_data)

    # Fetch ETF prices (only 4 ETFs!)
    etf_prices = fetch_simplified_etf_prices(start_date, end_date)

    # Align dates
    common_dates = macro_data.index.intersection(etf_prices.index)
    macro_data = macro_data.loc[common_dates]
    etf_prices = etf_prices.loc[common_dates]

    print(f"\n[OK] Backtest data prepared: {len(common_dates)} trading days\n")

    # Initialize portfolios
    results = []

    strategy_capital = initial_capital
    strategy_holdings = {}
    last_rebalance_date = None

    spy_shares = initial_capital / etf_prices['SPY'].iloc[0]

    trades = 0
    quadrant_changes = 0
    last_quadrant = None

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

        if last_quadrant is not None and current_quadrant != last_quadrant:
            quadrant_changes += 1
        last_quadrant = current_quadrant

        needs_rebalance = should_rebalance(date, last_rebalance_date, rebalance_frequency)

        if needs_rebalance:
            target_allocation = SIMPLIFIED_ALLOCATIONS.get(
                current_quadrant, SIMPLIFIED_ALLOCATIONS['Unknown'])

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
    benchmark_daily_returns = df_results['Benchmark_Value'].pct_change()

    strategy_vol = strategy_daily_returns.std() * np.sqrt(252) * 100
    benchmark_vol = benchmark_daily_returns.std() * np.sqrt(252) * 100

    strategy_sharpe = strategy_cagr / strategy_vol if strategy_vol > 0 else 0
    benchmark_sharpe = benchmark_cagr / benchmark_vol if benchmark_vol > 0 else 0

    def calculate_max_drawdown(values):
        cummax = values.cummax()
        drawdown = (values - cummax) / cummax * 100
        return drawdown.min()

    strategy_max_dd = calculate_max_drawdown(df_results['Strategy_Value'])
    benchmark_max_dd = calculate_max_drawdown(df_results['Benchmark_Value'])

    print("=" * 70)
    print("BACKTEST RESULTS")
    print("=" * 70)
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
    print(f"  Outperformance:    {strategy_return - benchmark_return:.2f}%")
    print(f"  CAGR Difference:   {strategy_cagr - benchmark_cagr:.2f}%")
    print(f"  Alpha:             {strategy_cagr - benchmark_cagr:.2f}%")
    print()
    print("=" * 70)

    df_results.attrs['cagr'] = strategy_cagr
    df_results.attrs['alpha'] = strategy_cagr - benchmark_cagr
    df_results.attrs['sharpe'] = strategy_sharpe
    df_results.attrs['max_dd'] = strategy_max_dd
    df_results.attrs['trades'] = trades

    return df_results


if __name__ == "__main__":
    # Test simplified strategy on 2015-2026
    print("\n" + "="*70)
    print("TEST 1: SIMPLIFIED STRATEGY (2015-2026)")
    print("="*70 + "\n")

    results_2015 = run_simplified_backtest(
        start_date='2015-01-01',
        end_date=None,
        z_threshold=1.0,
        min_holding_days=30,
        rebalance_frequency='quarterly',
        transaction_cost=0.0005
    )

    results_2015.to_csv('simplified_strategy_2015_2026.csv')
    print("\n[OK] Results saved to simplified_strategy_2015_2026.csv")

    # Test on 2000-2014 period
    print("\n\n" + "="*70)
    print("TEST 2: SIMPLIFIED STRATEGY (2000-2014)")
    print("="*70 + "\n")

    results_2000 = run_simplified_backtest(
        start_date='2000-01-01',
        end_date='2014-12-31',
        z_threshold=1.0,
        min_holding_days=30,
        rebalance_frequency='quarterly',
        transaction_cost=0.0005
    )

    results_2000.to_csv('simplified_strategy_2000_2014.csv')
    print("\n[OK] Results saved to simplified_strategy_2000_2014.csv")

    print("\n\n" + "="*70)
    print("COMPARISON ACROSS TIME PERIODS")
    print("="*70)
    print(f"\n2015-2026:")
    print(f"  Alpha: {results_2015.attrs['alpha']:+.2f}%")
    print(f"  Sharpe: {results_2015.attrs['sharpe']:.2f}")
    print(f"  Max DD: {results_2015.attrs['max_dd']:.2f}%")

    print(f"\n2000-2014:")
    print(f"  Alpha: {results_2000.attrs['alpha']:+.2f}%")
    print(f"  Sharpe: {results_2000.attrs['sharpe']:.2f}")
    print(f"  Max DD: {results_2000.attrs['max_dd']:.2f}%")

    print("\n[OK] Simplified strategy tests complete!")
