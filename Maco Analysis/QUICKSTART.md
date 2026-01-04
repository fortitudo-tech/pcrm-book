# Quick Start Guide - RMP Liquidity Tracker

## 🚀 Get Started in 3 Steps

### Step 1: See It Working (30 seconds)

Run the demo with mock data to see all features:

```bash
cd code/macro_analysis
python demo_tracker.py
```

This generates:
- ✓ Spider diagram showing quadrant movements
- ✓ Liquidity dashboard with 6 key charts
- ✓ Summary statistics and trends

**Output files**: `demo_spider_diagram.png` and `demo_dashboard.png`

---

### Step 2: Understand the Framework (5 minutes)

Read the guide:
```bash
cat MARKETS_TO_TRACK.md
```

Or jump to the essentials:

**Four Quadrants:**
```
                   Steepening ↑
                       |
    Dovish (3)         |      Happiness (2)
    Falling $ +        |      Rising $ +
    Steep Curve        |      Steep Curve
                       |
  ←──────────────────────────────────────→
    Falling $          |          Rising $
                       |
    Crisis (4)         |      Hawkish (1)
    Falling $ +        |      Rising $ +
    Flat Curve         |      Flat Curve
                       |
                   Flattening ↓
```

**What to Track (Minimum):**
1. **DXY** - US Dollar Index (X-axis)
2. **10Y-2Y Spread** - Yield curve (Y-axis)
3. **Bank Reserves** - Liquidity health
4. **VIX** - Stress gauge

---

### Step 3: Use Real Data (15 minutes setup)

#### A. Get FREE FRED API Key

1. Go to: https://fred.stlouisfed.org/
2. Create free account (30 seconds)
3. Request API key: https://fred.stlouisfed.org/docs/api/api_key.html
4. Copy your key (looks like: `a1b2c3d4e5f6...`)

#### B. Update the Notebook

1. Open: `rmp_liquidity_tracker.ipynb` in Jupyter
2. Find this cell:
   ```python
   FRED_API_KEY = 'YOUR_FRED_API_KEY_HERE'
   ```
3. Replace with your actual key:
   ```python
   FRED_API_KEY = 'a1b2c3d4e5f6...'
   ```

#### C. Run All Cells

- In Jupyter: **Cell → Run All**
- Or run cell by cell to see each step

**You'll get:**
- ✓ Real market data (2020-present)
- ✓ Current quadrant position
- ✓ Spider diagram with actual path
- ✓ Full liquidity dashboard
- ✓ Momentum indicators

---

## 📊 Daily Monitoring Routine (5 minutes)

### Quick Check (Every Morning):

1. **Check DXY**
   - Yahoo Finance: search "DXY"
   - Or: https://www.investing.com/indices/usdollar

2. **Check 10Y-2Y Spread**
   - FRED: https://fred.stlouisfed.org/series/T10Y2Y
   - Positive = Normal, Negative = Inverted

3. **Check VIX**
   - Yahoo Finance: search "^VIX"
   - <20 = Normal, >30 = Stress

4. **Quick Assessment**:
   - Is dollar rising or falling? (X-axis)
   - Is curve steepening or flattening? (Y-axis)
   - Which quadrant are we in?

### Weekly Update (15 minutes):

Run the notebook cells to update all charts with latest data.

---

## 🎯 Current Focus: 2026 Forecast

### The Prediction:
- **Movement**: Toward "Hawkish Policy" quadrant (Bottom Right)
- **DXY**: +5% appreciation expected
- **Yield Curve**: Flattening bias
- **Driver**: Liquidity tightening despite RMP interventions

### What to Watch:

| Indicator | Normal | Warning | Critical |
|-----------|--------|---------|----------|
| **Bank Reserves** | >$3T | $2.5-3T | <$2.5T |
| **VIX** | 12-20 | 20-30 | >30 |
| **10Y-2Y** | +50 to +200 bps | -50 to 0 | <-50 bps |
| **Credit Spreads** | <150 bps | 150-200 | >200 bps |

### Key Thesis:
RMP (Reserve Management Purchases) is a "sticking plaster" - temporary fix for deeper liquidity problems. Watch for:
1. ✓ Declining bank reserves (happening)
2. ✓ Rising bond market fails (stress signal)
3. ✓ Dollar strength despite domestic issues (safe haven)
4. ✓ Flatter curves (despite Fed interventions)

---

## 🔧 Troubleshooting

### "Can't fetch data"
→ Check internet connection
→ Verify FRED API key is correct
→ Check API rate limits (120 calls/min)

### "Module not found"
→ Install packages:
```bash
pip install pandas numpy matplotlib fredapi pandas-datareader
```

### "FRED API key invalid"
→ Get new key at fred.stlouisfed.org
→ Make sure no quotes around the key in code

### "Charts not showing"
→ Use `matplotlib.use('Agg')` for non-interactive
→ Or use Jupyter for interactive plots

---

## 📚 Learning Path

### Beginner (Week 1):
1. ✓ Run demo script
2. ✓ Read MARKETS_TO_TRACK.md (focus on "Essential" section)
3. ✓ Track DXY, 10Y-2Y, VIX daily
4. ✓ Identify current quadrant

### Intermediate (Week 2-3):
1. ✓ Get FRED API key
2. ✓ Run full notebook with real data
3. ✓ Add weekly monitoring routine
4. ✓ Track bank reserves, Fed balance sheet

### Advanced (Month 2+):
1. ✓ Add TIC data (capital flows)
2. ✓ Monitor cross-currency basis swaps
3. ✓ Build custom alerts for thresholds
4. ✓ Develop scenario projections

---

## 📂 File Guide

| File | Purpose | When to Use |
|------|---------|-------------|
| `README.md` | Overview & context | First read |
| `QUICKSTART.md` | This file! | Getting started |
| `MARKETS_TO_TRACK.md` | Comprehensive reference | Daily reference |
| `rmp_liquidity_tracker.ipynb` | Main notebook | Weekly analysis |
| `demo_tracker.py` | Demo with mock data | Test/learn |
| `test_tracker_simple.py` | Test installation | Troubleshooting |

---

## 💡 Pro Tips

1. **Save Time**: Bookmark these URLs
   - FRED: https://fred.stlouisfed.org/
   - DXY Chart: https://www.tradingview.com/symbols/TVC-DXY/
   - VIX: https://www.cboe.com/tradable_products/vix/

2. **Set Alerts**: Create Google Calendar reminders
   - Wednesday: Check bank reserves (FRED release)
   - Thursday: Check Fed balance sheet (H.4.1)
   - Monthly: Update full notebook

3. **Quick Quadrant Check**:
   - DXY up + Curve flattening = Hawkish Policy ← **2026 forecast**
   - DXY up + Curve steepening = Happiness Zone
   - DXY down + Curve flattening = Crisis Zone
   - DXY down + Curve steepening = Dovish/Co-op

4. **Context Matters**: Don't look at indicators in isolation
   - Rising DXY + Rising VIX = Flight to safety
   - Rising DXY + Falling VIX = Economic strength
   - Always check multiple indicators

---

## 🎓 Key Concepts

### Net Liquidity Formula:
```
Net Liquidity = Fed Balance Sheet - Reverse Repo - TGA
```

### Quadrant Logic:
```python
if DXY > average:
    x_axis = "RIGHT (Rising Dollar)"
else:
    x_axis = "LEFT (Falling Dollar)"

if curve_10y2y > average:
    y_axis = "UP (Steepening)"
else:
    y_axis = "DOWN (Flattening)"
```

### 2026 Forecast Direction:
```
Current → Hawkish Policy
- DXY rising (safe haven + Fed divergence)
- Curve flattening (tight conditions)
- Liquidity draining (reserves declining)
- RMP only temporary relief
```

---

## ❓ FAQ

**Q: Do I need to code?**
A: No! You can track manually using the checklists in MARKETS_TO_TRACK.md

**Q: How much does it cost?**
A: $0. All data sources are free (FRED, Yahoo Finance, etc.)

**Q: How often should I update?**
A: Daily quick check (5 min), Weekly full update (15 min)

**Q: What if I don't have Jupyter?**
A: Install with: `pip install jupyterlab` or use the Python scripts directly

**Q: Can I automate this?**
A: Yes! Use cron/scheduled tasks to run the scripts daily

---

## 📞 Next Steps

1. **Right Now**: Run `python demo_tracker.py`
2. **Today**: Get FRED API key
3. **This Week**: Set up weekly monitoring
4. **This Month**: Track movement toward 2026 forecast

---

## 🔗 Quick Links

- **FRED API**: https://fred.stlouisfed.org/docs/api/api_key.html
- **FRED Mobile App**: Download for on-the-go tracking
- **TradingView**: https://www.tradingview.com/ (free charts)
- **Fed H.4.1 Report**: https://www.federalreserve.gov/releases/h41/
- **NY Fed Markets**: https://www.newyorkfed.org/markets

---

**Ready?** Run this now:
```bash
python demo_tracker.py
```

Then check the generated PNG files! 🎉
