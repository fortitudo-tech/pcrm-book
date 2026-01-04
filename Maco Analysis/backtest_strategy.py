"""
Backtest RMP Quadrant Rotation Strategy vs Buy & Hold SPY

This script backtests the macro-valuation quadrant rotation strategy
against a simple buy-and-hold SPY benchmark over the past 10 years.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import yfinance as yf
from rmp_liquidity_tracker import (
    fetch_all_data,
    calculate_quadrant_position,
    calculate_momentum_indicators
)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


# =============================================================================
# Asset Universe & Allocation Rules
# =============================================================================

# Define ETF universe for each quadrant
QUADRANT_ALLOCATIONS = {
    'Dovish/Co-operative': {  # TOP LEFT: Weak USD + Steep Curve
        'EEM': 0.15,   # Emerging Markets
        'GLD': 0.15,   # Gold
        'XLI': 0.15,   # Industrials
        'XLB': 0.10,   # Materials
        'IWM': 0.15,   # Small Caps
        'KRE': 0.10,   # Regional Banks
        'DBC': 0.10,   # Commodities
        'SPY': 0.10,   # S&P 500 (core)
    },
    'Happiness Zone': {  # TOP RIGHT: Strong USD + Steep Curve
        'SPY': 0.30,   # S&P 500
        'QQQ': 0.25,   # Nasdaq
        'XLF': 0.15,   # Financials
        'VNQ': 0.10,   # REITs
        'XLK': 0.10,   # Technology
        'IWM': 0.05,   # Small Caps
        'EEM': 0.05,   # EM (reduced)
    },
    'Hawkish Policy': {  # BOTTOM RIGHT: Strong USD + Flat Curve
        'SHY': 0.25,   # Short-term Treasuries
        'XLP': 0.20,   # Consumer Staples
        'XLU': 0.15,   # Utilities
        'VIG': 0.15,   # Dividend Aristocrats
        'SPY': 0.10,   # S&P 500 (reduced)
        'GLD': 0.10,   # Gold (hedge)
        'CASH': 0.05,  # Cash
    },
    'Crisis Zone': {  # BOTTOM LEFT: Weak USD + Flat Curve
        'TLT': 0.30,   # Long-term Treasuries
        'GLD': 0.25,   # Gold
        'SHY': 0.20,   # Short-term Treasuries
        'XLU': 0.10,   # Utilities
        'XLV': 0.10,   # Healthcare
        'CASH': 0.05,  # Cash
    },
    'Unknown': {  # Default/Transition - Balanced
        'SPY': 0.60,   # S&P 500
        'TLT': 0.20,   # Treasuries
        'GLD': 0.10,   # Gold
        'CASH': 0.10,  # Cash
    }
}


# =============================================================================
# Data Fetching for Backtesting
# =============================================================================

def fetch_etf_prices(start_date, end_date):
    """
    Fetch historical prices for all ETFs used in the strategy.

    Parameters:
        start_date: Start date for backtest
        end_date: End date for backtest

    Returns:
        DataFrame with ETF prices
    """
    # Get unique list of all ETFs
    all_etfs = set()
    for allocations in QUADRANT_ALLOCATIONS.values():
        all_etfs.update([etf for etf in allocations.keys() if etf != 'CASH'])

    etf_list = sorted(list(all_etfs))

    print(f"Fetching prices for {len(etf_list)} ETFs...")

    prices = {}
    for etf in etf_list:
        try:
            print(f"  Downloading {etf}...")
            data = yf.download(etf, start=start_date, end=end_date, progress=False)
            if not data.empty:
                # Handle MultiIndex columns
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
    df = df.ffill()  # Forward fill missing data

    return df


# =============================================================================
# Backtesting Engine
# =============================================================================

def run_backtest(start_date='2015-01-01', end_date=None, initial_capital=100000,
                 rebalance_frequency='monthly', transaction_cost=0.001):
    """
    Run backtest of quadrant rotation strategy vs buy-and-hold SPY.

    Parameters:
        start_date: Start date for backtest
        end_date: End date for backtest (default: today)
        initial_capital: Starting capital in USD
        rebalance_frequency: 'daily', 'weekly', or 'monthly'
        transaction_cost: Transaction cost as fraction (0.001 = 0.1%)

    Returns:
        DataFrame with backtest results
    """
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')

    print("=" * 70)
    print("BACKTESTING QUADRANT ROTATION STRATEGY")
    print("=" * 70)
    print(f"Period: {start_date} to {end_date}")
    print(f"Initial Capital: ${initial_capital:,.0f}")
    print(f"Rebalance Frequency: {rebalance_frequency}")
    print(f"Transaction Cost: {transaction_cost*100:.2f}%\n")

    # Fetch macro data and calculate quadrants
    print("Fetching macro data...")
    macro_data = fetch_all_data(start_date=start_date, end_date=end_date)
    macro_data = calculate_quadrant_position(macro_data)
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
            portfolio_value = strategy_capital  # Start with cash
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
                    continue  # Keep as cash

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

    # Calculate Sharpe ratio (assuming 0% risk-free rate for simplicity)
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

    return df_results


# =============================================================================
# Visualization Functions
# =============================================================================

def plot_backtest_results(results):
    """
    Create comprehensive visualization of backtest results.

    Parameters:
        results: DataFrame from run_backtest()
    """
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(4, 2, hspace=0.3, wspace=0.3)

    # 1. Portfolio Value Comparison
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(results.index, results['Strategy_Value'], label='Quadrant Strategy', linewidth=2, color='#2E86AB')
    ax1.plot(results.index, results['Benchmark_Value'], label='Buy & Hold SPY', linewidth=2, color='#A23B72')
    ax1.fill_between(results.index, results['Strategy_Value'], results['Benchmark_Value'],
                     where=results['Strategy_Value'] >= results['Benchmark_Value'],
                     alpha=0.3, color='green', label='Outperformance')
    ax1.fill_between(results.index, results['Strategy_Value'], results['Benchmark_Value'],
                     where=results['Strategy_Value'] < results['Benchmark_Value'],
                     alpha=0.3, color='red', label='Underperformance')
    ax1.set_title('Portfolio Value Over Time', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Portfolio Value ($)')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

    # 2. Cumulative Returns
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(results.index, results['Strategy_Return'], label='Strategy', linewidth=2, color='#2E86AB')
    ax2.plot(results.index, results['Benchmark_Return'], label='Benchmark', linewidth=2, color='#A23B72')
    ax2.set_title('Cumulative Returns', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Return (%)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. Outperformance
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.plot(results.index, results['Outperformance'], linewidth=2, color='#F18F01')
    ax3.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax3.fill_between(results.index, results['Outperformance'], 0,
                     where=results['Outperformance'] >= 0, alpha=0.3, color='green')
    ax3.fill_between(results.index, results['Outperformance'], 0,
                     where=results['Outperformance'] < 0, alpha=0.3, color='red')
    ax3.set_title('Strategy vs Benchmark (Outperformance %)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Outperformance (%)')
    ax3.grid(True, alpha=0.3)

    # 4. Quadrant History
    ax4 = fig.add_subplot(gs[2, :])
    quadrant_map = {
        'Happiness Zone': 3,
        'Hawkish Policy': 2,
        'Crisis Zone': 1,
        'Dovish/Co-operative': 4,
        'Unknown': 0
    }
    colors = {3: 'green', 2: 'orange', 1: 'red', 4: 'blue', 0: 'gray'}
    results['Quadrant_Numeric'] = results['Quadrant'].map(quadrant_map)

    for quadrant, color in colors.items():
        mask = results['Quadrant_Numeric'] == quadrant
        if mask.any():
            ax4.fill_between(results.index, 0, 1, where=mask, alpha=0.5,
                           color=color, transform=ax4.get_xaxis_transform())

    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', alpha=0.5, label='Happiness Zone'),
        Patch(facecolor='orange', alpha=0.5, label='Hawkish Policy'),
        Patch(facecolor='red', alpha=0.5, label='Crisis Zone'),
        Patch(facecolor='blue', alpha=0.5, label='Dovish/Co-operative')
    ]
    ax4.legend(handles=legend_elements, loc='upper left', ncol=4)
    ax4.set_title('Market Quadrant Over Time', fontsize=12, fontweight='bold')
    ax4.set_yticks([])
    ax4.grid(True, axis='x', alpha=0.3)

    # 5. Rolling Returns (1-year)
    ax5 = fig.add_subplot(gs[3, 0])
    strategy_rolling = results['Strategy_Value'].pct_change(252) * 100
    benchmark_rolling = results['Benchmark_Value'].pct_change(252) * 100
    ax5.plot(results.index, strategy_rolling, label='Strategy', linewidth=2, color='#2E86AB')
    ax5.plot(results.index, benchmark_rolling, label='Benchmark', linewidth=2, color='#A23B72')
    ax5.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax5.set_title('Rolling 1-Year Returns', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Return (%)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. Drawdown
    ax6 = fig.add_subplot(gs[3, 1])
    strategy_cummax = results['Strategy_Value'].cummax()
    strategy_dd = (results['Strategy_Value'] - strategy_cummax) / strategy_cummax * 100
    benchmark_cummax = results['Benchmark_Value'].cummax()
    benchmark_dd = (results['Benchmark_Value'] - benchmark_cummax) / benchmark_cummax * 100

    ax6.fill_between(results.index, strategy_dd, 0, alpha=0.5, color='#2E86AB', label='Strategy')
    ax6.fill_between(results.index, benchmark_dd, 0, alpha=0.5, color='#A23B72', label='Benchmark')
    ax6.set_title('Drawdown Over Time', fontsize=12, fontweight='bold')
    ax6.set_ylabel('Drawdown (%)')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.suptitle('Quadrant Rotation Strategy Backtest Analysis',
                 fontsize=16, fontweight='bold', y=0.995)

    plt.tight_layout()
    plt.show()


def plot_quadrant_performance(results):
    """
    Analyze performance by quadrant.

    Parameters:
        results: DataFrame from run_backtest()
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    quadrants = ['Dovish/Co-operative', 'Happiness Zone', 'Hawkish Policy', 'Crisis Zone']
    colors = ['blue', 'green', 'orange', 'red']

    for idx, (quadrant, color) in enumerate(zip(quadrants, colors)):
        ax = axes[idx // 2, idx % 2]

        # Filter data for this quadrant
        mask = results['Quadrant'] == quadrant
        quad_data = results[mask]

        if len(quad_data) > 0:
            # Calculate returns in this quadrant
            quad_returns = quad_data['Strategy_Value'].pct_change() * 100
            bench_returns = quad_data['Benchmark_Value'].pct_change() * 100

            # Plot histogram
            ax.hist(quad_returns.dropna(), bins=50, alpha=0.6, color=color, label='Strategy', density=True)
            ax.hist(bench_returns.dropna(), bins=50, alpha=0.6, color='gray', label='Benchmark', density=True)

            # Stats
            days_in_quad = len(quad_data)
            pct_time = days_in_quad / len(results) * 100

            ax.set_title(f'{quadrant}\n({days_in_quad} days, {pct_time:.1f}% of time)',
                        fontsize=11, fontweight='bold')
            ax.set_xlabel('Daily Return (%)')
            ax.set_ylabel('Density')
            ax.legend()
            ax.grid(True, alpha=0.3)

    plt.suptitle('Return Distribution by Quadrant', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


# =============================================================================
# Main Execution
# =============================================================================

if __name__ == "__main__":
    # Run 10-year backtest
    results = run_backtest(
        start_date='2015-01-01',
        end_date=None,  # Today
        initial_capital=100000,
        rebalance_frequency='monthly',
        transaction_cost=0.001
    )

    # Visualize results
    print("\nGenerating performance charts...")
    plot_backtest_results(results)
    plot_quadrant_performance(results)

    # Save results to CSV
    output_file = 'backtest_results.csv'
    results.to_csv(output_file)
    print(f"\n[OK] Results saved to {output_file}")
