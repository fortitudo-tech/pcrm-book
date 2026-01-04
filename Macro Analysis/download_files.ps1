# PowerShell Script to Download RMP Tracker Files from GitHub
# Run this from: C:\Users\jmj2z\Projects\Claude projects\Maco Analysis

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Downloading RMP Liquidity Tracker Files" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "https://raw.githubusercontent.com/Jerempire/pcrm-book/claude/add-rmp-liquidity-program-Nee07/code/macro_analysis"

$files = @(
    "rmp_liquidity_tracker.ipynb",
    "MARKETS_TO_TRACK.md",
    "QUICKSTART.md",
    "README.md",
    "WINDOWS_SETUP.md",
    "demo_tracker.py",
    "demo_spider_diagram.png",
    "demo_dashboard.png",
    "test_tracker_simple.py",
    "quick_test.py"
)

Write-Host "Downloading files from GitHub..." -ForegroundColor Yellow
Write-Host ""

foreach ($file in $files) {
    $url = "$baseUrl/$file"
    $output = $file

    try {
        Write-Host "  Downloading: $file" -ForegroundColor White -NoNewline
        Invoke-WebRequest -Uri $url -OutFile $output -ErrorAction Stop
        Write-Host " ✓" -ForegroundColor Green
    } catch {
        Write-Host " ✗ Failed" -ForegroundColor Red
        Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Download Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Files downloaded to current directory." -ForegroundColor White
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Run the demo (no API key needed):" -ForegroundColor White
Write-Host "   python demo_tracker.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Get FREE FRED API key:" -ForegroundColor White
Write-Host "   https://fred.stlouisfed.org/docs/api/api_key.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Open notebook and add your API key:" -ForegroundColor White
Write-Host "   jupyter lab rmp_liquidity_tracker.ipynb" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Read the guides:" -ForegroundColor White
Write-Host "   - QUICKSTART.md (getting started)" -ForegroundColor Cyan
Write-Host "   - MARKETS_TO_TRACK.md (what to track)" -ForegroundColor Cyan
Write-Host "   - WINDOWS_SETUP.md (Windows tips)" -ForegroundColor Cyan
Write-Host ""

# List downloaded files
Write-Host "Downloaded files:" -ForegroundColor Yellow
Get-ChildItem -File | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize

Write-Host ""
Write-Host "Ready to use! Run: python demo_tracker.py" -ForegroundColor Green
Write-Host ""
