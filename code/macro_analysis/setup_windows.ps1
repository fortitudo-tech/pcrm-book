# PowerShell Setup Script for RMP Liquidity Tracker
# Run this from your pcrm-book repository directory

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "RMP Liquidity Tracker - Windows Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$destination = "C:\Users\jmj2z\Projects\Claude projects\Maco Analysis"

# Create destination directory if it doesn't exist
Write-Host "Creating destination directory..." -ForegroundColor Yellow
if (-not (Test-Path $destination)) {
    New-Item -ItemType Directory -Path $destination -Force | Out-Null
    Write-Host "✓ Created: $destination" -ForegroundColor Green
} else {
    Write-Host "✓ Directory already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Copying files..." -ForegroundColor Yellow

# Copy all relevant files
$files = @(
    "code\macro_analysis\rmp_liquidity_tracker.ipynb",
    "code\macro_analysis\MARKETS_TO_TRACK.md",
    "code\macro_analysis\QUICKSTART.md",
    "code\macro_analysis\README.md",
    "code\macro_analysis\demo_tracker.py",
    "code\macro_analysis\demo_spider_diagram.png",
    "code\macro_analysis\demo_dashboard.png",
    "code\macro_analysis\test_tracker_simple.py"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $fileName = Split-Path $file -Leaf
        Copy-Item -Path $file -Destination $destination -Force
        Write-Host "  ✓ Copied: $fileName" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Not found: $file" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files have been copied to:" -ForegroundColor White
Write-Host "  $destination" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Navigate to the directory:" -ForegroundColor White
Write-Host "   cd '$destination'" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Install required packages:" -ForegroundColor White
Write-Host "   pip install pandas numpy matplotlib fredapi pandas-datareader" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Get your FREE FRED API key:" -ForegroundColor White
Write-Host "   https://fred.stlouisfed.org/docs/api/api_key.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Run the demo (no API key needed):" -ForegroundColor White
Write-Host "   python demo_tracker.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "5. Open the notebook:" -ForegroundColor White
Write-Host "   jupyter lab rmp_liquidity_tracker.ipynb" -ForegroundColor Cyan
Write-Host ""
Write-Host "6. Add your FRED API key in the notebook" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
