# ======================================================================
# DIY Global Liquidity Index (GLI) Script - PLOTLY VERSION
# ======================================================================
# Requirements:
#   pip install pandas pandas_datareader yfinance plotly openpyxl xlsxwriter
# ======================================================================

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pandas_datareader import data as web
import yfinance as yf
from datetime import datetime

# ----------------------------------------------------------------------
# 1. Parameters
# ----------------------------------------------------------------------
START_DATE = "2010-01-01"
EXCEL_OUTPUT = "global_liquidity_DIY_v2.xlsx"

# ----------------------------------------------------------------------
# 2. Download central-bank balance sheet data from FRED
# ----------------------------------------------------------------------
cb_series = {
    "Fed": "WALCL",
    "ECB": "ECBASSETSW",
    "BOJ": "JPNASSETS"
}

print("Downloading central bank balance sheets from FRED...")
cb_list = []
cb_names = []

for name, code in cb_series.items():
    try:
        series = web.DataReader(code, "fred", START_DATE)
        cb_list.append(series)
        cb_names.append(name)
        print(f"  - {name}: {code} OK")
    except Exception as e:
        print(f"  - {name}: FAILED ({code}) -> {e}")

cb = pd.concat(cb_list, axis=1, keys=cb_names)
cb.columns = cb.columns.get_level_values(0)
print(f"Central bank data before ffill: {cb.shape}")
cb = cb.ffill()
cb = cb.dropna()
print("Central bank data shape:", cb.shape)

# ----------------------------------------------------------------------
# 3. FX series to convert ECB/BoJ to USD
# ----------------------------------------------------------------------
print("Downloading FX data from FRED...")
eurusd = web.DataReader("DEXUSEU", "fred", START_DATE)
jpyusd = web.DataReader("DEXJPUS", "fred", START_DATE)

fx = pd.concat([eurusd, jpyusd], axis=1)
fx.columns = ["EURUSD", "JPYUSD"]
fx = fx.ffill()

print("FX data shape:", fx.shape)

data = cb.join(fx, how="inner")
print("Merged CB + FX shape:", data.shape)

# ----------------------------------------------------------------------
# 4. Convert CB balance sheets to USD and compute total CB liquidity
# ----------------------------------------------------------------------
data["ECB_USD"] = data["ECB"] / data["EURUSD"]
if "BOE" in data.columns:
    data["BOE_USD"] = data["BOE"] / data["GBPUSD"]
    cb_usd_cols = ["Fed", "ECB_USD", "BOE_USD", "BOJ_USD"]
else:
    print("Warning: BOE data not available, excluding from calculations")
    cb_usd_cols = ["Fed", "ECB_USD", "BOJ_USD"]
data["BOJ_USD"] = data["BOJ"] / data["JPYUSD"]

data["CB_Total"] = data[cb_usd_cols].sum(axis=1)
print("Computed CB_Total in USD.")

# ----------------------------------------------------------------------
# 5. VIX (volatility) and DXY (broad dollar index)
# ----------------------------------------------------------------------
print("Downloading VIX and DXY from FRED...")
try:
    move = web.DataReader("VIXCLS", "fred", START_DATE)
    has_move = True
    print("  - VIX: OK")
except Exception as e:
    print(f"  - VIX: FAILED -> {e}")
    has_move = False

try:
    dxy = web.DataReader("DTWEXBGS", "fred", START_DATE)
    has_dxy = True
    print("  - DXY: OK")
except Exception as e:
    print(f"  - DXY: FAILED -> {e}")
    has_dxy = False

if has_move:
    data = data.join(move, how="inner")
if has_dxy:
    data = data.join(dxy, how="inner")

additional_cols = ["ECB_USD"]
if "BOE" in cb.columns:
    additional_cols.append("BOE_USD")
additional_cols.extend(["BOJ_USD", "CB_Total"])
if has_move:
    additional_cols.append("VIX")
if has_dxy:
    additional_cols.append("DXY")
data.columns = list(cb.columns) + list(fx.columns) + additional_cols

data = data.dropna()
print("Final merged daily data shape:", data.shape)

# ----------------------------------------------------------------------
# 6. Resample to weekly and build GLI_Flash + GLI_Full
# ----------------------------------------------------------------------
print("Resampling to weekly (Friday close)...")
weekly = data.resample("W-FRI").last()
weekly = weekly.dropna()
print("Weekly data shape:", weekly.shape)

def full_sample_zscore(x: pd.Series) -> pd.Series:
    return (x - x.mean()) / x.std()

def clip_zscore(z: pd.Series, clip: float = 3.0) -> pd.Series:
    return z.clip(lower=-clip, upper=clip)

cb_change_13w = weekly["CB_Total"].pct_change(13)
gli_flash = full_sample_zscore(cb_change_13w)
gli_flash = clip_zscore(gli_flash, clip=3.0)
gli_flash = gli_flash.rolling(window=4, min_periods=1).mean()

if has_move and "VIX" in weekly.columns:
    vix_z = full_sample_zscore(weekly["VIX"])
    vix_z = clip_zscore(vix_z, clip=3.0)
    gli_flash = gli_flash - vix_z

if has_dxy and "DXY" in weekly.columns:
    dxy_z = full_sample_zscore(weekly["DXY"])
    dxy_z = clip_zscore(dxy_z, clip=3.0)
    gli_flash = gli_flash - dxy_z

weekly["GLI_Flash"] = gli_flash
weekly["GLI_Full"] = weekly["GLI_Flash"].rolling(window=20, min_periods=10).mean()
print("Computed GLI_Flash and GLI_Full.")

# ----------------------------------------------------------------------
# 7. Growth metrics
# ----------------------------------------------------------------------
cb_smoothed = weekly["CB_Total"].rolling(window=4, min_periods=1).mean()
weekly["CB_YoY"] = cb_smoothed.pct_change(52)
growth_3m = cb_smoothed.pct_change(13).clip(lower=-0.2, upper=0.3)
cb_3m_ann = ((1 + growth_3m) ** (52/13)) - 1
weekly["CB_3m_ann"] = cb_3m_ann.clip(lower=-0.6, upper=1.5)
print("Computed CB_YoY and CB_3m_ann growth rates.")

# ----------------------------------------------------------------------
# 8. MSCI overlay
# ----------------------------------------------------------------------
print("Downloading ACWI (MSCI proxy) from Yahoo Finance...")
acwi_data = yf.download("ACWI", start=START_DATE, progress=False)

if isinstance(acwi_data.columns, pd.MultiIndex):
    if "Adj Close" in acwi_data.columns.get_level_values(0):
        acwi = acwi_data.xs("Adj Close", axis=1, level=0)
        if isinstance(acwi, pd.DataFrame):
            acwi = acwi.iloc[:, 0]
    else:
        acwi = acwi_data.xs("Close", axis=1, level=0)
        if isinstance(acwi, pd.DataFrame):
            acwi = acwi.iloc[:, 0]
elif "Adj Close" in acwi_data.columns:
    acwi = acwi_data["Adj Close"]
else:
    acwi = acwi_data["Close"]

acwi.name = "ACWI"

weekly = weekly.join(acwi.resample("W-FRI").last())
weekly = weekly.dropna(subset=["ACWI"])
print("Weekly data with ACWI shape:", weekly.shape)

def normalize_full_sample(x: pd.Series) -> pd.Series:
    return (x - x.min()) / (x.max() - x.min())

overlay = pd.DataFrame({
    "GLI": normalize_full_sample(weekly["GLI_Full"]),
    "MSCI": normalize_full_sample(weekly["ACWI"])
}).dropna()

print("Overlay data shape:", overlay.shape)

# ----------------------------------------------------------------------
# 9. Generate Interactive Plotly Charts
# ----------------------------------------------------------------------
print("Generating interactive Plotly charts...")

def create_flash_vs_full_chart(tick_type='yearly', suffix=''):
    """Create interactive Flash vs Full chart"""
    if tick_type == 'weekly':
        cutoff_date = pd.Timestamp.now() - pd.DateOffset(years=2)
        data_subset = weekly[weekly.index >= cutoff_date]
    elif tick_type == 'monthly':
        cutoff_date = pd.Timestamp.now() - pd.DateOffset(years=6)
        data_subset = weekly[weekly.index >= cutoff_date]
    else:
        data_subset = weekly

    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data_subset.index,
        y=data_subset["GLI_Flash"],
        name="GLI Flash",
        line=dict(color='blue', width=1.5),
        opacity=0.7,
        hovertemplate='<b>GLI Flash</b><br>Date: %{x}<br>Value: %{y:.2f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=data_subset.index,
        y=data_subset["GLI_Full"],
        name="GLI Full (Smoothed)",
        line=dict(color='orange', width=3),
        hovertemplate='<b>GLI Full</b><br>Date: %{x}<br>Value: %{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Global Liquidity – Flash vs Full ({tick_type.capitalize()} View)",
        xaxis_title="Date",
        yaxis_title="Index (z-score based)",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.write_html(f'gli_plot_flash_vs_full{suffix}.html')

# Generate all three versions
create_flash_vs_full_chart('yearly', '_yearly')
create_flash_vs_full_chart('monthly', '_monthly')
create_flash_vs_full_chart('weekly', '_weekly')

def create_growth_chart(tick_type='yearly', suffix=''):
    """Create interactive growth chart with dual y-axes"""
    if tick_type == 'weekly':
        cutoff_date = pd.Timestamp.now() - pd.DateOffset(years=2)
        data_subset = weekly[weekly.index >= cutoff_date]
    elif tick_type == 'monthly':
        cutoff_date = pd.Timestamp.now() - pd.DateOffset(years=6)
        data_subset = weekly[weekly.index >= cutoff_date]
    else:
        data_subset = weekly

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=data_subset.index,
            y=data_subset["CB_3m_ann"] * 100,
            name="3-Month Annualized",
            line=dict(color='royalblue', width=2),
            hovertemplate='<b>3M Ann Growth</b><br>Date: %{x}<br>Value: %{y:.1f}%<extra></extra>'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=data_subset.index,
            y=data_subset["CB_YoY"] * 100,
            name="YoY Change",
            line=dict(color='orange', width=3),
            hovertemplate='<b>YoY Growth</b><br>Date: %{x}<br>Value: %{y:.1f}%<extra></extra>'
        ),
        secondary_y=True
    )
    
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="3-Month Annualized (%)", secondary_y=False)
    fig.update_yaxes(title_text="Year-over-Year (%)", secondary_y=True)
    
    fig.update_layout(
        title=f"Global Liquidity Growth ({tick_type.capitalize()} View)",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.write_html(f'gli_plot_growth{suffix}.html')

create_growth_chart('yearly', '_yearly')
create_growth_chart('monthly', '_monthly')
create_growth_chart('weekly', '_weekly')

def create_overlay_chart(tick_type='yearly', suffix=''):
    """Create interactive overlay chart"""
    if tick_type == 'weekly':
        cutoff_date = pd.Timestamp.now() - pd.DateOffset(years=2)
        data_subset = overlay[overlay.index >= cutoff_date]
    elif tick_type == 'monthly':
        cutoff_date = pd.Timestamp.now() - pd.DateOffset(years=6)
        data_subset = overlay[overlay.index >= cutoff_date]
    else:
        data_subset = overlay

    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data_subset.index,
        y=data_subset["MSCI"],
        name="MSCI ACWI (Global Equities)",
        line=dict(color='black', width=2.5),
        hovertemplate='<b>MSCI ACWI</b><br>Date: %{x}<br>Value: %{y:.3f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=data_subset.index,
        y=data_subset["GLI"],
        name="Global Liquidity Index (Full)",
        line=dict(color='orange', width=2.5),
        hovertemplate='<b>GLI Full</b><br>Date: %{x}<br>Value: %{y:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Global Liquidity vs. Equities ({tick_type.capitalize()} View)",
        xaxis_title="Date",
        yaxis_title="Normalized Index (0-1)",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.write_html(f'gli_plot_msci_overlay{suffix}.html')

create_overlay_chart('yearly', '_yearly')
create_overlay_chart('monthly', '_monthly')
create_overlay_chart('weekly', '_weekly')

print("Generated 9 interactive Plotly charts (HTML format)")

# ----------------------------------------------------------------------
# 10. Export to Excel (same as before)
# ----------------------------------------------------------------------
print(f"Writing data to Excel: {EXCEL_OUTPUT}")

from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import ColorScaleRule

weekly_export = weekly.copy()
weekly_export["Liquidity_Pct_Change"] = weekly_export["CB_Total"].pct_change() * 100

def get_trend_signal(pct_change):
    if pd.isna(pct_change):
        return "Flat"
    elif pct_change > 1.0:
        return "Rising"
    elif pct_change < -1.0:
        return "Falling"
    else:
        return "Flat"

weekly_export["Trend_Signal"] = weekly_export["Liquidity_Pct_Change"].apply(get_trend_signal)

with pd.ExcelWriter(EXCEL_OUTPUT, engine="openpyxl") as writer:
    weekly_export.to_excel(writer, sheet_name="Weekly_Liquidity")
    overlay.to_excel(writer, sheet_name="MSCI_Overlay")
    
    workbook = writer.book
    worksheet = writer.sheets["Weekly_Liquidity"]
    max_row = worksheet.max_row
    
    key_columns = {
        'I': 'CB_Total',
        'L': 'GLI_Flash',
        'M': 'GLI_Full',
        'N': 'CB_YoY',
        'O': 'CB_3m_ann'
    }
    
    for col_letter in key_columns.keys():
        cell_range = f"{col_letter}2:{col_letter}{max_row}"
        rule = ColorScaleRule(
            start_type="min", start_color="FF6B6B",
            mid_type="percentile", mid_value=50, mid_color="FFD93D",
            end_type="max", end_color="6BCF7F"
        )
        worksheet.conditional_formatting.add(cell_range, rule)

print("Done. Excel file and interactive charts saved!")
