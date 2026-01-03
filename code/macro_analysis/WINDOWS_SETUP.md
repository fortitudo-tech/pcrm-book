# Windows Setup Guide

## Quick Setup for: `C:\Users\jmj2z\Projects\Claude projects\Maco Analysis`

### Method 1: Automated Setup (Easiest)

1. **Pull the Git Branch** (from your pcrm-book repository):
   ```cmd
   cd path\to\your\pcrm-book
   git fetch origin
   git checkout claude/add-rmp-liquidity-program-Nee07
   git pull
   ```

2. **Run the Setup Script**:

   **Option A - Batch File** (double-click or run from cmd):
   ```cmd
   code\macro_analysis\setup_windows.bat
   ```

   **Option B - PowerShell** (right-click → Run with PowerShell):
   ```powershell
   powershell -ExecutionPolicy Bypass -File code\macro_analysis\setup_windows.ps1
   ```

3. **Done!** All files will be copied to your desired location.

---

### Method 2: Manual Copy

1. **Pull the branch** (see above)

2. **Copy files manually**:
   - Open File Explorer
   - Navigate to: `your-repo\pcrm-book\code\macro_analysis\`
   - Select all files
   - Copy (Ctrl+C)
   - Navigate to: `C:\Users\jmj2z\Projects\Claude projects\Maco Analysis`
   - Paste (Ctrl+V)

---

### Method 3: Direct Download from GitHub

If you don't have the repo locally:

1. Go to: https://github.com/Jerempire/pcrm-book
2. Switch to branch: `claude/add-rmp-liquidity-program-Nee07`
3. Navigate to: `code/macro_analysis/`
4. Download each file individually or download the whole branch as ZIP

---

## After Copying Files

### Step 1: Install Python Packages

Open Command Prompt or PowerShell in your directory:
```cmd
cd "C:\Users\jmj2z\Projects\Claude projects\Maco Analysis"
pip install pandas numpy matplotlib fredapi pandas-datareader yfinance seaborn
```

### Step 2: Test the Installation

Run the demo (no API key needed):
```cmd
python demo_tracker.py
```

This will:
- ✓ Generate mock market data
- ✓ Create visualizations
- ✓ Save two PNG charts
- ✓ Verify everything works

### Step 3: Get FRED API Key

1. Go to: https://fred.stlouisfed.org/
2. Create free account
3. Request API key: https://fred.stlouisfed.org/docs/api/api_key.html
4. Copy your key (looks like: `a1b2c3d4e5f6...`)

### Step 4: Add API Key to Notebook

**Option A - Edit in Jupyter**:
```cmd
jupyter lab rmp_liquidity_tracker.ipynb
```
Find the cell with `FRED_API_KEY = 'YOUR_FRED_API_KEY_HERE'` and replace with your key.

**Option B - Edit in Notepad** (if you're comfortable with JSON):
```cmd
notepad rmp_liquidity_tracker.ipynb
```
Search for `YOUR_FRED_API_KEY_HERE` and replace with your actual key.

**Option C - Edit in VS Code** (recommended):
```cmd
code rmp_liquidity_tracker.ipynb
```

### Step 5: Run the Notebook

```cmd
jupyter lab rmp_liquidity_tracker.ipynb
```

In Jupyter, uncomment these lines in the notebook:
- Line with `fred = Fred(api_key=FRED_API_KEY)`
- All lines in the "Step 2: Fetch FRED data" cell
- All lines in "Step 3: Calculate quadrant positions" cell
- All visualization cells (Steps 4-6)

Then: **Cell → Run All**

---

## Files You'll Have

After setup, your directory will contain:

```
C:\Users\jmj2z\Projects\Claude projects\Maco Analysis\
│
├── rmp_liquidity_tracker.ipynb      Main tracking notebook
├── MARKETS_TO_TRACK.md               Comprehensive reference guide
├── QUICKSTART.md                     Quick start guide
├── README.md                         Overview
├── WINDOWS_SETUP.md                  This file
│
├── demo_tracker.py                   Demo with mock data
├── demo_spider_diagram.png           Example spider diagram
├── demo_dashboard.png                Example dashboard
│
├── test_tracker_simple.py            Test script
├── setup_windows.bat                 Batch setup script
└── setup_windows.ps1                 PowerShell setup script
```

---

## Daily Workflow

### Morning Routine (5 minutes):

**Option 1 - Quick Manual Check**:
1. Open browser, check:
   - DXY: https://www.investing.com/indices/usdollar
   - 10Y-2Y: https://fred.stlouisfed.org/series/T10Y2Y
   - VIX: https://finance.yahoo.com/quote/%5EVIX

**Option 2 - Run Notebook**:
```cmd
cd "C:\Users\jmj2z\Projects\Claude projects\Maco Analysis"
jupyter lab rmp_liquidity_tracker.ipynb
```
- Run cells 1-3 (fetch latest data)
- Check current quadrant position
- Review key metrics

### Weekly Update (15 minutes):

```cmd
cd "C:\Users\jmj2z\Projects\Claude projects\Maco Analysis"
jupyter lab rmp_liquidity_tracker.ipynb
```
- Run all cells to update all data
- Generate fresh spider diagram
- Review liquidity dashboard
- Check for quadrant changes

---

## Troubleshooting

### "pip is not recognized"
→ Python not in PATH. Reinstall Python with "Add to PATH" checked

### "jupyter is not recognized"
→ Install Jupyter: `pip install jupyterlab`

### "Module not found: fredapi"
→ Install packages: `pip install fredapi pandas numpy matplotlib`

### "Can't fetch data"
→ Check internet connection
→ Verify FRED API key is correct
→ Check you're not hitting rate limits (120 calls/min)

### Charts not showing in notebook
→ Make sure you're using Jupyter Lab, not plain Jupyter Notebook
→ Or add `%matplotlib inline` at the top of the notebook

### Path has spaces and commands fail
→ Always use quotes: `cd "C:\Users\jmj2z\Projects\Claude projects\Maco Analysis"`

---

## Pro Tips for Windows

1. **Create Desktop Shortcut**:
   - Right-click desktop → New → Shortcut
   - Target: `cmd /k cd /d "C:\Users\jmj2z\Projects\Claude projects\Maco Analysis" && jupyter lab`
   - Name it "RMP Tracker"

2. **Quick Access**:
   - Pin the folder to Quick Access in File Explorer
   - Add to Windows Terminal as a profile

3. **Scheduled Updates**:
   - Use Task Scheduler to run the notebook weekly
   - Or create a batch file that runs the demo daily

4. **Backup Your API Key**:
   - Save it in a password manager
   - Or create a `config.ini` file (add to .gitignore)

---

## Next Steps

1. ✓ Run `setup_windows.bat` or copy files manually
2. ✓ Install Python packages
3. ✓ Run `python demo_tracker.py` to test
4. ✓ Get FRED API key
5. ✓ Add key to notebook
6. ✓ Run notebook with real data
7. ✓ Set up daily monitoring routine

---

## Support

- Read: `QUICKSTART.md` for detailed usage
- Read: `MARKETS_TO_TRACK.md` for indicator reference
- Read: `README.md` for framework overview

**Ready to start?** Run the setup script or copy the files! 🚀
