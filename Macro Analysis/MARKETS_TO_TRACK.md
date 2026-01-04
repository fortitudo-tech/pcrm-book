# Markets to Track: Macro-Valuation Framework Guide

## Quick Reference: Where Are We & Where Are We Going?

This guide helps you track markets based on the macro-valuation quadrant framework that maps **Capital Flows** and **Monetary Policy** into market positioning.

---

## The Framework

### Two Key Dimensions:

1. **X-Axis (Horizontal): US Dollar Exchange Rate**
   - Left = Falling Dollar (Weak)
   - Right = Rising Dollar (Strong)

2. **Y-Axis (Vertical): Yield Curve Shape**
   - Down = Flattening Curve
   - Up = Steepening Curve

### Four Quadrants:

```
                    Steepening Curve ↑
                           |
    Dovish/Co-op (3)       |      Happiness Zone (2)
    Falling $ +            |      Rising $ +
    Steep Curve            |      Steep Curve
                           |
    ←──────────────────────┼──────────────────────→
    Falling $              |              Rising $
                           |
    Crisis Zone (4)        |      Hawkish Policy (1)
    Falling $ +            |      Rising $ +
    Flat Curve             |      Flat Curve
                           |
                    Flattening Curve ↓
```

**Historical Examples:**
- **Happiness Zone**: 1984, 2000, 2015, 2020
- **Crisis Zone**: 1980, 1990, 2010
- **2026 Forecast**: Movement toward Hawkish Policy (Bottom Right)

---

## Essential Markets to Track (Start Here)

### 1. US Dollar Index (DXY)
- **What**: Trade-weighted US dollar index
- **Where**: Bloomberg `DXY Index`, Yahoo Finance `DX-Y.NYB`, Investing.com
- **Frequency**: Real-time / Daily close
- **2026 Forecast**: +5% appreciation expected
- **Current Level**: Check daily
- **Why**: X-axis positioning in quadrant framework

### 2. Yield Curve Spread (10Y-2Y)
- **What**: 10-Year Treasury yield minus 2-Year Treasury yield
- **Where**: FRED `T10Y2Y`, Bloomberg `USYC2Y10 Index`
- **Frequency**: Daily
- **Normal Range**: +50 to +200 bps (positive = healthy)
- **Inverted**: < 0 bps (recession warning)
- **Why**: Y-axis positioning in quadrant framework

### 3. Bank Excess Reserves
- **What**: Reserves held by banks at the Fed above requirements
- **Where**: FRED series `EXCSRESNW`
- **Frequency**: Weekly (Wednesday)
- **Critical Level**: Watch for decline below $3 trillion
- **Why**: Core liquidity measure; low reserves = funding stress

### 4. VIX (Volatility Index)
- **What**: S&P 500 implied volatility (fear gauge)
- **Where**: CBOE, Yahoo Finance `^VIX`
- **Frequency**: Real-time
- **Normal**: 12-20
- **Elevated**: 20-30
- **Crisis**: > 30
- **Why**: Market stress indicator

---

## Recommended Tracking (Comprehensive View)

### 5. Federal Reserve Balance Sheet
- **What**: Total assets held by the Fed
- **Where**: FRED series `WALCL`, Fed H.4.1 Report
- **Frequency**: Weekly (Thursday release)
- **Trend**: Watch for QT (declining) vs QE (rising)
- **Why**: Monetary policy stance (loose vs tight)

### 6. Reverse Repo Program (RRP)
- **What**: Overnight reverse repo operations
- **Where**: FRED series `RRPONTSYD`, NY Fed website
- **Frequency**: Daily
- **High Usage**: > $2 trillion = excess liquidity
- **Low Usage**: < $500 billion = liquidity getting absorbed
- **Why**: Measures excess liquidity in system

### 7. Credit Spreads
- **Investment Grade (IG)**: FRED series `BAMLC0A4CBBB`
- **High Yield (HY)**: FRED series `BAMLH0A0HYM2`
- **Frequency**: Daily
- **Normal IG**: 100-150 bps
- **Stress IG**: > 200 bps
- **Why**: Risk pricing and credit market health

### 8. SOFR (Secured Overnight Financing Rate)
- **What**: Key overnight lending rate
- **Where**: NY Fed, Bloomberg `SOFR Index`
- **Frequency**: Daily
- **Watch**: Spikes above Fed Funds Rate = funding stress
- **Why**: Real-time funding market conditions

### 9. TIC Data (Treasury International Capital)
- **What**: Foreign purchases/sales of US securities
- **Where**: Treasury.gov TIC System
- **Frequency**: Monthly (6-week lag)
- **What to Watch**: Net foreign inflows (positive = capital flowing in)
- **Why**: Tracks capital flows directly

### 10. Fed Funds Effective Rate
- **What**: Actual overnight interbank lending rate
- **Where**: FRED series `FEDFUNDS`
- **Frequency**: Daily
- **Why**: Current monetary policy rate

---

## Advanced Tracking (Professional Level)

### 11. Treasury General Account (TGA)
- **FRED**: `WTREGEN`
- **Why**: When Treasury spends (TGA ↓), liquidity enters system

### 12. Net Liquidity
- **Formula**: Fed Balance Sheet - RRP - TGA
- **Why**: True measure of liquidity available to markets
- **Build it**: Combine series from above

### 13. MOVE Index
- **What**: Bond market volatility index
- **Where**: Bloomberg `MOVE Index`
- **Normal**: 50-80
- **Stress**: > 100
- **Why**: Fixed income stress gauge

### 14. Foreign Holdings of US Treasuries
- **Where**: Treasury.gov Major Foreign Holders report
- **Frequency**: Monthly
- **Top Holders**: Japan, China
- **Why**: Shows structural demand for USD assets

### 15. Cross-Currency Basis Swaps
- **What**: Cost to swap currencies (e.g., EUR/USD basis)
- **Where**: Bloomberg `EURUSD3M Curncy`
- **Normal**: Near zero
- **Stress**: Wide negative = dollar shortage
- **Why**: Offshore dollar funding stress

### 16. Central Bank Swap Lines
- **What**: Fed lending to foreign central banks
- **Where**: Fed H.4.1 Report
- **Normal**: Near zero usage
- **Crisis**: Billions in usage
- **Why**: Extreme offshore dollar stress indicator

### 17. Bond Market Trade Fails
- **What**: Failed Treasury settlement transactions
- **Where**: Fed/DTCC data
- **Normal**: Low fails
- **Stress**: Rising fails = liquidity problems
- **Why**: Direct measure of market dysfunction

---

## Daily Monitoring Checklist

### Morning Routine (5 minutes):
- [ ] Check DXY level and overnight change
- [ ] Check 10Y-2Y spread
- [ ] Check VIX level
- [ ] Check SOFR rate
- [ ] Scan financial headlines for Fed/liquidity news

### Weekly Routine (15 minutes):
- [ ] Wednesday: Bank excess reserves (FRED)
- [ ] Thursday: Fed balance sheet (H.4.1)
- [ ] Check RRP usage trend
- [ ] Review credit spreads (IG/HY)
- [ ] Update quadrant position in notebook

### Monthly Routine (30 minutes):
- [ ] Review TIC flows data
- [ ] Check foreign Treasury holdings
- [ ] Update all FRED series
- [ ] Run full notebook analysis
- [ ] Assess quadrant movement vs forecast

---

## Data Sources & Tools

### Free Sources:
1. **FRED** (Federal Reserve Economic Data)
   - URL: https://fred.stlouisfed.org/
   - API: Free with registration
   - Best for: US macro data, Fed data

2. **Yahoo Finance**
   - URL: https://finance.yahoo.com/
   - API: `yfinance` Python library
   - Best for: Market prices (DXY, VIX, yields)

3. **Treasury.gov**
   - TIC Data: https://home.treasury.gov/data/treasury-international-capital-tic-system
   - Best for: Capital flows

4. **NY Fed**
   - URL: https://www.newyorkfed.org/markets
   - Best for: Repo operations, SOFR

5. **CBOE**
   - URL: https://www.cboe.com/
   - Best for: VIX data

### Premium Sources (if available):
- **Bloomberg Terminal**: Real-time everything
- **Refinitiv/Eikon**: Comprehensive data
- **FactSet**: Analytics platform

---

## Interpreting Your Position

### Current Quadrant Implications:

#### Quadrant 1: Hawkish Policy (Bottom Right)
**Position**: Rising $ + Flatter Curve
**Drivers**: Tight monetary policy, liquidity drain
**Implications**:
- Fed tightening or not easing enough
- Liquidity conditions deteriorating
- **RMP interventions likely here** ← We are focused here for 2026
- Risk assets under pressure
- Dollar strength hurts EM currencies
**Action**: Monitor liquidity metrics closely, watch for Fed action

#### Quadrant 2: Happiness Zone (Top Right)
**Position**: Rising $ + Steeper Curve
**Drivers**: Strong capital inflows
**Implications**:
- Global capital flowing to US
- Positive for risk assets
- Strong economic backdrop
- Yield curve normalizing
**Action**: Favorable environment, stay invested

#### Quadrant 3: Dovish/Co-operative (Top Left)
**Position**: Falling $ + Steeper Curve
**Drivers**: Loose monetary policy
**Implications**:
- Fed easing aggressively
- Reflationary environment
- EM currencies benefiting
- Commodity prices supported
**Action**: Consider inflation hedges

#### Quadrant 4: Crisis Zone (Bottom Left)
**Position**: Falling $ + Flatter Curve
**Drivers**: Capital flight
**Implications**:
- Major stress/crisis
- Flight to quality
- Fed may need emergency measures
- High volatility
**Action**: Risk-off positioning, watch for policy response

---

## 2026 Forecast from Article

### Expected Path:
- **Movement**: Toward Bottom Right (Hawkish Policy quadrant)
- **DXY**: +5% appreciation (current ~106 → ~111)
- **Yield Curve**: Flattening expected
- **Drivers**:
  - Tightening liquidity conditions
  - Fed policy divergence (US tighter than expected)
  - Safe-haven flows despite domestic origin of stress
  - RMP program only a "sticking plaster" (temporary fix)

### Key Watchpoints:
1. **Liquidity deterioration**: Declining bank reserves
2. **Rising bond fails**: Market stress
3. **Credit spread widening**: Risk repricing
4. **Dollar strength**: Especially vs JPY and CNY
5. **Flattening curve**: Despite RMP support

### Invalidation Signals:
If you see these, forecast may be wrong:
- Massive Fed balance sheet expansion (real QE)
- Large capital outflows from US (TIC data negative)
- DXY breaking below 100
- 10Y-2Y steepening beyond +100 bps

---

## Quick Start Guide

### Step 1: Set Up Data Access (One-time)
1. Get FRED API key (free): https://fred.stlouisfed.org/docs/api/api_key.html
2. Install Python packages: `yfinance`, `fredapi`, `pandas`, `matplotlib`
3. Open the notebook: `rmp_liquidity_tracker.ipynb`

### Step 2: Run Initial Analysis (First time)
1. Update FRED_API_KEY in notebook
2. Run all cells to fetch data
3. Generate quadrant spider diagram
4. Note current position

### Step 3: Monitor Weekly (Ongoing)
1. Re-run data fetching cells
2. Check for quadrant changes
3. Review liquidity dashboard
4. Compare to 2026 forecast path

### Step 4: Deep Dive Monthly (Optional)
1. Update TIC data manually
2. Review all indicators
3. Write notes on major changes
4. Adjust portfolio positioning if needed

---

## Key Formulas

### Net Liquidity
```
Net Liquidity = Fed Balance Sheet - Reverse Repo - TGA
```

### Yield Curve Slope
```
10Y-2Y Spread = 10-Year Yield - 2-Year Yield
```

### Z-Score for Quadrant Positioning
```
Z-Score = (Current Value - Rolling Mean) / Rolling Std Dev
```

### DXY Projection (Article forecast)
```
Target DXY = Current DXY × 1.05  (for 2026)
```

---

## Contacts & Resources

### Official Data Sources:
- **Federal Reserve**: https://www.federalreserve.gov/
- **US Treasury**: https://home.treasury.gov/
- **NY Fed Markets**: https://www.newyorkfed.org/markets

### Educational Resources:
- **FRED Blog**: https://fredblog.stlouisfed.org/
- **NY Fed Liberty Street Economics**: https://libertystreeteconomics.newyorkfed.org/
- **BIS Papers**: https://www.bis.org/

### Market Commentary:
- Monitor financial news for Fed speakers
- Follow Treasury auction results
- Watch for liquidity stress headlines

---

## Troubleshooting

### "Where do I start?"
→ Start with the 4 essential indicators: DXY, 10Y-2Y, Bank Reserves, VIX

### "FRED API not working?"
→ Check your API key, ensure you're not hitting rate limits (120 calls/min)

### "Data is outdated?"
→ TIC data has 6-week lag, that's normal. Use other indicators for real-time

### "Quadrant keeps changing?"
→ Use longer lookback periods (252 days), add smoothing

### "Don't understand a metric?"
→ Start with the notebook comments, then check FRED series description

---

## Summary: Minimum Viable Tracking

If you only track **4 things**, track these:

1. **DXY** → Where is the dollar? (X-axis)
2. **10Y-2Y** → What's the curve doing? (Y-axis)
3. **Bank Reserves** → Is liquidity healthy?
4. **VIX** → Is there stress?

These four tell you 80% of what you need to know about your quadrant position and market conditions.

---

**Document Version**: 1.0
**Last Updated**: 2026-01-03
**Related Notebook**: `rmp_liquidity_tracker.ipynb`
