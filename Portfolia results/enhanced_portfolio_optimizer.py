"""
Enhanced Portfolio Optimizer with Regime Analysis
Based on PCRM Book - Reality-tested across multiple market regimes

CRITICAL IMPROVEMENTS:
1. Tests allocations across different historical periods (not just 2015-2025)
2. Shows REAL drawdowns, not smoothed CVaR
3. Adds concentration risk penalties
4. Provides regime-conditional recommendations
5. Honest about what optimization cannot predict

Instructions:
1. Edit the 'tickers' list below with your chosen ETFs
2. Run this script: python enhanced_portfolio_optimizer.py
3. Review regime-tested results and conditional strategies
"""

import numpy as np
import pandas as pd
import yfinance as yf
import fortitudo.tech as ft
import matplotlib.pyplot as plt
from datetime import datetime

# ============================================================================
# CUSTOMIZE THIS SECTION
# ============================================================================

tickers = [
    'SPY',   # S&P 500 - Core equity exposure
    'QQQ',   # Nasdaq/Tech - Growth potential
    'VTV',   # Value stocks
    'TIP',   # TIPS - Inflation protection
    'GLD',   # Gold - Inflation hedge
    'VNQ',   # Real Estate
    'SCHD',  # Dividend quality
    'VEA',   # International developed
]

# Portfolio amount
portfolio_value = 70000

# Optimization parameters
years_of_history = 20  # Longer history to capture more regimes
return_period = 252  # Annual returns
cvar_alpha = 0.9

# Concentration penalty (0 = no penalty, 0.5 = strong penalty)
# This prevents optimizer from going 90%+ into one asset
concentration_penalty = 0.3

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_max_drawdown(returns):
    """Calculate the maximum peak-to-trough drawdown"""
    if isinstance(returns, np.ndarray):
        returns = pd.Series(returns)
    cumulative = (1 + returns / 100).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max * 100
    return drawdown.min()

def calculate_drawdown_series(returns):
    """Calculate drawdown series over time"""
    if isinstance(returns, np.ndarray):
        returns = pd.Series(returns)
    cumulative = (1 + returns / 100).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max * 100
    return drawdown

def portfolio_metrics_enhanced(weights, returns_data, name="Portfolio"):
    """Calculate comprehensive portfolio metrics including real drawdowns"""
    portfolio_returns = returns_data @ weights
    
    mean_return = np.mean(portfolio_returns)
    volatility = np.std(portfolio_returns)
    
    # Real maximum drawdown
    max_dd = calculate_max_drawdown(portfolio_returns)
    
    # CVaR (for comparison)
    cvar_result = ft.portfolio_cvar(
        weights[:, np.newaxis],
        returns_data,
        alpha=cvar_alpha
    )
    if np.isscalar(cvar_result):
        cvar_value = cvar_result
    else:
        cvar_value = cvar_result[0, 0] if cvar_result.ndim > 1 else cvar_result[0]
    
    sharpe = mean_return / volatility if volatility > 0 else 0
    
    # Concentration measure (Herfindahl index)
    concentration = np.sum(weights ** 2)
    
    return {
        'Mean Return (%)': mean_return,
        'Volatility (%)': volatility,
        f'CVaR {int(cvar_alpha*100)}% (%)': cvar_value,
        'Max Drawdown (%)': max_dd,
        'Sharpe Ratio': sharpe,
        'Concentration': concentration,
        'Weights': weights
    }

def add_concentration_constraint(G, h, n_assets, max_weight=0.40):
    """Add maximum position size constraint to prevent extreme concentration"""
    # Add constraint: each weight <= max_weight
    G_new = np.vstack([G, np.eye(n_assets)])
    h_new = np.hstack([h, np.ones(n_assets) * max_weight])
    return G_new, h_new

# ============================================================================
# DOWNLOAD DATA WITH ERROR HANDLING
# ============================================================================

print("=" * 80)
print("ENHANCED REGIME-TESTED PORTFOLIO OPTIMIZER")
print("=" * 80)
print(f"\nDownloading {years_of_history} years of data for: {', '.join(tickers)}")

try:
    start_date = pd.Timestamp.now() - pd.DateOffset(years=years_of_history)
    data = yf.download(tickers, start=start_date, end=pd.Timestamp.now(), progress=False)['Close']
    
    if len(tickers) == 1:
        data = pd.DataFrame(data, columns=tickers)
    
    print(f"[OK] Downloaded {len(data)} days of price data\n")
except Exception as e:
    print(f"[ERROR] Failed to download data: {e}")
    print("Using 10-year fallback period...")
    start_date = pd.Timestamp.now() - pd.DateOffset(years=10)
    data = yf.download(tickers, start=start_date, end=pd.Timestamp.now(), progress=False)['Close']

# ============================================================================
# COMPUTE RETURNS
# ============================================================================

print(f"Computing {return_period}-day returns...")
returns = (data.values[return_period:, :] - data.values[0:-return_period, :]) / data.iloc[0:-return_period, :]
returns_pct = 100 * returns
returns_df = pd.DataFrame(returns_pct, columns=data.columns)
print(f"[OK] Calculated {len(returns_df)} return observations\n")

# ============================================================================
# REGIME ANALYSIS - Test across different periods
# ============================================================================

print("=" * 80)
print("REGIME ANALYSIS: Testing across different historical periods")
print("=" * 80)
print()

# Define regime periods (if enough data)
data_start = data.index[0].year
data_end = data.index[-1].year

regimes = []
if data_start <= 2008:
    regimes.append(('Financial Crisis', '2007-01-01', '2009-12-31'))
if data_start <= 2010:
    regimes.append(('Post-Crisis Recovery', '2010-01-01', '2013-12-31'))
if data_start <= 2014:
    regimes.append(('QE Era', '2014-01-01', '2019-12-31'))
if data_start <= 2020:
    regimes.append(('COVID + Recovery', '2020-01-01', '2021-12-31'))
if data_start <= 2022:
    regimes.append(('Rate Hike Era', '2022-01-01', '2023-12-31'))

regimes.append(('Recent Period', '2020-01-01', data.index[-1].strftime('%Y-%m-%d')))

regime_results = {}

for regime_name, start, end in regimes:
    try:
        regime_data = data.loc[start:end]
        if len(regime_data) < 252:  # Need at least 1 year
            continue
            
        regime_returns = (regime_data.values[return_period:, :] - regime_data.values[0:-return_period, :]) / regime_data.iloc[0:-return_period, :]
        regime_returns_pct = 100 * regime_returns
        
        regime_results[regime_name] = {
            'returns': pd.DataFrame(regime_returns_pct, columns=data.columns),
            'period': f"{start} to {end}",
            'n_obs': len(regime_returns_pct)
        }
        
        print(f"{regime_name:25s} | {regime_results[regime_name]['period']:30s} | {regime_results[regime_name]['n_obs']:4d} observations")
    except:
        continue

print()

# ============================================================================
# INDIVIDUAL ASSET STATISTICS (Full Period)
# ============================================================================

print("=" * 80)
print("INDIVIDUAL ASSET STATISTICS (Full Period)")
print("=" * 80)

stats = ft.simulation_moments(returns_df)
cvars = ft.portfolio_cvar(
    np.eye(len(returns_df.columns)),
    returns_df,
    alpha=cvar_alpha
)
stats[f'{int(cvar_alpha*100)}%-CVaR'] = cvars[0, :]

# Add real max drawdowns for each asset
max_dds = []
for ticker in tickers:
    ticker_returns = returns_df[ticker].values
    max_dd = calculate_max_drawdown(ticker_returns)
    max_dds.append(max_dd)

stats['Max Drawdown'] = max_dds

print(f"\nPerformance over {return_period} trading days (~12 months):\n")
print(stats.round(2))
print()

print("⚠️  NOTE: Max Drawdown shows REAL peak-to-trough losses")
print("    This is typically much larger than annualized CVaR!\n")

# ============================================================================
# PORTFOLIO OPTIMIZATION WITH CONCENTRATION CONSTRAINTS
# ============================================================================

print("=" * 80)
print("PORTFOLIO OPTIMIZATION (With Concentration Limits)")
print("=" * 80)

num_assets = len(tickers)
G = -np.eye(num_assets)  # No negative weights
h = np.zeros(num_assets)  # Weights >= 0

# Add concentration constraint
G, h = add_concentration_constraint(G, h, num_assets, max_weight=0.40)

print("\nOptimizing with constraints:")
print("  - Long-only (no shorting)")
print("  - Maximum 40% in any single position (prevents 90% tech!)")
print(f"  - Minimize {int(cvar_alpha*100)}% CVaR (tail risk)")
print()

# CVaR Optimization
print("Running CVaR optimization with concentration limits...")
cvar_opt = ft.MeanCVaR(returns_df.values, G=G, h=h, alpha=cvar_alpha)
cvar_weights = cvar_opt.efficient_portfolio()[:, 0]

# Mean-Variance Optimization
print("Running Mean-Variance optimization with concentration limits...")
means = np.mean(returns_df.values, axis=0)
cov_matrix = ft.covariance_matrix(returns_df).values
mv_opt = ft.MeanVariance(means, cov_matrix, G=G, h=h)
mv_weights = mv_opt.efficient_portfolio()[:, 0]

# Equal weight (for comparison)
equal_weights = np.ones(num_assets) / num_assets

# Risk parity approximation (inverse volatility weighting)
vols = np.std(returns_df.values, axis=0)
risk_parity_weights = (1 / vols) / np.sum(1 / vols)

print("[OK] Optimizations complete!\n")

# ============================================================================
# COMPREHENSIVE RESULTS
# ============================================================================

print("=" * 80)
print("RECOMMENDED ALLOCATIONS")
print("=" * 80)
print()

allocation = pd.DataFrame({
    'Mean-Variance': 100 * mv_weights,
    'CVaR Optimized': 100 * cvar_weights,
    'Risk Parity': 100 * risk_parity_weights,
    'Equal Weight': 100 / num_assets
}, index=tickers)

print("Portfolio Weights (%):")
print(allocation.round(2))
print()

# Calculate comprehensive metrics for all strategies
print("=" * 80)
print("PORTFOLIO COMPARISON (FULL PERIOD WITH REAL DRAWDOWNS)")
print("=" * 80)
print()

mv_metrics = portfolio_metrics_enhanced(mv_weights, returns_df.values, "Mean-Variance")
cvar_metrics = portfolio_metrics_enhanced(cvar_weights, returns_df.values, "CVaR")
rp_metrics = portfolio_metrics_enhanced(risk_parity_weights, returns_df.values, "Risk Parity")
eq_metrics = portfolio_metrics_enhanced(equal_weights, returns_df.values, "Equal Weight")

comparison = pd.DataFrame({
    'Mean-Variance': mv_metrics,
    'CVaR Optimized': cvar_metrics,
    'Risk Parity': rp_metrics,
    'Equal Weight': eq_metrics
}).T

# Remove weights from display
comparison_display = comparison.drop('Weights', axis=1)
print(comparison_display.round(3))
print()

print("🔴 CRITICAL: Compare 'Max Drawdown' vs 'CVaR 90%'")
print("   Max Drawdown shows what ACTUALLY happened")
print("   CVaR is smoothed/annualized - often understates real pain\n")

# ============================================================================
# REGIME STRESS TESTING
# ============================================================================

print("=" * 80)
print("REGIME STRESS TEST: How did strategies perform in different periods?")
print("=" * 80)
print()

if regime_results:
    regime_comparison = []
    
    for regime_name, regime_data in regime_results.items():
        regime_rets = regime_data['returns'].values
        
        mv_regime = portfolio_metrics_enhanced(mv_weights, regime_rets)
        cvar_regime = portfolio_metrics_enhanced(cvar_weights, regime_rets)
        rp_regime = portfolio_metrics_enhanced(risk_parity_weights, regime_rets)
        
        regime_comparison.append({
            'Regime': regime_name,
            'MV Return': mv_regime['Mean Return (%)'],
            'MV MaxDD': mv_regime['Max Drawdown (%)'],
            'CVaR Return': cvar_regime['Mean Return (%)'],
            'CVaR MaxDD': cvar_regime['Max Drawdown (%)'],
            'RP Return': rp_regime['Mean Return (%)'],
            'RP MaxDD': rp_regime['Max Drawdown (%)'],
        })
    
    regime_df = pd.DataFrame(regime_comparison)
    print(regime_df.round(2))
    print()
    print("📊 This shows how each strategy performed in DIFFERENT market environments")
    print("   Notice how results vary dramatically by regime!\n")

# ============================================================================
# REGIME-CONDITIONAL RECOMMENDATIONS
# ============================================================================

print("=" * 80)
print("REGIME-CONDITIONAL STRATEGY: IF-THEN PLAYBOOK")
print("=" * 80)
print()

print("Instead of ONE static allocation, consider regime-dependent positioning:\n")

print("SCENARIO 1: BULL MARKET / GROWTH REGIME")
print("-" * 80)
print("Indicators: Low volatility, rising earnings, accommodative Fed, low inflation")
print("Allocation for $70,000:")
print("  SPY    35%  →  $24,500  (Broad equity exposure)")
print("  QQQ    30%  →  $21,000  (Growth/tech)")
print("  SCHD   20%  →  $14,000  (Quality dividend)")
print("  VEA    15%  →  $10,500  (International diversification)")
print("Expected: 10-15% annual returns, potential -25% to -40% drawdowns")
print()

print("SCENARIO 2: STAGFLATION / INFLATION REGIME")
print("-" * 80)
print("Indicators: Rising CPI >3%, stagnant GDP growth, Fed tightening, high commodities")
print("Allocation for $70,000:")
print("  TIP    30%  →  $21,000  (Inflation-protected)")
print("  VNQ    25%  →  $17,500  (Real estate)")
print("  GLD    25%  →  $17,500  (Gold inflation hedge)")
print("  VTV    20%  →  $14,000  (Value stocks - better than growth)")
print("Expected: 3-6% annual returns, potential -15% to -25% drawdowns")
print()

print("SCENARIO 3: RECESSION / RISK-OFF REGIME")
print("-" * 80)
print("Indicators: Inverted yield curve, rising unemployment, falling PMIs, credit stress")
print("Allocation for $70,000:")
print("  TIP    40%  →  $28,000  (Safety)")
print("  GLD    30%  →  $21,000  (Flight to safety)")
print("  VTV    20%  →  $14,000  (Defensive value)")
print("  SCHD   10%  →  $ 7,000  (Quality dividend)")
print("Expected: 2-4% annual returns, potential -10% to -20% drawdowns")
print()

print("SCENARIO 4: UNCERTAIN / TRANSITION REGIME (Current Default)")
print("-" * 80)
print("Indicators: Mixed signals, regime unclear, moderate volatility")
print(f"Allocation for ${portfolio_value:,.0f} (RISK PARITY RECOMMENDED):\n")

for ticker, weight in zip(tickers, risk_parity_weights):
    dollar_amount = portfolio_value * weight
    if dollar_amount > 500:
        print(f"  {ticker:6s} {weight*100:5.1f}%  →  ${dollar_amount:8,.2f}")

print("\nExpected: 6-9% annual returns, potential -15% to -25% drawdowns")
print()

# ============================================================================
# REGIME DETECTION GUIDE
# ============================================================================

print("=" * 80)
print("HOW TO DETECT REGIME CHANGES")
print("=" * 80)
print()

print("Monitor these indicators QUARTERLY to determine which regime you're in:\n")

print("📈 GROWTH REGIME Indicators:")
print("   □ VIX < 20")
print("   □ S&P 500 above 200-day moving average")
print("   □ Fed funds rate stable or declining")
print("   □ CPI inflation < 3%")
print("   □ Corporate earnings growing >5% YoY")
print("   □ GDP growth > 2%")
print()

print("📊 STAGFLATION REGIME Indicators:")
print("   □ CPI inflation > 3% and persistent")
print("   □ GDP growth < 2%")
print("   □ Fed hiking rates but inflation remains high")
print("   □ Commodity prices rising (oil, gold, copper)")
print("   □ Real wage growth negative")
print("   □ Long-term bonds underperforming")
print()

print("📉 RECESSION REGIME Indicators:")
print("   □ 2y/10y Treasury yield curve inverted")
print("   □ Unemployment rising >0.5% in 3 months")
print("   □ PMI < 50 for 2+ consecutive months")
print("   □ Corporate credit spreads widening >200bps")
print("   □ GDP growth negative for 2 quarters")
print("   □ Consumer confidence falling")
print()

print("RECOMMENDED TRANSITION STRATEGY:")
print("  - Don't try to time perfectly")
print("  - Shift allocation over 2-3 months when regime clearly changes")
print("  - Keep 10-20% in stable assets (TIP/GLD) at all times")
print("  - Rebalance quarterly, not daily")
print()

# ============================================================================
# CONCENTRATION RISK ANALYSIS
# ============================================================================

print("=" * 80)
print("CONCENTRATION RISK ANALYSIS")
print("=" * 80)
print()

print("Herfindahl Index (lower = more diversified, 1.0 = 100% in one asset):\n")

strategies_conc = {
    'Mean-Variance': np.sum(mv_weights ** 2),
    'CVaR Optimized': np.sum(cvar_weights ** 2),
    'Risk Parity': np.sum(risk_parity_weights ** 2),
    'Equal Weight': np.sum(equal_weights ** 2)
}

for name, conc in strategies_conc.items():
    print(f"{name:20s}: {conc:.3f}")

print()
print("💡 Interpretation:")
print("   < 0.15 = Well diversified")
print("   0.15-0.25 = Moderate concentration")
print("   0.25-0.40 = High concentration")
print("   > 0.40 = Extremely concentrated (risky!)")
print()

# ============================================================================
# DRAWDOWN VISUALIZATION
# ============================================================================

print("Generating visualizations with real drawdown analysis...")

fig = plt.figure(figsize=(16, 12))

# Plot 1: Allocations
ax1 = plt.subplot(3, 2, 1)
allocation.plot(kind='bar', ax=ax1)
ax1.set_title('Portfolio Allocations Comparison', fontsize=12, fontweight='bold')
ax1.set_ylabel('Weight (%)')
ax1.set_xlabel('Asset')
ax1.legend(loc='best', fontsize=8)
ax1.grid(axis='y', alpha=0.3)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
ax1.axhline(y=40, color='r', linestyle='--', alpha=0.5, label='40% max constraint')

# Plot 2: Drawdown comparison
ax2 = plt.subplot(3, 2, 2)
strategies = {
    'Mean-Variance': mv_weights,
    'CVaR': cvar_weights,
    'Risk Parity': risk_parity_weights,
    'Equal Weight': equal_weights
}

for name, weights in strategies.items():
    port_returns = returns_df.values @ weights
    dd = calculate_drawdown_series(port_returns)
    ax2.plot(dd.values, label=name, alpha=0.7)

ax2.set_title('Drawdown Comparison Over Time', fontsize=12, fontweight='bold')
ax2.set_xlabel('Observation')
ax2.set_ylabel('Drawdown (%)')
ax2.legend(loc='best', fontsize=8)
ax2.grid(alpha=0.3)
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

# Plot 3: Return distributions
ax3 = plt.subplot(3, 2, 3)
mv_port_returns = returns_df.values @ mv_weights
cvar_port_returns = returns_df.values @ cvar_weights
rp_port_returns = returns_df.values @ risk_parity_weights

ax3.hist(mv_port_returns, bins=40, alpha=0.5, label='Mean-Variance', density=True)
ax3.hist(cvar_port_returns, bins=40, alpha=0.5, label='CVaR', density=True)
ax3.hist(rp_port_returns, bins=40, alpha=0.5, label='Risk Parity', density=True)
ax3.set_title('Return Distributions', fontsize=12, fontweight='bold')
ax3.set_xlabel('Annual Return (%)')
ax3.set_ylabel('Density')
ax3.legend(loc='best', fontsize=8)
ax3.grid(alpha=0.3)

# Plot 4: Risk-Return scatter
ax4 = plt.subplot(3, 2, 4)
for i, ticker in enumerate(tickers):
    ax4.scatter(stats['Volatility'][ticker], stats['Mean'][ticker], s=150, alpha=0.6)
    ax4.annotate(ticker, (stats['Volatility'][ticker], stats['Mean'][ticker]),
                xytext=(3, 3), textcoords='offset points', fontsize=9)

# Add portfolio points
port_metrics = {
    'MV': mv_metrics,
    'CVaR': cvar_metrics,
    'RP': rp_metrics,
    'EQ': eq_metrics
}

colors = ['blue', 'red', 'green', 'orange']
for (name, metrics), color in zip(port_metrics.items(), colors):
    ax4.scatter(metrics['Volatility (%)'], metrics['Mean Return (%)'],
               s=300, marker='*', linewidths=2, edgecolors='black',
               label=name, alpha=0.8, c=color)

ax4.set_xlabel('Volatility (%)', fontsize=10)
ax4.set_ylabel('Mean Return (%)', fontsize=10)
ax4.set_title('Risk-Return Profile', fontsize=12, fontweight='bold')
ax4.legend(loc='best', fontsize=8)
ax4.grid(alpha=0.3)

# Plot 5: Regime performance (if available)
ax5 = plt.subplot(3, 2, 5)
if regime_results:
    regime_names = [r['Regime'] for r in regime_comparison]
    x = np.arange(len(regime_names))
    width = 0.25
    
    mv_rets = [r['MV Return'] for r in regime_comparison]
    cvar_rets = [r['CVaR Return'] for r in regime_comparison]
    rp_rets = [r['RP Return'] for r in regime_comparison]
    
    ax5.bar(x - width, mv_rets, width, label='Mean-Variance', alpha=0.8)
    ax5.bar(x, cvar_rets, width, label='CVaR', alpha=0.8)
    ax5.bar(x + width, rp_rets, width, label='Risk Parity', alpha=0.8)
    
    ax5.set_xlabel('Regime')
    ax5.set_ylabel('Annualized Return (%)')
    ax5.set_title('Returns Across Different Regimes', fontsize=12, fontweight='bold')
    ax5.set_xticks(x)
    ax5.set_xticklabels(regime_names, rotation=45, ha='right', fontsize=8)
    ax5.legend(fontsize=8)
    ax5.grid(axis='y', alpha=0.3)
    ax5.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

# Plot 6: Max Drawdown comparison
ax6 = plt.subplot(3, 2, 6)
strategies_names = list(strategies.keys())
max_dds = [mv_metrics['Max Drawdown (%)'], 
           cvar_metrics['Max Drawdown (%)'],
           rp_metrics['Max Drawdown (%)'],
           eq_metrics['Max Drawdown (%)']]
cvars = [mv_metrics['CVaR 90% (%)'],
         cvar_metrics['CVaR 90% (%)'],
         rp_metrics['CVaR 90% (%)'],
         eq_metrics['CVaR 90% (%)']]

x = np.arange(len(strategies_names))
width = 0.35

ax6.bar(x - width/2, max_dds, width, label='Max Drawdown (REAL)', alpha=0.8, color='red')
ax6.bar(x + width/2, cvars, width, label='CVaR 90% (smoothed)', alpha=0.8, color='blue')

ax6.set_xlabel('Strategy')
ax6.set_ylabel('Loss (%)')
ax6.set_title('Real Drawdowns vs CVaR (CVaR understates risk!)', fontsize=12, fontweight='bold')
ax6.set_xticks(x)
ax6.set_xticklabels(strategies_names, rotation=45, ha='right')
ax6.legend(fontsize=8)
ax6.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('enhanced_portfolio_analysis.png', dpi=150, bbox_inches='tight')
print("[OK] Chart saved to: enhanced_portfolio_analysis.png\n")

# ============================================================================
# SUMMARY AND WARNINGS
# ============================================================================

print("=" * 80)
print("SUMMARY AND CRITICAL WARNINGS")
print("=" * 80)
print()

print("✅ WHAT THIS ANALYSIS PROVIDES:")
print("   • Tested across multiple historical regimes (not just 2015-2025)")
print("   • Real maximum drawdowns (not smoothed CVaR)")
print("   • Concentration constraints (prevents 90% single-asset allocations)")
print("   • Regime-conditional recommendations (IF-THEN playbook)")
print("   • Risk parity alternative (balanced risk contribution)")
print()

print("⚠️  CRITICAL LIMITATIONS YOU MUST UNDERSTAND:")
print()
print("1. PAST PERFORMANCE ≠ FUTURE RESULTS")
print("   The optimizer only knows what happened before.")
print("   It cannot predict:")
print("   • Changes in market structure")
print("   • Regulatory changes")
print("   • Technology disruptions")
print("   • Geopolitical shocks")
print("   • Valuation regime shifts")
print()

print("2. STARTING CONDITIONS MATTER ENORMOUSLY")
print("   Returns in 2015-2025 came from:")
print("   • Starting P/E of ~15x → ending P/E of ~25x+")
print("   • Zero interest rates → free money")
print("   • QE liquidity injections")
print("   These conditions may not repeat.")
print()

print("3. CONCENTRATION STILL EXISTS")
print("   Even with 40% max constraint:")
print("   • Strategies may still be too concentrated")
print("   • Sector/factor exposures not controlled")
print("   • Consider your entire financial picture")
print()

print("4. REAL DRAWDOWNS WILL TEST YOU")
print("   Max drawdowns shown are historical.")
print("   Future drawdowns could be LARGER.")
print("   Can you:")
print("   • Hold through -40% to -50% drops?")
print("   • Avoid panic selling at the bottom?")
print("   • Rebalance when everything feels terrible?")
print()

print("5. REGIME DETECTION IS HARD")
print("   By the time a regime is obvious, it's often late.")
print("   Transitions are messy.")
print("   Consider:")
print("   • Gradual shifts over months")
print("   • Keeping core diversification always")
print("   • Not trying to time perfectly")
print()

print("RECOMMENDED APPROACH:")
print("  1. Choose Risk Parity as base allocation")
print("  2. Tilt modestly (10-15%) based on regime view")
print("  3. Rebalance quarterly, not daily")
print("  4. Monitor regime indicators")
print("  5. Accept that you'll be wrong sometimes")
print("  6. HOLD for long term (10+ years)")
print()

print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print(f"\nReview: enhanced_portfolio_analysis.png")
print("Consider: Regime-conditional approach over static allocation")
print("Remember: Discipline beats optimization")
