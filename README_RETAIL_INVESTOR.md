# 📁 Retail Investor Portfolio Toolkit

## What I've Created For You

I've built a **complete portfolio optimization system** that you can run on your own computer. Here's what you have:

---

## 📄 Your Files

### ✨ **my_portfolio_optimizer.py** (Main Script)
**What it does:**
- Downloads historical data for your chosen ETFs
- Calculates risk metrics (volatility, CVaR, skewness)
- Optimizes portfolio weights using two methods:
  - **CVaR optimization** (minimizes tail risk)
  - **Mean-Variance** (traditional approach)
- Generates allocation recommendations
- Creates visualizations
- Tells you EXACTLY how much of each ETF to buy

**How to use:**
1. Edit the ticker list (line 21-29)
2. Run: `python my_portfolio_optimizer.py`
3. Review the output
4. Execute trades in Fidelity

---

### 📋 **PORTFOLIO_TEMPLATES.md** (Ready-to-Use Portfolios)
**What's inside:**
- 8 pre-built portfolio templates
- Conservative (low risk)
- Balanced (moderate risk)
- Aggressive (high growth)
- Global diversification
- Dividend income
- Sector rotation
- All-weather
- Crypto-enhanced

**How to use:**
1. Find the template that matches your age/goals
2. Copy the ticker list
3. Paste into `my_portfolio_optimizer.py`
4. Run the script

---

### 🚀 **QUICK_START.md** (Step-by-Step Guide)
**What's inside:**
- 5-minute setup instructions
- How to install the environment
- How to run the optimizer
- How to execute in Fidelity
- Troubleshooting tips
- Real example walkthrough

**Start here if you're new!**

---

### 📊 **EXAMPLE_OUTPUT.md** (See What to Expect)
**What's inside:**
- Full example of script output
- Shows what the allocation tables look like
- Explains the metrics
- Shows how to interpret results

**Read this to know what you'll see**

---

## 🎯 Quick Start (3 Steps)

### Step 1: Setup (One-time, 5 minutes)
```bash
cd pcrm-book
conda env create -f environment.yml
conda activate pcrm-book
```

### Step 2: Customize (2 minutes)
- Open `PORTFOLIO_TEMPLATES.md`
- Pick a template (e.g., "Balanced")
- Copy tickers into `my_portfolio_optimizer.py` line 21

### Step 3: Run (30 seconds)
```bash
python my_portfolio_optimizer.py
```

**Done!** You'll get allocation recommendations.

---

## 💰 What Happens Next

### The Script Outputs:

1. **Individual Asset Stats**
   ```
              Mean  Volatility  90%-CVaR
   SPY       2.85        8.45     16.42
   QQQ       3.52       11.23     21.15
   ...
   ```

2. **Recommended Allocations**
   ```
              CVaR Optimized
   SPY                 18.45%
   QQQ                 12.25%
   XLP                 22.50%
   ...
   ```

3. **Dollar Amounts** (for your portfolio size)
   ```
   For a $10,000 portfolio, buy:
     SPY  18.45%  →  $1,845.00
     QQQ  12.25%  →  $1,225.00
     ...
   ```

4. **Two Charts** (saved as PNG files)
   - Allocation comparison bar chart
   - Risk-return scatter plot

---

## 🏦 Executing in Fidelity

### Log into Fidelity.com

**For each ticker in your allocation:**

1. Click **"Trade"** → **"Stocks & ETFs"**
2. Search for ticker (e.g., "SPY")
3. Select **"Buy"**
4. Enter the **dollar amount** from script output
5. Select **"Shares"** → change to **"Dollars"** if needed
6. Review → **Submit**

**Fidelity features:**
- ✅ Zero commissions on all ETFs
- ✅ Fractional shares available
- ✅ Can buy exact dollar amounts
- ✅ Instant execution during market hours

---

## 🔄 Maintenance Schedule

| When | What to Do | Time |
|------|-----------|------|
| **Today** | Initial setup & first purchase | 30 min |
| **Quarterly** | Re-run optimizer & rebalance | 15 min |
| **Annually** | Review strategy & goals | 1 hour |

**Quarterly dates:** March 1, June 1, September 1, December 1

---

## 📈 Real-World Example

**Meet Alex, 32 years old, software engineer:**

**Starting point:**
- $20,000 in savings account (0.5% interest)
- No investment experience
- Moderate risk tolerance
- 30+ year time horizon

**What Alex did:**
1. Chose **"Balanced Template"** from templates
2. Ran the optimizer
3. Got allocation:
   - SPY (20%), QQQ (15%), VEA (15%), VWO (10%)
   - XLP (15%), XLV (10%), BND (10%), GLD (5%)
4. Executed in Fidelity (took 15 minutes)

**After 1 year:**
- Portfolio value: $22,400 (12% return)
- Max drawdown: 8% (stayed calm during dip)
- Rebalanced 4 times (15 min each)
- Feels confident and in control

**Alex's key insight:**
> "The best part isn't the returns—it's that I finally understand
> WHAT I own and WHY. I'm not guessing anymore."

---

## 🎓 Learning Path

### Week 1: Get Started
- ✅ Install environment
- ✅ Run optimizer with a template
- ✅ Understand the output
- ✅ Execute first trades

### Month 1: Understand
- ✅ Read `EXAMPLE_OUTPUT.md`
- ✅ Try different templates
- ✅ Compare CVaR vs Mean-Variance results
- ✅ Learn what the metrics mean

### Quarter 1: Master
- ✅ First rebalancing
- ✅ Customize your own ticker list
- ✅ Experiment with parameters
- ✅ Read PCRM book chapters 2-3

### Year 1: Optimize
- ✅ Track actual performance
- ✅ Refine strategy based on results
- ✅ Consider advanced topics (Chapter 5-6)
- ✅ Help others get started!

---

## ⚠️ Important Notes

### This is NOT:
❌ A get-rich-quick scheme
❌ Day trading or stock picking
❌ Market timing
❌ Gambling

### This IS:
✅ **Systematic** portfolio management
✅ **Data-driven** decision making
✅ **Risk-aware** optimization
✅ **Long-term** wealth building

---

## 🆘 Common Questions

### "Which template should I choose?"
**Rule of thumb:**
- Age 20-35 → Aggressive
- Age 35-50 → Balanced
- Age 50-65 → Conservative
- Age 65+ → Conservative or Dividend Income

### "How often should I rebalance?"
**Recommended:** Quarterly

**Why?**
- Monthly = too frequent (taxes, fees)
- Annual = too infrequent (drift)
- Quarterly = sweet spot

### "What if I only have $1,000?"
**No problem!**
- Fidelity allows fractional shares
- Start with fewer ETFs (pick top 5 from allocation)
- Add more as you save

### "Should I use CVaR or Mean-Variance weights?"
**Use CVaR if:**
- You care more about avoiding big losses
- You sleep better with lower risk
- You're within 10 years of retirement

**Use Mean-Variance if:**
- You want higher expected returns
- You can stomach volatility
- You're young with long time horizon

**Most people → Use CVaR**

---

## 📚 Next Steps After Mastery

### Level 2 (Intermediate):
- Read PCRM Chapter 3: Simulations
- Read PCRM Chapter 4: Dynamic Strategies
- Implement views with Entropy Pooling (Chapter 5)

### Level 3 (Advanced):
- Options strategies (Chapter 6)
- Build multi-asset portfolios
- Stress testing
- Custom Python portfolio tools

### Level 4 (Expert):
- Contribute to fortitudo.tech
- Research papers
- Professional portfolio management

---

## 🎯 Your Immediate Action Plan

**Tonight (15 minutes):**
1. Read `QUICK_START.md`
2. Read `PORTFOLIO_TEMPLATES.md`
3. Pick your template

**This Weekend (1 hour):**
1. Install conda environment
2. Run `my_portfolio_optimizer.py`
3. Review results
4. Open Fidelity account (if needed)

**Next Week:**
1. Execute trades in Fidelity
2. Set quarterly calendar reminder
3. Sleep better knowing you have a plan!

---

## 📞 Resources

**Technical Help:**
- PCRM Book: https://antonvorobets.substack.com/p/pcrm-book
- fortitudo.tech: https://github.com/fortitudo-tech/fortitudo.tech

**Brokerage:**
- Open Fidelity account: https://www.fidelity.com
- Fidelity research: https://research.fidelity.com

**Market Data:**
- Yahoo Finance: https://finance.yahoo.com
- ETF Database: https://etfdb.com

---

## 🏆 Success Criteria

After 1 year, you should be able to say **YES** to:

- [ ] I run the optimizer quarterly
- [ ] I understand my allocation
- [ ] I'm comfortable with my risk level
- [ ] I don't panic sell during downturns
- [ ] I've stuck to my rebalancing schedule
- [ ] My portfolio matches my goals
- [ ] I can explain my strategy to others

If YES to all → You're a quantitative investor! 🎉

---

## 💬 Final Thoughts

**You don't need:**
- A finance degree
- Expensive advisors (1% annual fee = $10k on $1M!)
- Complex trading strategies
- Perfect market timing

**You DO need:**
- This toolkit (✓ you have it)
- 30 minutes quarterly
- Discipline to stick to the plan
- Patience for compound growth

**The difference between you and professional portfolio managers:**
They have Bloomberg terminals and PhDs. You have this Python script.

**Guess what? The math is the SAME.**

---

**Ready to start? Open `QUICK_START.md` and follow Step 1!**

Good luck! 🚀📈
