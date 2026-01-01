#!/usr/bin/env python3
"""
Automated daily market research script.

This script runs automatically via cron to provide daily market insights.
Configure via crontab to run at your desired time.

Example cron entry (runs daily at 6 PM Eastern):
0 18 * * * cd /path/to/pcrm-book && poetry run python scripts/daily_research.py >> logs/daily_research.log 2>&1
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents import (
    DataCollectionAgent,
    StatisticalAnalysisAgent,
    RiskAnalyticsAgent,
    MarketResearchAgent,
    config
)


def daily_research_pipeline(tickers=None, output_dir='output/daily_reports'):
    """
    Run comprehensive daily research pipeline.

    Args:
        tickers: List of tickers to analyze (default: major indices)
        output_dir: Directory to save reports
    """
    if tickers is None:
        tickers = ['SPY', 'QQQ', 'TLT', 'GLD', 'VTI', 'IWM', 'EFA', 'EEM']

    print(f"\n{'='*60}")
    print(f"Daily Market Research - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 1. DATA COLLECTION
    print("1. Collecting market data...")
    data_agent = DataCollectionAgent()

    try:
        prices = data_agent.execute(
            tickers=tickers,
            period='1y',
            interval='1d'
        )

        if 'Adj Close' in prices.columns.levels[0]:
            prices_adj = prices['Adj Close']
        else:
            prices_adj = prices

        returns = data_agent.calculate_returns(prices_adj).dropna()

        print(f"   ✓ Collected {len(prices_adj)} days of data for {len(tickers)} assets")

    except Exception as e:
        print(f"   ✗ Error collecting data: {e}")
        return None

    # 2. MARKET SUMMARY
    print("\n2. Generating market summary...")
    market_agent = MarketResearchAgent()

    try:
        summary = market_agent.market_summary(prices_adj, returns)

        print("\n   LATEST PRICES:")
        for ticker, price in summary['latest_prices'].items():
            change_1d = summary['price_change_1d'].get(ticker, 0) * 100
            symbol = "🟢" if change_1d >= 0 else "🔴"
            print(f"   {symbol} {ticker}: ${price:.2f} ({change_1d:+.2f}%)")

    except Exception as e:
        print(f"   ✗ Error generating summary: {e}")
        summary = None

    # 3. RISK ANALYSIS
    print("\n3. Analyzing risk metrics...")
    risk_agent = RiskAnalyticsAgent()

    try:
        # Calculate VaR for each asset
        var_95 = risk_agent.value_at_risk(
            returns,
            confidence_level=0.95,
            method='historical'
        )

        # Calculate volatility
        volatility = risk_agent.calculate_volatility(returns, annualize=True)

        print("\n   RISK METRICS (95% VaR, Annual Volatility):")
        for ticker in tickers:
            if ticker in var_95.index:
                var_val = var_95[ticker] * 100
                vol_val = volatility[ticker] * 100
                print(f"   {ticker}: VaR={var_val:.2f}%, Vol={vol_val:.1f}%")

    except Exception as e:
        print(f"   ✗ Error analyzing risk: {e}")
        var_95 = None
        volatility = None

    # 4. MOMENTUM INDICATORS
    print("\n4. Checking momentum indicators...")

    try:
        momentum = market_agent.momentum_analysis(prices_adj, period=14)

        print("\n   RSI (14-day):")
        latest_rsi = momentum['RSI'].iloc[-1]
        for ticker in tickers:
            if ticker in latest_rsi.index:
                rsi_val = latest_rsi[ticker]
                if rsi_val > 70:
                    status = "⚠️  OVERBOUGHT"
                elif rsi_val < 30:
                    status = "⚠️  OVERSOLD"
                else:
                    status = "✓ Neutral"
                print(f"   {ticker}: {rsi_val:.1f} - {status}")

    except Exception as e:
        print(f"   ✗ Error analyzing momentum: {e}")
        momentum = None

    # 5. REGIME DETECTION
    print("\n5. Detecting market regime...")

    try:
        regimes = market_agent.regime_detection(
            returns,
            method='volatility',
            window=60
        )

        current_vol = regimes['volatility'].iloc[-1]
        print("\n   CURRENT VOLATILITY (60-day):")
        for ticker in tickers:
            if ticker in current_vol.index:
                vol_val = current_vol[ticker] * 100 * (252**0.5)
                print(f"   {ticker}: {vol_val:.1f}% annualized")

    except Exception as e:
        print(f"   ✗ Error detecting regime: {e}")
        regimes = None

    # 6. CORRELATION ANALYSIS
    print("\n6. Analyzing correlations...")
    stats_agent = StatisticalAnalysisAgent()

    try:
        corr_analysis = stats_agent.correlation_analysis(returns)

        print("\n   CORRELATION MATRIX:")
        print(corr_analysis['correlation'].round(2))

    except Exception as e:
        print(f"   ✗ Error analyzing correlations: {e}")
        corr_analysis = None

    # 7. SAVE REPORT
    print("\n7. Saving report...")

    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = Path(output_dir) / f"daily_report_{timestamp}.txt"

        with open(report_file, 'w') as f:
            f.write(f"DAILY MARKET RESEARCH REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*60}\n\n")

            if summary:
                f.write("MARKET SUMMARY\n")
                f.write(f"Latest Prices: {summary['latest_prices']}\n")
                f.write(f"1-Day Changes: {summary['price_change_1d']}\n\n")

            if var_95 is not None:
                f.write(f"RISK METRICS\n")
                f.write(f"VaR (95%): {var_95.to_dict()}\n")
                f.write(f"Volatility: {volatility.to_dict()}\n\n")

            if momentum:
                f.write(f"MOMENTUM\n")
                f.write(f"RSI: {momentum['RSI'].iloc[-1].to_dict()}\n\n")

            if corr_analysis:
                f.write(f"CORRELATIONS\n")
                f.write(f"{corr_analysis['correlation']}\n\n")

        print(f"   ✓ Report saved to {report_file}")

    except Exception as e:
        print(f"   ✗ Error saving report: {e}")

    # 8. SUMMARY
    print(f"\n{'='*60}")
    print("Research Complete!")
    print(f"{'='*60}\n")

    return {
        'summary': summary,
        'risk': {'var': var_95, 'volatility': volatility},
        'momentum': momentum,
        'regime': regimes,
        'correlation': corr_analysis
    }


if __name__ == "__main__":
    # You can customize the ticker list here
    custom_tickers = os.getenv('RESEARCH_TICKERS', None)
    if custom_tickers:
        tickers = custom_tickers.split(',')
    else:
        tickers = None  # Use defaults

    # Run the pipeline
    results = daily_research_pipeline(tickers=tickers)

    # Exit code based on success
    sys.exit(0 if results else 1)
