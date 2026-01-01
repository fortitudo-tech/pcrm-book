# Portfolio Templates for Different Investor Types

Copy one of these ticker lists into `my_portfolio_optimizer.py` line 21-29

---

## 🟢 CONSERVATIVE (Low Risk, Income Focus)

**Best for:** Retirees, risk-averse investors, ages 60+

```python
tickers = [
    'BND',   # Total Bond Market
    'TLT',   # Long-term Treasury Bonds
    'XLP',   # Consumer Staples
    'XLU',   # Utilities
    'XLV',   # Health Care
    'SCHD',  # Dividend Aristocrats
    'GLD',   # Gold
]

years_of_history = 5
return_period = 63  # Quarterly rebalancing
cvar_alpha = 0.95   # Very conservative (worst 5%)
```

**Expected:** Low volatility, steady income, capital preservation

---

## 🟡 BALANCED (Moderate Risk, Growth + Income)

**Best for:** Ages 40-60, balanced approach

```python
tickers = [
    'SPY',   # S&P 500
    'QQQ',   # Nasdaq Tech
    'VEA',   # Developed International
    'VWO',   # Emerging Markets
    'XLP',   # Consumer Staples
    'XLV',   # Health Care
    'BND',   # Total Bond Market
    'GLD',   # Gold
]

years_of_history = 5
return_period = 63  # Quarterly rebalancing
cvar_alpha = 0.90   # Moderate risk focus
```

**Expected:** Balanced growth and protection, moderate volatility

---

## 🔴 AGGRESSIVE (High Risk, Maximum Growth)

**Best for:** Ages 20-40, high risk tolerance, long time horizon

```python
tickers = [
    'QQQ',   # Nasdaq 100 (Tech)
    'XLK',   # Technology Sector
    'XLY',   # Consumer Discretionary
    'VWO',   # Emerging Markets
    'ARKK',  # ARK Innovation (High Beta)
    'SMH',   # Semiconductors
    'ICLN',  # Clean Energy
    'SPY',   # S&P 500 (Core)
]

years_of_history = 3
return_period = 21  # Monthly rebalancing (more active)
cvar_alpha = 0.85   # Focus on worst 15% (accept more risk)
```

**Expected:** High growth potential, high volatility, bigger drawdowns

---

## 🌍 GLOBAL DIVERSIFICATION

**Best for:** International exposure, currency diversification

```python
tickers = [
    'SPY',   # US Large Cap
    'VEA',   # Developed Markets (Europe, Japan)
    'VWO',   # Emerging Markets (China, India)
    'VNQ',   # US Real Estate
    'VNQI',  # International Real Estate
    'GLD',   # Gold
    'TLT',   # US Treasuries
    'BWX',   # International Bonds
]

years_of_history = 5
return_period = 63
cvar_alpha = 0.90
```

**Expected:** Geographic diversification, currency hedge

---

## 💰 DIVIDEND INCOME MAXIMIZER

**Best for:** Income investors, retirees

```python
tickers = [
    'SCHD',  # Dividend Aristocrats
    'VYM',   # High Dividend Yield
    'DGRO',  # Dividend Growth
    'XLP',   # Consumer Staples
    'XLU',   # Utilities
    'VNQ',   # Real Estate (REITs)
    'BND',   # Bonds
]

years_of_history = 5
return_period = 126  # Semi-annual (longer hold)
cvar_alpha = 0.95    # Very conservative
```

**Expected:** High dividend yield, lower total return, stability

---

## 🏦 SECTOR ROTATION (Advanced)

**Best for:** Active investors, sector tacticians

```python
tickers = [
    'XLB',   # Materials
    'XLE',   # Energy
    'XLF',   # Financials
    'XLI',   # Industrials
    'XLK',   # Technology
    'XLP',   # Consumer Staples
    'XLU',   # Utilities
    'XLV',   # Health Care
    'XLY',   # Consumer Discretionary
]

years_of_history = 3
return_period = 21   # Monthly rebalancing
cvar_alpha = 0.90
```

**Expected:** Active sector rotation, requires monitoring

---

## 🛡️ ALL-WEATHER PORTFOLIO (Inspired by Ray Dalio)

**Best for:** Set-it-and-forget-it, crisis-resistant

```python
tickers = [
    'SPY',   # Stocks (30%)
    'TLT',   # Long-term Bonds (40%)
    'IEF',   # Intermediate Bonds (15%)
    'GLD',   # Gold (7.5%)
    'DBC',   # Commodities (7.5%)
]

years_of_history = 10
return_period = 252  # Yearly rebalancing
cvar_alpha = 0.95    # Maximum protection
```

**Expected:** Smooth returns across all economic environments

---

## 🚀 CRYPTO-ENHANCED PORTFOLIO (High Risk)

**Best for:** Crypto believers with risk tolerance

```python
tickers = [
    'SPY',   # S&P 500 (Core 50%)
    'QQQ',   # Tech (20%)
    'BITO',  # Bitcoin Strategy ETF (10%)
    'GLD',   # Gold (10%)
    'TLT',   # Bonds (10%)
]

years_of_history = 2
return_period = 21
cvar_alpha = 0.85
```

**Expected:** High volatility, crypto exposure, potential for large gains/losses

---

## 📊 HOW TO USE THESE TEMPLATES

1. **Copy the entire ticker list** from your chosen template
2. **Paste it into** `my_portfolio_optimizer.py` at line 21
3. **Adjust parameters** if desired:
   - `years_of_history`: How much historical data to use
   - `return_period`: Optimization horizon (21=monthly, 63=quarterly)
   - `cvar_alpha`: Risk focus (0.95=very safe, 0.85=riskier)
4. **Run the script:** `python my_portfolio_optimizer.py`
5. **Review the output** and execute in Fidelity

---

## 🎯 QUICK COMPARISON

| Template | Risk Level | Expected Return | Best For |
|----------|-----------|----------------|----------|
| Conservative | ⭐ | 4-6% | Retirees |
| Balanced | ⭐⭐⭐ | 7-9% | Most investors |
| Aggressive | ⭐⭐⭐⭐⭐ | 10-15% | Young investors |
| Global | ⭐⭐⭐ | 7-10% | Diversifiers |
| Dividend | ⭐⭐ | 5-7% | Income seekers |
| Sector Rotation | ⭐⭐⭐⭐ | 9-12% | Active traders |
| All-Weather | ⭐⭐ | 6-8% | Set-and-forget |
| Crypto-Enhanced | ⭐⭐⭐⭐⭐ | 10-20%* | Risk takers |

*Crypto portfolios can have extreme variance

---

## 💡 PRO TIPS

**Mixing Templates:**
You can combine tickers from different templates! For example:

```python
tickers = [
    # 60% from Balanced
    'SPY', 'QQQ', 'VEA',
    # 30% from Dividend
    'SCHD', 'VYM',
    # 10% from Conservative
    'GLD', 'BND',
]
```

**Backtesting:**
Change `years_of_history` to see how the portfolio would have performed:
- `years_of_history = 3` → Recent performance
- `years_of_history = 10` → Includes 2008 crisis
- `years_of_history = 15` → Long-term stability test

**Rebalancing Frequency:**
- `return_period = 21` → Monthly (active, more trades)
- `return_period = 63` → Quarterly (recommended)
- `return_period = 126` → Semi-annual (passive)
- `return_period = 252` → Annual (very passive)

**Risk Tolerance:**
- `cvar_alpha = 0.95` → Very conservative (focus on worst 5%)
- `cvar_alpha = 0.90` → Moderate (worst 10%)
- `cvar_alpha = 0.85` → Aggressive (worst 15%)
