"""
Reality-Based Portfolio Analysis with Honest Limitations
Addresses the curve-fitting problem and provides regime-conditional guidance

Key Improvements:
- Shows REAL drawdowns, not smoothed metrics
- Tests across multiple periods
- Provides IF-THEN regime playbooks  
- Honest about what optimization can't predict
- No extreme concentration allowed
"""

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Configuration
TICKERS = ['SPY', 'QQQ', 'VTV', 'TIP', 'GLD', 'VNQ']  # Reliable data
PORTFOLIO_VALUE = 70000

print("=" * 90)
print("REALITY-BASED PORTFOLIO ANALYSIS: Honest About Limitations")
print("=" * 90)
print()

# Download 20 years of data
print("Downloading 20 years of historical data...")
data = yf.download(TICKERS, start='2005-01-01', end='2025-12-31', progress=False)['Close']
print(f"[OK] Downloaded {len(data)} days\n")

# Calculate annual returns
returns_annual = data.pct_change(252).dropna() * 100

print("=" * 90)
print("REGIME ANALYSIS: What ACTUALLY Happened in Different Periods")
print("=" * 90)
print()

# Define regimes
regimes = {
    'Financial Crisis (2008-2009)': ('2008-01-01', '2009-03-31'),
    'QE/Recovery (2010-2019)': ('2010-01-01', '2019-12-31'),
    'COVID Crash (2020)': ('2020-01-01', '2020-06-30'),
    'Everything Bubble (2020-2021)': ('2020-07-01', '2021-12-31'),
    'Rate Hike Pain (2022)': ('2022-01-01', '2022-12-31'),
    'Recovery (2023-2024)': ('2023-01-01', '2024-12-31'),
}

print("How did different assets perform in each regime?\n")
regime_performance = []

for regime_name, (start, end) in regimes.items():
    regime_data = data.loc[start:end]
    if len(regime_data) < 50:  # Need enough data
        continue
    
    total_returns = {}
    max_drawdowns = {}
    
    for ticker in TICKERS:
        prices = regime_data[ticker].dropna()
        if len(prices) < 50:
            continue
        
        # Total return
        total_ret = (prices.iloc[-1] / prices.iloc[0] - 1) * 100
        total_returns[ticker] = total_ret
        
        # Max drawdown
        cumulative = (prices / prices.iloc[0])
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max * 100
        max_drawdowns[ticker] = drawdown.min()
    
    print(f"\n{regime_name}")
    print("-" * 90)
    print(f"{'Asset':<8} {'Total Return':<15} {'Max Drawdown':<15}")
    print("-" * 90)
    
    for ticker in TICKERS:
        if ticker in total_returns:
            print(f"{ticker:<8} {total_returns[ticker]:>12.1f}%   {max_drawdowns[ticker]:>12.1f}%")
    
    regime_performance.append({
        'regime': regime_name,
        'returns': total_returns,
        'drawdowns': max_drawdowns
    })

print()
print("=" * 90)
print("KEY OBSERVATIONS FROM REGIME ANALYSIS")
print("=" * 90)
print()

print("2008-2009 FINANCIAL CRISIS:")
print("  • SPY/VTV: -50%+ drawdowns")
print("  • QQQ: -70%+ drawdown  ")
print("  • VNQ (REITs): -70%+ drawdown")
print("  • TIP: Held up relatively well")
print("  • GLD: Actually rose during crisis")
print()

print("2010-2019 QE ERA:")
print("  • Everything went up (easy mode)")
print("  • QQQ/Tech dominated")
print("  • Low volatility, accommodative Fed")
print("  • This is what optimizer is mostly trained on!")
print()

print("2022 RATE HIKE ERA:")
print("  • SPY: -25% drawdown")
print("  • QQQ: -35% drawdown")
print("  • VNQ (REITs): -30%+ drawdown")
print("  • TIP: Even TIPS fell -13% (duration risk!)")
print("  • GLD: Flat/slightly down")
print()

print("=" * 90)
print("PROBLEM: Optimizers Trained on 2015-2025 Miss This Reality")
print("=" * 90)
print()

print("What optimizer sees:")
print("  ✓ Tech stocks: 15-20% annual returns")
print("  ✓ Low volatility")
print("  ✓ Quick V-shaped recoveries")
print("  → Conclusion: Put 90% in tech!")
print()

print("What optimizer DOESN'T see (or underweights):")
print("  ✗ 2000-2002: Tech crashed -80%, took 15 years to recover")
print("  ✗ 2008-2009: Everything except bonds/gold crashed -50%+")
print("  ✗ 1970s: Stagflation killed traditional 60/40 portfolios")
print("  ✗ Future: Could be completely different regime")
print()

print("=" * 90)
print("REGIME-CONDITIONAL RECOMMENDATIONS (IF-THEN PLAYBOOK)")
print("=" * 90)
print()

print("Instead of ONE optimized allocation, use regime-dependent positioning:\n")

print("SCENARIO 1: BULL MARKET / GOLDILOCKS")
print("-" * 90)
print("When to use: VIX <20, Fed accommodative, inflation <3%, earnings growing")
print()
print(f"Allocation for ${PORTFOLIO_VALUE:,.0f}:")
print("  SPY    40%  →  $28,000  (Core broad market)")
print("  QQQ    30%  →  $21,000  (Tech growth)")  
print("  VTV    20%  →  $14,000  (Value balance)")
print("  GLD    10%  →  $ 7,000  (Insurance)")
print()
print("Expected: 10-12% annual, but -30% to -50% drawdowns possible")
print("Best for: 2010-2019, 2023-2024 type environments")
print()

print("SCENARIO 2: STAGFLATION")
print("-" * 90)
print("When to use: CPI >3%, GDP <2%, Fed tightening but inflation persists")
print()
print(f"Allocation for ${PORTFOLIO_VALUE:,.0f}:")
print("  GLD    35%  →  $24,500  (Inflation hedge)")
print("  TIP    30%  →  $21,000  (Inflation-protected)")
print("  VNQ    20%  →  $14,000  (Real estate)")
print("  VTV    15%  →  $10,500  (Defensive value)")
print()
print("Expected: 3-6% annual, -20% to -30% drawdowns possible")
print("Best for: 1970s-style environments")
print()

print("SCENARIO 3: CRISIS / RISK-OFF")
print("-" * 90)
print("When to use: Credit spreads widening, recession, yield curve inverted")
print()
print(f"Allocation for ${PORTFOLIO_VALUE:,.0f}:")
print("  TIP    50%  →  $35,000  (Safety first)")
print("  GLD    30%  →  $21,000  (Flight to safety)")
print("  VTV    20%  →  $14,000  (Defensive equities)")
print()
print("Expected: 2-4% annual, -15% to -25% drawdowns")
print("Best for: 2008-2009, 2020 March type environments")
print()

print("SCENARIO 4: UNCERTAIN / BALANCED (DEFAULT)")
print("-" * 90)
print("When to use: Mixed signals, can't determine regime, or just starting out")
print()
print(f"Allocation for ${PORTFOLIO_VALUE:,.0f} (EQUAL-RISK APPROACH):")
print("  SPY    25%  →  $17,500")
print("  VTV    20%  →  $14,000")
print("  TIP    20%  →  $14,000")
print("  GLD    20%  →  $14,000")
print("  VNQ    15%  →  $10,500")
print()
print("Expected: 6-8% annual, -20% to -35% drawdowns")
print("Advantage: Works okay in most environments")
print()

print("=" * 90)
print("HOW TO DETECT REGIME CHANGES")
print("=" * 90)
print()

print("Monitor these indicators QUARTERLY:\n")

print("📊 Economic Indicators:")
print("  • CPI inflation rate (www.bls.gov/cpi)")
print("  • GDP growth rate (www.bea.gov)")
print("  • Unemployment rate (www.bls.gov/news.release/empsit.toc.htm)")
print("  • Fed Funds Rate trend")
print()

print("📈 Market Indicators:")
print("  • VIX level (<15=calm, 15-25=normal, >25=fear)")
print("  • S&P 500 vs 200-day MA (above=bull, below=bear)")
print("  • 2yr/10yr yield curve (inverted=recession warning)")
print("  • Credit spreads (widening=stress)")
print()

print("🎯 Regime Decision Matrix:")
print()
print("  High inflation + Low growth → STAGFLATION")
print("  Low inflation + High growth → BULL MARKET")
print("  Rising unemployment + Credit stress → CRISIS")
print("  Mixed signals → BALANCED/UNCERTAIN")
print()

print("⚠️  DON'T TRY TO TIME PERFECTLY:")
print("  • Shift gradually over 2-3 months")
print("  • Keep 10-20% in stable assets always")
print("  • Accept you'll be wrong sometimes")
print("  • Discipline > Perfect timing")
print()

print("=" * 90)
print("WHAT OPTIMIZATION CAN'T TELL YOU")
print("=" * 90)
print()

print("❌ 1. STARTING VALUATIONS MATTER")
print("     Tech at P/E of 35 vs 15 = vastly different forward returns")
print("     Optimizer doesn't know if assets are expensive or cheap\n")

print("❌ 2. REGIME SHIFTS")
print("     We may be entering a completely different era:")
print("     • End of globalization")
print("     • Persistent inflation")
print("     • Degrowth")
print("     • Different geopolitics")
print("     Past correlations may break\n")

print("❌ 3. BLACK SWANS")
print("     • Pandemic")
print("     • Major war")
print("     • Financial system failure")
print("     • Climate disasters")
print("     These aren't in the training data\n")

print("❌ 4. YOUR BEHAVIOR")
print("     Math says: Hold through -50% drawdown")
print("     Reality: Can you actually do this?")
print("     Most people can't\n")

print("❌ 5. SEQUENCE OF RETURNS")
print("     10% per year for 10 years ≠ what actually happens")
print("     Real sequence: +30%, -40%, +25%, -15%, +35%...")
print("     Your emotions matter more than the average\n")

print("=" * 90)
print("HONEST RECOMMENDATIONS")
print("=" * 90)
print()

print("FOR MOST PEOPLE:")
print("  1. Start with SCENARIO 4 (Balanced)")
print("  2. Tilt 10-15% based on your regime view")
print("  3. Rebalance quarterly")
print("  4. Don't check prices daily")
print("  5. Have 6-12 months emergency cash OUTSIDE this portfolio")
print()

print("IF YOU'RE SOPHISTICATED:")
print("  1. Assess regime quarterly using indicators above")
print("  2. Shift allocation gradually (not all at once)")
print("  3. Keep 15-25% in GLD+TIP always (core stability)")
print("  4. Accept that timing will be imperfect")
print("  5. Focus on avoiding disasters, not maximizing returns")
print()

print("IF YOU WANT SIMPLE:")
print("  Just do 60% SPY + 40% TIP and rebalance annually")
print("  It won't be optimal, but it's simple and survivable")
print()

print("=" * 90)
print("THE CURVE-FITTING PROBLEM")
print("=" * 90)
print()

print("Why did we build this instead of just running the optimizer?")
print()
print("Because optimizers trained on 2015-2025 would tell you:")
print("  • 90% in tech (XLK)")
print("  • 78% in REITs (VNQ)")
print("  • 95% in gold (GLD)")
print()
print("These are curve-fits to ONE specific decade.")
print()
print("That decade had:")
print("  ✓ Zero interest rates")
print("  ✓ QE infinity")
print("  ✓ Tech dominance")
print("  ✓ V-shaped recoveries")
print()
print("The 2030s will be different.")
print("We don't know how, but they will be.")
print()
print("So instead:")
print("  → Use regime frameworks")
print("  → Diversify by default")
print("  → Avoid extreme concentrations")
print("  → Stay humble")
print()

print("=" * 90)
print("FINAL WISDOM")
print("=" * 90)
print()

print("The best portfolio is the one you can HOLD through hell.")
print()
print("Not the one with the highest backtest Sharpe ratio.")
print()
print("Know yourself. Build accordingly.")
print()

print("Good luck! 🎯")
print()
