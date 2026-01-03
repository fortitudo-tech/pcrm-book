# Macro-Valuation & RMP Liquidity Tracking

This folder contains tools for tracking macro-valuation shifts and liquidity conditions, with a focus on the Federal Reserve's RMP (Reserve Management Purchases) liquidity program and its implications for 2026.

## Overview

The framework maps markets into a four-quadrant system based on:
- **Capital Flows** (strong inflows vs outflows)
- **Monetary Policy Stance** (loose vs tight)

These drive two observable market dimensions:
- **X-axis**: US Dollar exchange rate (DXY)
- **Y-axis**: Yield curve shape (10Y-2Y spread)

## Files in This Folder

### 1. `rmp_liquidity_tracker.ipynb`
**Main tracking notebook** with:
- Data fetching functions for market and FRED data
- Quadrant positioning calculations
- Spider diagram visualization (path through quadrants over time)
- Liquidity dashboard (bank reserves, Fed balance sheet, RRP, etc.)
- Forward-looking projections based on 2026 forecast

**Requirements**:
- FRED API key (free): https://fred.stlouisfed.org/docs/api/api_key.html
- Python packages: `yfinance`, `fredapi`, `pandas`, `matplotlib`, `seaborn`

### 2. `MARKETS_TO_TRACK.md`
**Comprehensive reference guide** covering:
- Essential markets to track (start here if new)
- Recommended indicators for comprehensive view
- Advanced metrics for professional analysis
- Daily/weekly/monthly monitoring checklists
- Data sources and where to find them
- Interpretation guide for each quadrant
- 2026 forecast details and watchpoints

## Quick Start

### For Beginners:
1. Read `MARKETS_TO_TRACK.md` → "Essential Markets to Track" section
2. Focus on 4 key indicators:
   - DXY (US Dollar Index)
   - 10Y-2Y spread (Yield Curve)
   - Bank Excess Reserves
   - VIX (Volatility)
3. Check these daily using free sources (Yahoo Finance, FRED)

### For Intermediate Users:
1. Get a FRED API key (free)
2. Open `rmp_liquidity_tracker.ipynb`
3. Update `FRED_API_KEY` in the config cell
4. Run all cells to generate current position analysis
5. Set up weekly monitoring routine

### For Advanced Users:
1. Extend the notebook with additional indicators (TIC data, cross-currency basis, etc.)
2. Build automated alerts for threshold breaches
3. Integrate with your own portfolio/risk systems
4. Develop scenario projections

## The Four Quadrants

```
                   Steepening Curve ↑
                          |
        Dovish/Co-op      |      Happiness Zone
        (Top Left)        |      (Top Right)
                          |
    ←─────────────────────┼─────────────────────→
      Falling Dollar      |      Rising Dollar
                          |
        Crisis Zone       |      Hawkish Policy
        (Bottom Left)     |      (Bottom Right)
                          |
                   Flattening Curve ↓
```

**Historical Context**:
- **Happiness Zone**: 1984, 2000, 2015, 2020
- **Crisis Zone**: 1980, 1990, 2010
- **2026 Forecast**: Movement toward **Hawkish Policy** (Bottom Right)

## 2026 Outlook Summary

Based on the macro-valuation framework analysis:

### Expected Movement:
- **Quadrant**: Toward Bottom Right (Hawkish Policy)
- **DXY**: +5% appreciation expected
- **Yield Curve**: Flattening bias
- **Key Driver**: Tightening liquidity conditions despite RMP interventions

### Critical Thesis:
The article argues that the Fed's RMP liquidity program is merely a "sticking plaster" - a temporary fix that masks deeper liquidity problems:

1. **Rolling Liquidity Downturn**: Global liquidity entering cyclical downswing in 2026
2. **Bank Reserve Depletion**: Excess reserves declining (watch for < $3T)
3. **Rising Bond Fails**: Settlement failures indicating market stress
4. **Policy Shift**: Transition from "Fed QE" to "Treasury QE" (real economy vs markets)
5. **Safe-Haven Flows**: Dollar strength from flight-to-quality, even if crisis is US-originated

### Implications:
- Pressure on risk assets
- Flatter yield curves (bad for banks)
- Dollar strength (stress on EM currencies, especially CNY and JPY)
- Continued need for Fed interventions (RMP, repo operations)
- Divergence: Strong real economy, weaker financial markets

### Invalidation Signals:
Watch for these to know if the forecast is wrong:
- Massive Fed QE (balance sheet re-expansion)
- Large capital outflows from US (negative TIC flows)
- DXY breaking below 100
- Yield curve steepening beyond +100 bps

## Data Sources

### Free Sources:
- **FRED**: https://fred.stlouisfed.org/ (US macro data)
- **Yahoo Finance**: Market prices via `yfinance`
- **Treasury.gov**: TIC data (capital flows)
- **NY Fed**: https://www.newyorkfed.org/markets (repo, SOFR)

### Premium (if available):
- Bloomberg Terminal
- Refinitiv/Eikon
- FactSet

## Monitoring Frequency

### Daily (5 min):
- DXY, 10Y-2Y spread, VIX, SOFR

### Weekly (15 min):
- Bank reserves (Wed), Fed balance sheet (Thu), RRP, credit spreads

### Monthly (30 min):
- TIC flows, foreign Treasury holdings, full notebook update

## Key Metrics by Category

### Liquidity (Critical for RMP Context):
- Bank Excess Reserves (FRED: `EXCSRESNW`)
- Fed Balance Sheet (FRED: `WALCL`)
- Reverse Repo (FRED: `RRPONTSYD`)
- Net Liquidity = Fed BS - RRP - TGA

### Positioning:
- DXY (X-axis)
- 10Y-2Y Spread (Y-axis)

### Stress:
- VIX (equity volatility)
- MOVE (bond volatility)
- Credit Spreads (IG: `BAMLC0A4CBBB`, HY: `BAMLH0A0HYM2`)
- SOFR spikes

### Policy:
- Fed Funds Rate (FRED: `FEDFUNDS`)
- Fed Balance Sheet changes (QT vs QE)
- Central bank swap lines (H.4.1)

### Capital Flows:
- TIC data (monthly, lagged)
- Foreign Treasury holdings
- Cross-currency basis swaps (advanced)

## Thresholds to Watch

| Metric | Normal | Caution | Crisis |
|--------|--------|---------|--------|
| Bank Reserves | > $3T | $2.5-3T | < $2.5T |
| VIX | 12-20 | 20-30 | > 30 |
| IG Spread | 100-150 bps | 150-200 bps | > 200 bps |
| 10Y-2Y | +50 to +200 | -50 to 0 | < -50 |
| RRP | Varies | Rapid changes | Near zero (all absorbed) |

## Contributing & Extending

Feel free to extend this framework:
- Add new indicators (commodities, crypto, etc.)
- Build ML models for quadrant prediction
- Create automated alert systems
- Integrate with portfolio optimization

## Related Resources

### Official Documentation:
- Federal Reserve: https://www.federalreserve.gov/
- Fed H.4.1 Report: https://www.federalreserve.gov/releases/h41/

### Educational:
- FRED Blog: https://fredblog.stlouisfed.org/
- NY Fed Liberty Street Economics: https://libertystreeteconomics.newyorkfed.org/
- BIS Research: https://www.bis.org/

### Market Data APIs:
- FRED API Docs: https://fred.stlouisfed.org/docs/api/
- yfinance: https://github.com/ranaroussi/yfinance

## License

This code is part of the Portfolio Construction and Risk Management book project and follows the same licensing:
- Book: CC BY-NC-ND 4.0
- Code: GPL v3

---

**Questions or Issues?**
- Check `MARKETS_TO_TRACK.md` for detailed explanations
- Review the notebook comments for technical details
- Consult FRED series descriptions for data definitions

**Last Updated**: 2026-01-03
