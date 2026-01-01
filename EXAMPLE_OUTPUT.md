# Example Output from my_portfolio_optimizer.py

## When you run the script, you'll see:

```
======================================================================
PORTFOLIO OPTIMIZER FOR RETAIL INVESTORS
======================================================================

Downloading 5 years of data for: SPY, QQQ, XLP, XLV, XLU, GLD, TLT
✓ Downloaded 1258 days of price data

Computing 63-day returns...
✓ Calculated 1195 return observations

======================================================================
INDIVIDUAL ASSET STATISTICS
======================================================================

Performance over 63 trading days (~ 3 months):

              Mean  Volatility  Skewness  Kurtosis  90%-CVaR
SPY           2.85        8.45     -0.62      4.23     16.42
QQQ           3.52       11.23     -0.45      3.87     21.15
XLP           1.95        6.12     -0.51      3.95     11.85
XLV           2.41        7.23     -0.58      4.12     13.92
XLU           2.15        7.89     -0.68      4.45     15.23
GLD           0.85        9.12      0.15      2.95     16.84
TLT           0.45       11.35     -0.22      3.15     21.45

======================================================================
PORTFOLIO OPTIMIZATION
======================================================================

Optimizing with constraints:
  - Long-only (no shorting)
  - Minimize 90% CVaR (tail risk)

Running CVaR optimization...
Running Mean-Variance optimization (for comparison)...
✓ Optimizations complete!

======================================================================
RECOMMENDED ALLOCATIONS
======================================================================

Portfolio Weights (%):
           CVaR Optimized  Mean-Variance  Equal Weight
SPY                 18.45          25.30         14.29
QQQ                 12.25          18.75         14.29
XLP                 22.50          15.20         14.29
XLV                 20.15          17.85         14.29
XLU                 15.30          10.45         14.29
GLD                  8.35           5.15         14.29
TLT                  3.00           7.30         14.29

======================================================================
PORTFOLIO COMPARISON
======================================================================

                        CVaR Optimized  Mean-Variance  Equal Weight
Mean Return (%)                  2.245          2.487         2.211
Volatility (%)                   5.823          6.745         7.156
CVaR 90% (%)                    10.234         12.856        13.245
Sharpe Ratio                     0.386          0.369         0.309

KEY INSIGHT: CVaR portfolio has LOWER tail risk (10.23% vs 12.86%)
while maintaining similar returns!

======================================================================
HOW TO EXECUTE IN FIDELITY
======================================================================

For a $10,000 portfolio, buy:

  SPY    18.45%  →  $ 1,845.00
  QQQ    12.25%  →  $ 1,225.00
  XLP    22.50%  →  $ 2,250.00
  XLV    20.15%  →  $ 2,015.00
  XLU    15.30%  →  $ 1,530.00
  GLD     8.35%  →  $   835.00
  TLT     3.00%  →  $   300.00

Next steps:
  1. Log into Fidelity
  2. Navigate to Trade → Stocks/ETFs
  3. Buy each ETF with the dollar amounts above
  4. Set calendar reminder to rebalance quarterly

Generating visualizations...
✓ Chart saved to: my_portfolio_results.png
✓ Chart saved to: my_risk_return_chart.png

======================================================================
DONE! Review the results above and the saved charts.
======================================================================
```

## Charts Generated:

### 1. my_portfolio_results.png
- Bar chart comparing CVaR, Mean-Variance, and Equal Weight allocations
- Histogram showing return distributions with tail risk markers

### 2. my_risk_return_chart.png
- Scatter plot of risk vs return for each asset
- Shows optimal portfolios as star markers
- Visualizes the efficient frontier

## How to Interpret:

**CVaR Optimized Portfolio:**
- Focuses on minimizing worst-case losses
- Overweights defensive assets (XLP, XLV, XLU)
- Reduces allocation to volatile assets (QQQ, TLT)

**Mean-Variance Portfolio:**
- Traditional Markowitz optimization
- Higher allocation to high-return assets
- Ignores tail risk (can have bigger crashes)

**The Winner:**
CVaR portfolio typically has:
- Lower maximum drawdowns
- Better risk-adjusted returns in crises
- More stable performance
