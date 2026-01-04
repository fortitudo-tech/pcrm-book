"""
RMP Liquidity Program & Macro-Valuation Tracking

This module implements a framework to track where markets are and where they're going
based on the macro-valuation shifts framework. The framework uses two key dimensions:

1. **Yield Curve** (Vertical axis): Steepening vs Flattening
2. **Exchange Rate** (Horizontal axis): Falling vs Rising US Dollar

These are driven by:
- **Capital Flows**: Strong inflows (rightward) vs outflows (leftward)
- **Monetary Policy Stance**: Loose (upward) vs Tight (downward)

Four Quadrants:
- **Top Right ("Happiness Zone")**: Rising dollar + Steeper yield curve → Strong capital inflows
- **Bottom Right ("Hawkish Policy")**: Rising dollar + Flatter yield curve → Tight monetary conditions
- **Bottom Left ("Crisis Zone")**: Falling dollar + Flatter yield curve → Capital flight
- **Top Left ("Dovish/Co-operative")**: Falling dollar + Steeper yield curve → Loose monetary policy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import yfinance as yf
from fredapi import Fred
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


# =============================================================================
# Configuration
# =============================================================================

# You'll need a FRED API key (free): https://fred.stlouisfed.org/docs/api/api_key.html
FRED_API_KEY = '4532dbd3e3fb05a0ab2587a8e0ea25ec'  # Replace with your key

# Default date range
DEFAULT_START_DATE = '2020-01-01'
DEFAULT_END_DATE = datetime.today().strftime('%Y-%m-%d')


# =============================================================================
# Data Fetching Functions
# =============================================================================

def fetch_market_data(start_date=None, end_date=None):
    """
    Fetch key market indicators for macro-valuation tracking.

    Parameters:
        start_date: Start date for data (default: 2020-01-01)
        end_date: End date for data (default: today)

    Returns:
        DataFrame with all key indicators
    """
    if start_date is None:
        start_date = DEFAULT_START_DATE
    if end_date is None:
        end_date = DEFAULT_END_DATE

    # Helper function to extract Close price from yfinance download
    def extract_close(df):
        if df.empty:
            return pd.Series(dtype=float)
        # Handle MultiIndex columns (newer yfinance versions)
        if isinstance(df.columns, pd.MultiIndex):
            close_cols = [col for col in df.columns if col[0] == 'Close']
            if close_cols:
                series = df[close_cols[0]]
                series.name = None  # Remove the name to avoid conflicts
                return series
        # Handle simple columns
        elif 'Close' in df.columns:
            return df['Close']
        return pd.Series(dtype=float)

    # 1. US Dollar Index (DXY)
    print("Fetching DXY...")
    try:
        dxy_df = yf.download('DX-Y.NYB', start=start_date, end=end_date, progress=False)
        dxy = extract_close(dxy_df)
        if dxy.empty:
            print("Warning: Could not fetch DXY data")
    except Exception as e:
        print(f"Error fetching DXY: {e}")
        dxy = pd.Series(dtype=float)

    # 2. Treasury Yields (for yield curve)
    print("Fetching Treasury yields...")
    try:
        # 10-year yield
        tnx_df = yf.download('^TNX', start=start_date, end=end_date, progress=False)
        tnx = extract_close(tnx_df)
        if tnx.empty:
            print("Warning: Could not fetch 10Y Treasury data")
    except Exception as e:
        print(f"Error fetching 10Y Treasury: {e}")
        tnx = pd.Series(dtype=float)

    # 3. VIX
    print("Fetching VIX...")
    try:
        vix_df = yf.download('^VIX', start=start_date, end=end_date, progress=False)
        vix = extract_close(vix_df)
        if vix.empty:
            print("Warning: Could not fetch VIX data")
    except Exception as e:
        print(f"Error fetching VIX: {e}")
        vix = pd.Series(dtype=float)

    # 4. Create combined DataFrame
    df = pd.DataFrame({
        'DXY': dxy,
        'UST_10Y': tnx,
        'VIX': vix
    })

    # Drop rows where all values are NaN
    df = df.dropna(how='all')

    return df


def fetch_fred_data(fred_api_key=None, start_date=None, end_date=None):
    """
    Fetch FRED economic data for liquidity and policy tracking.

    Parameters:
        fred_api_key: FRED API key (default: uses global FRED_API_KEY)
        start_date: Start date for data (default: 2020-01-01)
        end_date: End date for data (default: today)

    Returns:
        DataFrame with FRED indicators
    """
    if fred_api_key is None:
        fred_api_key = FRED_API_KEY
    if start_date is None:
        start_date = DEFAULT_START_DATE
    if end_date is None:
        end_date = DEFAULT_END_DATE

    fred = Fred(api_key=fred_api_key)

    indicators = {
        'EXCSRESNW': 'Bank_Excess_Reserves',
        'WALCL': 'Fed_Balance_Sheet',
        'RRPONTSYD': 'Reverse_Repo',
        'FEDFUNDS': 'Fed_Funds_Rate',
        'WTREGEN': 'Treasury_General_Account',
        'DGS10': 'UST_10Y_Yield',
        'DGS2': 'UST_2Y_Yield',
        'BAMLC0A4CBBB': 'IG_Spread',
        'BAMLH0A0HYM2': 'HY_Spread'
    }

    data = {}

    for series_id, label in indicators.items():
        try:
            print(f"Fetching {label}...")
            series = fred.get_series(series_id, start_date, end_date)
            data[label] = series
        except Exception as e:
            print(f"Error fetching {label}: {e}")
            data[label] = pd.Series(dtype=float)

    df = pd.DataFrame(data)

    # Calculate derived metrics
    df['Yield_Curve_10Y2Y'] = df['UST_10Y_Yield'] - df['UST_2Y_Yield']
    df['Net_Liquidity'] = (df['Fed_Balance_Sheet']
                           - df['Reverse_Repo']
                           - df['Treasury_General_Account'])

    return df


def fetch_all_data(fred_api_key=None, start_date=None, end_date=None):
    """
    Fetch and merge all market and FRED data.

    Parameters:
        fred_api_key: FRED API key (default: uses global FRED_API_KEY)
        start_date: Start date for data (default: 2020-01-01)
        end_date: End date for data (default: today)

    Returns:
        DataFrame with all indicators merged
    """
    print("=" * 60)
    print("Fetching Market Data...")
    print("=" * 60)
    market_data = fetch_market_data(start_date, end_date)
    print(f"[OK] Fetched {len(market_data)} days of market data\n")

    print("=" * 60)
    print("Fetching FRED Economic Data...")
    print("=" * 60)
    fred_data = fetch_fred_data(fred_api_key, start_date, end_date)
    print(f"[OK] Fetched {len(fred_data)} days of FRED data\n")

    # Merge datasets
    combined_data = pd.merge(market_data, fred_data,
                             left_index=True, right_index=True, how='outer')
    combined_data = combined_data.sort_index()

    return combined_data


# =============================================================================
# Quadrant Positioning Calculations
# =============================================================================

def calculate_quadrant_position(df, lookback_period=252):
    """
    Calculate position in the macro-valuation quadrant system.

    Parameters:
        df: DataFrame with market indicators
        lookback_period: Period for z-score normalization (default: 252 days)

    Returns:
        DataFrame with quadrant coordinates (x, y)
    """
    result = df.copy()

    # Calculate z-scores using expanding window to handle gaps in data
    # For DXY
    if 'DXY' in result.columns:
        dxy_valid = result['DXY'].dropna()
        if len(dxy_valid) >= lookback_period:
            # Calculate rolling stats on valid data only
            dxy_mean = dxy_valid.rolling(lookback_period, min_periods=lookback_period).mean()
            dxy_std = dxy_valid.rolling(lookback_period, min_periods=lookback_period).std()
            dxy_zscore = (dxy_valid - dxy_mean) / dxy_std
            # Map back to original index
            result['DXY_zscore'] = dxy_zscore.reindex(result.index)
        else:
            result['DXY_zscore'] = np.nan
    else:
        result['DXY_zscore'] = np.nan

    # For Yield Curve
    if 'Yield_Curve_10Y2Y' in result.columns:
        yc_valid = result['Yield_Curve_10Y2Y'].dropna()
        if len(yc_valid) >= lookback_period:
            yc_mean = yc_valid.rolling(lookback_period, min_periods=lookback_period).mean()
            yc_std = yc_valid.rolling(lookback_period, min_periods=lookback_period).std()
            yc_zscore = (yc_valid - yc_mean) / yc_std
            # Map back to original index
            result['YieldCurve_zscore'] = yc_zscore.reindex(result.index)
        else:
            result['YieldCurve_zscore'] = np.nan
    else:
        result['YieldCurve_zscore'] = np.nan

    # Assign quadrants
    def assign_quadrant(row):
        x, y = row.get('DXY_zscore'), row.get('YieldCurve_zscore')

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

    result['Quadrant'] = result.apply(assign_quadrant, axis=1)

    return result


def calculate_momentum_indicators(df, short_window=20, long_window=60):
    """
    Calculate momentum to determine directional movement in quadrant space.

    Parameters:
        df: DataFrame with quadrant positions
        short_window: Short-term moving average window
        long_window: Long-term moving average window

    Returns:
        DataFrame with momentum indicators
    """
    result = df.copy()

    # DXY momentum (x-axis movement)
    result['DXY_momentum'] = (
        result['DXY'].rolling(short_window).mean() -
        result['DXY'].rolling(long_window).mean()
    )

    # Yield curve momentum (y-axis movement)
    result['YieldCurve_momentum'] = (
        result['Yield_Curve_10Y2Y'].rolling(short_window).mean() -
        result['Yield_Curve_10Y2Y'].rolling(long_window).mean()
    )

    # Net liquidity momentum (predictive for future moves)
    if 'Net_Liquidity' in result.columns:
        result['NetLiquidity_momentum'] = result['Net_Liquidity'].pct_change(30)

    return result


# =============================================================================
# Visualization Functions
# =============================================================================

def plot_quadrant_spider(df, recent_months=36, annotation_dates=None, save_path=None):
    """
    Create spider diagram showing path through macro-valuation quadrants.

    Parameters:
        df: DataFrame with quadrant positions
        recent_months: Number of recent months to highlight
        annotation_dates: List of dates to annotate (optional)
        save_path: Path to save the plot (optional)
    """
    # Filter to valid data only
    df_valid = df.dropna(subset=['DXY_zscore', 'YieldCurve_zscore']).copy()

    if df_valid.empty:
        print("Warning: No valid data for quadrant spider plot")
        return

    fig, ax = plt.subplots(figsize=(12, 10))

    # Filter data
    cutoff_date = df_valid.index[-1] - pd.DateOffset(months=recent_months)
    df_recent = df_valid[df_valid.index >= cutoff_date].copy()

    # Plot historical path (faded)
    df_historical = df_valid[df_valid.index < cutoff_date].copy()
    if len(df_historical) > 0:
        ax.plot(df_historical['DXY_zscore'], df_historical['YieldCurve_zscore'],
                'o-', alpha=0.2, color='gray', markersize=2, label='Historical')

    # Plot recent path (colorful gradient)
    if len(df_recent) > 0:
        points = ax.scatter(df_recent['DXY_zscore'], df_recent['YieldCurve_zscore'],
                           c=range(len(df_recent)), cmap='plasma', s=50,
                           alpha=0.7, edgecolors='black', linewidth=0.5)

        # Connect recent points
        ax.plot(df_recent['DXY_zscore'], df_recent['YieldCurve_zscore'],
                '-', alpha=0.4, color='blue', linewidth=1.5)

        # Mark current position
        current = df_valid.iloc[-1]
        ax.scatter(current['DXY_zscore'], current['YieldCurve_zscore'],
                  s=300, marker='*', color='red', edgecolors='black',
                  linewidth=2, zorder=5, label='Current')

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

    # Add axis lines
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.3)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1, alpha=0.3)

    # Labels
    ax.set_xlabel('Exchange Rate (DXY) →\nFalling ← | → Rising', fontsize=12, fontweight='bold')
    ax.set_ylabel('Yield Curve (10Y-2Y) →\nFlattening ← | → Steepening', fontsize=12, fontweight='bold')
    ax.set_title('Macro-Valuation Quadrant Spider Diagram\nCapital Flows & Monetary Policy Positioning',
                fontsize=14, fontweight='bold', pad=20)

    # Add colorbar for time
    cbar = plt.colorbar(points, ax=ax)
    cbar.set_label('Time (Recent to Latest)', rotation=270, labelpad=20)

    # Grid
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left')

    # Set reasonable axis limits
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Saved plot to {save_path}")

    plt.show()


def plot_liquidity_dashboard(df, save_path=None):
    """
    Create comprehensive liquidity dashboard for RMP program context.

    Parameters:
        df: DataFrame with all indicators
        save_path: Path to save the plot (optional)
    """
    fig, axes = plt.subplots(3, 2, figsize=(16, 12))

    # 1. Bank Excess Reserves
    ax = axes[0, 0]
    if 'Bank_Excess_Reserves' in df.columns:
        ax.plot(df.index, df['Bank_Excess_Reserves'], linewidth=2, color='blue')
        ax.fill_between(df.index, df['Bank_Excess_Reserves'], alpha=0.3, color='blue')
    ax.set_title('Bank Excess Reserves (Critical Liquidity Measure)', fontweight='bold')
    ax.set_ylabel('Billions USD')
    ax.grid(True, alpha=0.3)

    # 2. Fed Balance Sheet vs RRP
    ax = axes[0, 1]
    if 'Fed_Balance_Sheet' in df.columns:
        ax.plot(df.index, df['Fed_Balance_Sheet']/1000, label='Fed Balance Sheet', linewidth=2)
    if 'Reverse_Repo' in df.columns:
        ax.plot(df.index, df['Reverse_Repo']/1000, label='Reverse Repo', linewidth=2)
    ax.set_title('Fed Balance Sheet vs Reverse Repo', fontweight='bold')
    ax.set_ylabel('Trillions USD')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 3. Net Liquidity (Fed BS - RRP - TGA)
    ax = axes[1, 0]
    if 'Net_Liquidity' in df.columns:
        ax.plot(df.index, df['Net_Liquidity']/1000, linewidth=2, color='green')
        ax.fill_between(df.index, df['Net_Liquidity']/1000, alpha=0.3, color='green')
    ax.set_title('Net Liquidity (Fed BS - RRP - TGA)', fontweight='bold')
    ax.set_ylabel('Trillions USD')
    ax.grid(True, alpha=0.3)

    # 4. Yield Curve
    ax = axes[1, 1]
    if 'Yield_Curve_10Y2Y' in df.columns:
        ax.plot(df.index, df['Yield_Curve_10Y2Y'], linewidth=2, color='purple')
        ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Inversion')
        ax.fill_between(df.index, df['Yield_Curve_10Y2Y'], 0,
                         where=df['Yield_Curve_10Y2Y']>0, alpha=0.3, color='green', label='Steep')
        ax.fill_between(df.index, df['Yield_Curve_10Y2Y'], 0,
                         where=df['Yield_Curve_10Y2Y']<=0, alpha=0.3, color='red', label='Inverted')
    ax.set_title('Yield Curve (10Y-2Y Spread)', fontweight='bold')
    ax.set_ylabel('Basis Points')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 5. Credit Spreads
    ax = axes[2, 0]
    if 'IG_Spread' in df.columns:
        ax.plot(df.index, df['IG_Spread'], label='IG Spread', linewidth=2)
    if 'HY_Spread' in df.columns:
        ax.plot(df.index, df['HY_Spread'], label='HY Spread', linewidth=2)
    ax.set_title('Credit Spreads (Stress Indicators)', fontweight='bold')
    ax.set_ylabel('Basis Points')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 6. DXY
    ax = axes[2, 1]
    if 'DXY' in df.columns:
        ax.plot(df.index, df['DXY'], linewidth=2, color='darkgreen')
        ax.fill_between(df.index, df['DXY'], alpha=0.3, color='darkgreen')
    ax.set_title('US Dollar Index (DXY)', fontweight='bold')
    ax.set_ylabel('Index Level')
    ax.grid(True, alpha=0.3)

    plt.suptitle('Liquidity & Macro Dashboard (RMP Context)',
                fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Saved plot to {save_path}")

    plt.show()


def plot_quadrant_history(df, save_path=None):
    """
    Plot time series showing which quadrant the market has been in.

    Parameters:
        df: DataFrame with quadrant positions
        save_path: Path to save the plot (optional)
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    # Map quadrants to numeric values for plotting
    quadrant_map = {
        'Happiness Zone': 3,
        'Hawkish Policy': 2,
        'Crisis Zone': 1,
        'Dovish/Co-operative': 4,
        'Unknown': 0
    }

    colors = {
        3: 'green',
        2: 'orange',
        1: 'red',
        4: 'blue',
        0: 'gray'
    }

    df['Quadrant_Numeric'] = df['Quadrant'].map(quadrant_map)

    # Plot as colored areas
    for quadrant, color in colors.items():
        mask = df['Quadrant_Numeric'] == quadrant
        if mask.any():
            ax.fill_between(df.index, 0, 1, where=mask, alpha=0.5,
                           color=color, transform=ax.get_xaxis_transform())

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', alpha=0.5, label='Happiness Zone'),
        Patch(facecolor='orange', alpha=0.5, label='Hawkish Policy'),
        Patch(facecolor='red', alpha=0.5, label='Crisis Zone'),
        Patch(facecolor='blue', alpha=0.5, label='Dovish/Co-operative')
    ]

    ax.legend(handles=legend_elements, loc='upper left', ncol=4)
    ax.set_title('Macro-Valuation Quadrant History', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date')
    ax.set_yticks([])
    ax.grid(True, axis='x', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Saved plot to {save_path}")

    plt.show()


# =============================================================================
# Scenario Projection
# =============================================================================

def project_dxy_scenario(current_dxy, expected_change_pct, horizon_days=365):
    """
    Project DXY path based on expected % change.

    Per article: DXY expected to firm by ~5% in 2026

    Parameters:
        current_dxy: Current DXY level
        expected_change_pct: Expected percentage change
        horizon_days: Number of days to project

    Returns:
        Series with projected DXY values
    """
    target_dxy = current_dxy * (1 + expected_change_pct/100)

    # Create projection path with some volatility
    dates = pd.date_range(start=datetime.today(), periods=horizon_days, freq='D')

    # Linear path with random walk
    trend = np.linspace(current_dxy, target_dxy, horizon_days)
    noise = np.random.normal(0, current_dxy * 0.003, horizon_days).cumsum()
    projection = trend + noise

    return pd.Series(projection, index=dates)


# =============================================================================
# Analysis & Reporting
# =============================================================================

def print_current_position(df):
    """
    Print current market position summary.

    Parameters:
        df: DataFrame with quadrant positions
    """
    # Find the last row with valid DXY and Quadrant data
    valid_rows = df.dropna(subset=['DXY', 'Quadrant'])
    if valid_rows.empty:
        print("\n" + "=" * 60)
        print("CURRENT MARKET POSITION")
        print("=" * 60)
        print("No valid data available")
        print("=" * 60 + "\n")
        return

    current = valid_rows.iloc[-1]
    current_date = valid_rows.index[-1]

    print("\n" + "=" * 60)
    print("CURRENT MARKET POSITION")
    print("=" * 60)
    print(f"Date: {current_date.strftime('%Y-%m-%d')}")
    print(f"\nQuadrant: {current['Quadrant']}")
    print(f"\nPositioning:")

    if not pd.isna(current['DXY']):
        print(f"  DXY Level: {current['DXY']:.2f}")
    if 'DXY_zscore' in current and not pd.isna(current['DXY_zscore']):
        print(f"  DXY Z-Score: {current['DXY_zscore']:.2f}")

    if 'Yield_Curve_10Y2Y' in current and not pd.isna(current['Yield_Curve_10Y2Y']):
        print(f"  10Y-2Y Spread: {current['Yield_Curve_10Y2Y']:.0f} bps")
    if 'YieldCurve_zscore' in current and not pd.isna(current['YieldCurve_zscore']):
        print(f"  Yield Curve Z-Score: {current['YieldCurve_zscore']:.2f}")

    if 'VIX' in current and not pd.isna(current['VIX']):
        print(f"\nStress Indicators:")
        print(f"  VIX: {current['VIX']:.2f}")

    if 'IG_Spread' in current and not pd.isna(current['IG_Spread']):
        print(f"  IG Spread: {current['IG_Spread']:.2f} bps")

    if 'HY_Spread' in current and not pd.isna(current['HY_Spread']):
        print(f"  HY Spread: {current['HY_Spread']:.2f} bps")

    if 'Net_Liquidity' in current and not pd.isna(current['Net_Liquidity']):
        print(f"\nLiquidity:")
        print(f"  Net Liquidity: ${current['Net_Liquidity']/1000:.2f}T")

    print("=" * 60 + "\n")


def generate_report(df, output_dir=None):
    """
    Generate comprehensive analysis report with all visualizations.

    Parameters:
        df: DataFrame with all indicators and quadrant positions
        output_dir: Directory to save plots (optional)
    """
    print("\n" + "=" * 60)
    print("GENERATING COMPREHENSIVE MARKET ANALYSIS REPORT")
    print("=" * 60)

    # Print current position
    print_current_position(df)

    # Generate plots
    print("\nGenerating visualizations...")

    if output_dir:
        import os
        os.makedirs(output_dir, exist_ok=True)

        spider_path = os.path.join(output_dir, 'quadrant_spider.png')
        dashboard_path = os.path.join(output_dir, 'liquidity_dashboard.png')
        history_path = os.path.join(output_dir, 'quadrant_history.png')
    else:
        spider_path = dashboard_path = history_path = None

    # 1. Quadrant Spider Diagram
    print("\n1. Creating quadrant spider diagram...")
    plot_quadrant_spider(df, recent_months=36, save_path=spider_path)

    # 2. Liquidity Dashboard
    print("\n2. Creating liquidity dashboard...")
    plot_liquidity_dashboard(df, save_path=dashboard_path)

    # 3. Quadrant History
    print("\n3. Creating quadrant history...")
    plot_quadrant_history(df, save_path=history_path)

    print("\n" + "=" * 60)
    print("REPORT GENERATION COMPLETE")
    print("=" * 60 + "\n")


# =============================================================================
# Main Execution
# =============================================================================

def main():
    """
    Main function to run complete analysis.
    """
    # Fetch all data
    data = fetch_all_data()

    # Calculate quadrant positions
    print("=" * 60)
    print("Calculating Quadrant Positions...")
    print("=" * 60)
    data = calculate_quadrant_position(data)
    data = calculate_momentum_indicators(data)
    print("[OK] Calculations complete\n")

    # Generate comprehensive report
    generate_report(data)

    return data


if __name__ == "__main__":
    # Run the analysis
    df = main()
