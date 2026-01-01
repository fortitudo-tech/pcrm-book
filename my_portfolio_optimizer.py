"""
Simple Portfolio Optimizer for Retail Investors
Based on PCRM Book - Customized for your Fidelity account

Instructions:
1. Edit the 'tickers' list below with your chosen ETFs
2. Run this script: python my_portfolio_optimizer.py
3. Review the recommended allocation
"""

import numpy as np
import pandas as pd
import yfinance as yf
import fortitudo.tech as ft
import matplotlib.pyplot as plt

# ============================================================================
# CUSTOMIZE THIS SECTION - Add your ETFs here!
# ============================================================================

tickers = [
    'SPY',   # S&P 500
    'QQQ',   # Nasdaq 100 (Tech)
    'XLP',   # Consumer Staples
    'XLV',   # Health Care
    'XLU',   # Utilities
    'GLD',   # Gold
    'TLT',   # 20+ Year Treasury Bonds
]

# How many years of historical data to use?
years_of_history = 5

# What return period to optimize for? (in trading days)
# 21 = 1 month, 63 = 3 months, 252 = 1 year
return_period = 63  # 3 months (quarterly)

# CVaR confidence level (0.9 = focus on worst 10% of scenarios)
cvar_alpha = 0.9

# ============================================================================
# DOWNLOAD DATA
# ============================================================================

print("=" * 70)
print("PORTFOLIO OPTIMIZER FOR RETAIL INVESTORS")
print("=" * 70)
print(f"\nDownloading {years_of_history} years of data for: {', '.join(tickers)}")

start_date = pd.Timestamp.now() - pd.DateOffset(years=years_of_history)
data = yf.download(tickers, start=start_date, end=pd.Timestamp.now())['Close']

if len(tickers) == 1:
    data = pd.DataFrame(data, columns=tickers)

print(f"✓ Downloaded {len(data)} days of price data\n")

# ============================================================================
# COMPUTE RETURNS
# ============================================================================

print(f"Computing {return_period}-day returns...")

# Calculate overlapping period returns
returns = (data.values[return_period:, :] - data.values[0:-return_period, :]) / data.iloc[0:-return_period, :]
returns_pct = 100 * returns  # Convert to percentage
returns_df = pd.DataFrame(returns_pct, columns=data.columns)

print(f"✓ Calculated {len(returns_df)} return observations\n")

# ============================================================================
# ANALYZE EACH ASSET
# ============================================================================

print("=" * 70)
print("INDIVIDUAL ASSET STATISTICS")
print("=" * 70)

# Compute statistics
stats = ft.simulation_moments(returns_df)

# Compute CVaR for each asset
cvars = ft.portfolio_cvar(
    np.eye(len(returns_df.columns)),
    returns_df,
    alpha=cvar_alpha
)
stats[f'{int(cvar_alpha*100)}%-CVaR'] = cvars[0, :]

print("\nPerformance over", return_period, "trading days (~", return_period//21, "months):\n")
print(stats.round(2))
print()

# ============================================================================
# PORTFOLIO OPTIMIZATION
# ============================================================================

print("=" * 70)
print("PORTFOLIO OPTIMIZATION")
print("=" * 70)

# Set up constraints (long-only, no shorting)
num_assets = len(tickers)
G = -np.eye(num_assets)  # No negative weights
h = np.zeros(num_assets)  # Weights >= 0

print("\nOptimizing with constraints:")
print("  - Long-only (no shorting)")
print(f"  - Minimize {int(cvar_alpha*100)}% CVaR (tail risk)")
print()

# CVaR Optimization
print("Running CVaR optimization...")
cvar_opt = ft.MeanCVaR(returns_df.values, G=G, h=h, alpha=cvar_alpha)
cvar_weights = cvar_opt.efficient_portfolio()[:, 0]

# Mean-Variance Optimization (traditional approach)
print("Running Mean-Variance optimization (for comparison)...")
means = np.mean(returns_df.values, axis=0)
cov_matrix = ft.covariance_matrix(returns_df).values
mv_opt = ft.MeanVariance(means, cov_matrix, G=G, h=h)
mv_weights = mv_opt.efficient_portfolio()[:, 0]

print("✓ Optimizations complete!\n")

# ============================================================================
# RESULTS
# ============================================================================

print("=" * 70)
print("RECOMMENDED ALLOCATIONS")
print("=" * 70)
print()

# Create results dataframe
allocation = pd.DataFrame({
    'CVaR Optimized': 100 * cvar_weights,
    'Mean-Variance': 100 * mv_weights,
    'Equal Weight': 100 / num_assets
}, index=tickers)

print("Portfolio Weights (%):")
print(allocation.round(2))
print()

# Calculate portfolio metrics
def portfolio_metrics(weights, returns_data):
    """Calculate key portfolio metrics"""
    portfolio_returns = returns_data @ weights
    mean_return = np.mean(portfolio_returns)
    volatility = np.std(portfolio_returns)
    cvar_value = ft.portfolio_cvar(
        weights[:, np.newaxis],
        returns_data,
        alpha=cvar_alpha
    )[0, 0]
    sharpe = mean_return / volatility if volatility > 0 else 0

    return {
        'Mean Return (%)': mean_return,
        'Volatility (%)': volatility,
        f'CVaR {int(cvar_alpha*100)}% (%)': cvar_value,
        'Sharpe Ratio': sharpe
    }

# Compare all three approaches
print("=" * 70)
print("PORTFOLIO COMPARISON")
print("=" * 70)
print()

comparison = pd.DataFrame({
    'CVaR Optimized': portfolio_metrics(cvar_weights, returns_df.values),
    'Mean-Variance': portfolio_metrics(mv_weights, returns_df.values),
    'Equal Weight': portfolio_metrics(np.ones(num_assets)/num_assets, returns_df.values)
})

print(comparison.round(3))
print()

# ============================================================================
# ACTIONABLE ADVICE
# ============================================================================

print("=" * 70)
print("HOW TO EXECUTE IN FIDELITY")
print("=" * 70)
print()

# Assume $10,000 portfolio for example
portfolio_value = 10000

print(f"For a ${portfolio_value:,.0f} portfolio, buy:")
print()

for ticker, weight in zip(tickers, cvar_weights):
    dollar_amount = portfolio_value * weight
    print(f"  {ticker:6s} {weight*100:6.2f}%  →  ${dollar_amount:8.2f}")

print()
print("Next steps:")
print("  1. Log into Fidelity")
print("  2. Navigate to Trade → Stocks/ETFs")
print("  3. Buy each ETF with the dollar amounts above")
print("  4. Set calendar reminder to rebalance quarterly")
print()

# ============================================================================
# VISUALIZATION
# ============================================================================

print("Generating visualizations...")

# Plot 1: Allocation comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

allocation.plot(kind='bar', ax=ax1)
ax1.set_title('Portfolio Allocations Comparison')
ax1.set_ylabel('Weight (%)')
ax1.set_xlabel('Asset')
ax1.legend(loc='best')
ax1.grid(axis='y', alpha=0.3)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Plot 2: Return distributions for CVaR vs Mean-Variance
cvar_portfolio_returns = returns_df.values @ cvar_weights
mv_portfolio_returns = returns_df.values @ mv_weights

ax2.hist(cvar_portfolio_returns, bins=50, alpha=0.6, label='CVaR Optimized', density=True)
ax2.hist(mv_portfolio_returns, bins=50, alpha=0.6, label='Mean-Variance', density=True)
ax2.axvline(np.percentile(cvar_portfolio_returns, (1-cvar_alpha)*100),
            color='blue', linestyle='--', alpha=0.7, label=f'CVaR {int(cvar_alpha*100)}%')
ax2.axvline(np.percentile(mv_portfolio_returns, (1-cvar_alpha)*100),
            color='orange', linestyle='--', alpha=0.7, label=f'MV {int(cvar_alpha*100)}%')
ax2.set_title(f'Portfolio Return Distributions ({return_period}-day)')
ax2.set_xlabel('Return (%)')
ax2.set_ylabel('Density')
ax2.legend(loc='best')
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/home/user/pcrm-book/my_portfolio_results.png', dpi=150, bbox_inches='tight')
print(f"✓ Chart saved to: my_portfolio_results.png")
print()

# Plot 3: Individual asset risk-return scatter
fig, ax = plt.subplots(figsize=(10, 8))

for i, ticker in enumerate(tickers):
    ax.scatter(stats['Volatility'][ticker], stats['Mean'][ticker], s=200, alpha=0.6)
    ax.annotate(ticker, (stats['Volatility'][ticker], stats['Mean'][ticker]),
                xytext=(5, 5), textcoords='offset points', fontsize=10)

# Add portfolio points
for name, weights in [('CVaR Portfolio', cvar_weights), ('MV Portfolio', mv_weights)]:
    metrics = portfolio_metrics(weights, returns_df.values)
    ax.scatter(metrics['Volatility (%)'], metrics['Mean Return (%)'],
               s=400, marker='*', linewidths=2, edgecolors='black',
               label=name, alpha=0.8)

ax.set_xlabel(f'Volatility (%) - {return_period} days', fontsize=12)
ax.set_ylabel(f'Mean Return (%) - {return_period} days', fontsize=12)
ax.set_title('Risk-Return Profile: Individual Assets vs Portfolios', fontsize=14)
ax.legend(loc='best')
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/home/user/pcrm-book/my_risk_return_chart.png', dpi=150, bbox_inches='tight')
print(f"✓ Chart saved to: my_risk_return_chart.png")

plt.show()

print()
print("=" * 70)
print("DONE! Review the results above and the saved charts.")
print("=" * 70)
