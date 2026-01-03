@echo off
REM Setup script for copying RMP Liquidity Tracker to Windows location
REM Run this from your pcrm-book repository directory

echo ================================================
echo RMP Liquidity Tracker - Windows Setup
echo ================================================
echo.

set DEST="C:\Users\jmj2z\Projects\Claude projects\Maco Analysis"

echo Creating destination directory...
if not exist %DEST% mkdir %DEST%

echo.
echo Copying files from repository to %DEST%...
echo.

xcopy /Y /I "code\macro_analysis\*.ipynb" %DEST%
xcopy /Y /I "code\macro_analysis\*.md" %DEST%
xcopy /Y /I "code\macro_analysis\*.py" %DEST%
xcopy /Y /I "code\macro_analysis\*.png" %DEST%

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Files have been copied to:
echo %DEST%
echo.
echo Next steps:
echo 1. Navigate to the directory:
echo    cd %DEST%
echo.
echo 2. Install required packages:
echo    pip install pandas numpy matplotlib fredapi pandas-datareader
echo.
echo 3. Get your FREE FRED API key:
echo    https://fred.stlouisfed.org/docs/api/api_key.html
echo.
echo 4. Open the notebook:
echo    jupyter lab rmp_liquidity_tracker.ipynb
echo.
echo 5. Add your FRED API key to the notebook
echo.
echo Or run the demo first:
echo    python demo_tracker.py
echo.
pause
