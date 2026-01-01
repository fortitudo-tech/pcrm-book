# 🚀 QUICK START GUIDE - Portfolio Optimizer

## 5-Minute Setup

### 1. Install (One Time Only)

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/fortitudo-tech/pcrm-book.git
cd pcrm-book

# Create Python environment
conda env create -f environment.yml

# Activate it
conda activate pcrm-book
```

---

### 2. Choose Your Portfolio

Open `PORTFOLIO_TEMPLATES.md` and pick a template that matches your:
- **Age:** Younger = more aggressive
- **Risk tolerance:** Conservative, Balanced, or Aggressive
- **Goals:** Growth, Income, or Preservation

**Popular choices:**
- **Age 20-35:** Aggressive Template
- **Age 35-50:** Balanced Template
- **Age 50+:** Conservative Template

---

### 3. Customize the Script

Open `my_portfolio_optimizer.py` in any text editor:

**Find line 21** and replace the ticker list with your chosen template.

**Example:**
```python
# BEFORE (default)
tickers = [
    'SPY',
    'QQQ',
    'XLP',
    # ...
]

# AFTER (your choice - e.g., Balanced)
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
```

---

### 4. Run It!

```bash
# Make sure environment is activated
conda activate pcrm-book

# Run the optimizer
python my_portfolio_optimizer.py
```

**Wait 10-30 seconds** while it downloads data and runs optimization.

---

### 5. Review Results

You'll see output like this:

```
======================================================================
RECOMMENDED ALLOCATIONS
======================================================================

Portfolio Weights (%):
           CVaR Optimized  Mean-Variance  Equal Weight
SPY                 18.45          25.30         14.29
QQQ                 12.25          18.75         14.29
XLP                 22.50          15.20         14.29
...

For a $10,000 portfolio, buy:
  SPY    18.45%  →  $ 1,845.00
  QQQ    12.25%  →  $ 1,225.00
  XLP    22.50%  →  $ 2,250.00
  ...
```

**Two charts will be saved:**
- `my_portfolio_results.png` - Allocation comparison
- `my_risk_return_chart.png` - Risk/return visualization

---

### 6. Execute in Fidelity

**Log into Fidelity.com:**

1. Navigate to **"Trade"** → **"Stocks & ETFs"**
2. For each ticker in the "CVaR Optimized" column:
   - Search for the ticker (e.g., "SPY")
   - Select **"Buy"**
   - Enter **dollar amount** from the output
   - Review and submit
3. Repeat for all tickers

**Fidelity Pro Tips:**
- ✅ Commission-free for all ETFs listed
- ✅ Can buy fractional shares (exact dollar amounts)
- ✅ Set orders to execute at market open
- ✅ Use "trade ticket" to queue multiple orders

---

## 📅 Ongoing Maintenance

### Quarterly Rebalancing

**Set a calendar reminder** for every 3 months:

```bash
# March 1, June 1, September 1, December 1
conda activate pcrm-book
python my_portfolio_optimizer.py
```

**Compare new allocations to current holdings:**
- If difference > 5% → Rebalance
- If difference < 5% → Hold (save on taxes)

---

## 🔧 Customization Options

### Change Portfolio Size

Edit line ~150 in the script:

```python
# BEFORE
portfolio_value = 10000

# AFTER (for your actual portfolio)
portfolio_value = 50000  # Your amount
```

### Change Rebalancing Frequency

Edit line 36:

```python
# Monthly rebalancing
return_period = 21

# Quarterly (recommended)
return_period = 63

# Annual
return_period = 252
```

### Adjust Risk Tolerance

Edit line 39:

```python
# Very conservative (minimize worst 5%)
cvar_alpha = 0.95

# Moderate (minimize worst 10%)
cvar_alpha = 0.90

# Aggressive (minimize worst 15%)
cvar_alpha = 0.85
```

---

## ❓ Troubleshooting

### "ModuleNotFoundError: No module named 'numpy'"

**Solution:** Activate the conda environment first

```bash
conda activate pcrm-book
python my_portfolio_optimizer.py
```

---

### "No data found for ticker XYZ"

**Solution:** The ticker might be:
- Misspelled → Check Yahoo Finance
- Delisted → Replace with similar ETF
- New → Needs more history → Remove or use shorter `years_of_history`

---

### "Optimization failed" or weird allocations

**Causes:**
- Not enough historical data → Reduce `years_of_history`
- Too many tickers → Reduce to 5-8 tickers
- Highly correlated assets → Pick more diverse ETFs

---

### Charts don't display

**Solution 1:** Charts are saved to files:
```bash
open my_portfolio_results.png
open my_risk_return_chart.png
```

**Solution 2:** Remove `plt.show()` if running headless

---

## 📊 Understanding the Output

### Mean Return
- **Higher = Better**, but consider risk
- 2-3% (quarterly) = ~8-12% annualized

### Volatility
- **Lower = Better** (less swing)
- <7% (quarterly) = stable
- >12% (quarterly) = volatile

### CVaR (Conditional Value at Risk)
- **Lower = Better** (smaller crashes)
- Most important metric for downside protection
- Shows average loss in worst-case scenarios

### Sharpe Ratio
- **Higher = Better** (return per unit of risk)
- >0.5 = good
- >1.0 = excellent

---

## 🎯 Real Example Walkthrough

**Sarah, Age 35, Moderate Risk Tolerance:**

1. **Chooses:** Balanced template
2. **Runs:** `python my_portfolio_optimizer.py`
3. **Gets allocation:**
   - SPY: 22%
   - QQQ: 15%
   - VEA: 18%
   - XLP: 20%
   - BND: 15%
   - GLD: 10%

4. **With $25,000 portfolio:**
   - SPY: $5,500
   - QQQ: $3,750
   - VEA: $4,500
   - XLP: $5,000
   - BND: $3,750
   - GLD: $2,500

5. **Executes in Fidelity** (10 minutes)
6. **Sets reminder** for June 1st to rebalance
7. **Expected outcome:**
   - Annual return: 7-9%
   - Max drawdown: ~15% (vs 25% for 100% stocks)
   - Sleep better at night ✅

---

## 🏆 Success Metrics

After 1 year, you should be able to say:

✅ "I understand what I own and why"
✅ "I'm comfortable with the risk level"
✅ "I rebalance systematically, not emotionally"
✅ "I'm not panic-selling during corrections"
✅ "My portfolio matches my age and goals"

---

## 📚 Next Steps

**Beginner:**
- Stick to one template
- Rebalance quarterly
- Don't overthink it

**Intermediate:**
- Mix templates
- Experiment with parameters
- Backtest over 10+ years

**Advanced:**
- Read the original PCRM book chapters
- Implement Entropy Pooling views
- Explore derivatives strategies (Chapter 6)

---

## 🔗 Resources

- **Fidelity Account:** https://www.fidelity.com
- **PCRM Book PDF:** https://antonvorobets.substack.com/p/pcrm-book
- **fortitudo.tech Docs:** https://github.com/fortitudo-tech/fortitudo.tech
- **Yahoo Finance (ticker lookup):** https://finance.yahoo.com

---

**You're ready to build a professional portfolio! 🚀**

Questions? Check `EXAMPLE_OUTPUT.md` to see what results look like.
