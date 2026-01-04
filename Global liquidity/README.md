# Global Liquidity Dashboard

## Overview

This branch contains a comprehensive **Global Liquidity Index (GLI)** analysis tool with an interactive web dashboard. It tracks and visualizes central bank balance sheets from major economies (Fed, ECB, Bank of Japan) to provide insights into global liquidity conditions and their relationship with financial markets.

## What It Does

The Global Liquidity Dashboard:

1. **Downloads and aggregates data** from multiple sources:
   - Federal Reserve, ECB, and Bank of Japan balance sheets (FRED)
   - Foreign exchange rates for currency conversion
   - VIX volatility index
   - Dollar strength index (DXY)
   - MSCI ACWI (global equities proxy)

2. **Calculates two proprietary liquidity indices**:
   - **GLI Flash**: Short-term momentum indicator (13-week changes) for tactical signals
   - **GLI Full**: Smoothed long-term indicator (20-week moving average) for macro regime analysis

3. **Generates comprehensive visualizations**:
   - 9 interactive charts (3 chart types × 3 time granularities)
   - Flash vs Full liquidity comparison
   - Year-over-year and 3-month annualized growth rates
   - Liquidity vs global equity market overlay

4. **Provides an interactive web dashboard**:
   - Real-time chart viewing with click-to-zoom functionality
   - One-click data refresh to update all charts
   - Responsive design for desktop and mobile
   - Hosted locally at `http://localhost:5000`

5. **Exports analysis to Excel** with:
   - Conditional formatting on key metrics
   - Trend signals (Rising/Falling/Flat)
   - Multiple worksheets with detailed data
   - Embedded charts for offline analysis

## Files in This Branch

### Core Analysis Scripts
- **`liquidity_website.py`**: Main data processing script that downloads data, calculates indices, and generates all charts
- **`global_liquidity.py`**: Alternative/backup version of the liquidity analysis script

### Web Dashboard
- **`app.py`**: Flask web server that hosts the interactive dashboard
- **`templates/index.html`**: HTML template with interactive UI and zoom functionality

### Generated Outputs (not committed to repo)
- `gli_plot_*.png`: 9 chart images in PNG format
- `global_liquidity_DIY_v2.xlsx`: Excel workbook with full analysis

## How to Use

### 1. Install Dependencies
```bash
pip install pandas pandas_datareader yfinance matplotlib openpyxl xlsxwriter flask
```

### 2. Run the Analysis (Generate Charts)
```bash
python liquidity_website.py
```

This will:
- Download the latest data from FRED and Yahoo Finance
- Calculate GLI Flash and GLI Full indices
- Generate 9 charts saved as PNG files
- Create an Excel file with detailed analysis

### 3. Start the Web Dashboard
```bash
python app.py
```

Then open your browser to `http://localhost:5000`

### 4. Using the Dashboard
- **View Charts**: Scroll through three sections of visualizations
- **Zoom In**: Click any chart to view it in full-screen mode
- **Close Zoom**: Press Escape, click the X, or click anywhere to exit zoom
- **Refresh Data**: Click the "🔄 Refresh Data" button to download fresh data and regenerate all charts

## Key Metrics Explained

### GLI Flash
- Momentum-based indicator using 13-week percentage changes
- Adjusted for volatility (VIX) and dollar strength (DXY)
- Best for short-term tactical positioning
- More volatile but responds quickly to changes

### GLI Full
- 20-week smoothed version of GLI Flash
- Shows macro liquidity regime (easing vs tightening)
- Better for strategic asset allocation
- More stable but slightly lagged

### Liquidity Growth Rates
- **Year-over-Year (YoY)**: Annual growth rate of total central bank assets
- **3-Month Annualized**: Recent trend extrapolated to annual rate
- Above 0% = Easing (liquidity expanding)
- Below 0% = Tightening (liquidity contracting)

## Why This Matters

Global liquidity is a powerful driver of asset prices. When central banks expand their balance sheets (QE), liquidity floods into the financial system, typically supporting higher asset prices. When they contract (QT), liquidity drains away, often preceding market corrections.

This tool helps investors:
- **Identify macro regime changes** (easing → tightening or vice versa)
- **Time tactical positions** using short-term momentum signals
- **Understand equity market drivers** through liquidity-stock correlation
- **Monitor real-time conditions** with regular data updates

## Technical Details

### Data Sources
- **FRED (Federal Reserve Economic Data)**: Central bank balance sheets, FX rates, VIX, DXY
- **Yahoo Finance**: MSCI ACWI ETF as global equity proxy

### Calculation Methodology
1. Convert all balance sheets to USD using FX rates
2. Sum Fed + ECB + BoJ assets for total global liquidity
3. Calculate 13-week momentum (percentage change)
4. Normalize to z-scores for consistent scaling
5. Subtract volatility and dollar strength headwinds
6. Apply smoothing for the Full index

### Update Frequency
- Central bank data: Weekly (Friday close)
- Market data: Daily (automatically resampled to weekly)
- Manual updates: Run `liquidity_website.py` or click "Refresh Data" in dashboard

## Limitations

- Does not include Bank of England (data availability issues)
- Does not account for reverse repo operations or other liquidity drains
- Correlation with markets can break down during unique events
- Historical data starts in 2010 (limited pre-GFC coverage)

## Future Enhancements

Potential improvements:
- Add People's Bank of China balance sheet
- Include Treasury General Account (TGA) adjustments
- Add automated email alerts for regime changes
- Deploy dashboard to cloud for remote access
- Add machine learning predictions for liquidity trends

## License

Part of the pcrm-book repository. See main LICENSE file for details.

## Questions or Issues?

This is a research tool for educational purposes. Always combine with other analysis and risk management practices before making investment decisions.
