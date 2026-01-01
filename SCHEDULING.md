# Automated Research Scheduling Guide

The agents don't run automatically by default - they're **tools** you call when needed. This guide shows you how to set up automated daily research.

## 🤖 What Gets Automated

The **daily research pipeline** (`scripts/daily_research.py`) automatically:

1. ✅ Collects latest market data for your tickers
2. ✅ Generates market summary (prices, daily changes)
3. ✅ Calculates risk metrics (VaR, volatility)
4. ✅ Computes momentum indicators (RSI, MACD)
5. ✅ Detects market regime (volatility-based)
6. ✅ Analyzes correlations across assets
7. ✅ Saves detailed report to file
8. ✅ Logs all activity

## ⏰ Scheduling Options

### Option 1: Cron Job (Linux/Mac) - **Recommended for Simplicity**

**When to use:** Personal servers, VPS, Mac computers
**Runs:** At specific times daily
**Setup time:** 2 minutes

```bash
# Run the setup helper
./scripts/setup_scheduler.sh

# Or manually add to crontab (crontab -e):
0 18 * * * cd /path/to/pcrm-book && poetry run python scripts/daily_research.py >> logs/daily_research.log 2>&1
```

**Common schedules:**
```bash
# 9:00 AM daily
0 9 * * *

# 4:00 PM daily (market close)
0 16 * * *

# 6:00 PM daily
0 18 * * *

# 6:30 PM daily
30 18 * * *

# 5:00 PM weekdays only
0 17 * * 1-5

# Every 4 hours
0 */4 * * *
```

**Verify it's running:**
```bash
crontab -l  # List scheduled jobs
tail -f logs/daily_research.log  # Watch live output
```

---

### Option 2: Continuous Python Scheduler - **Easiest**

**When to use:** Any platform, development, testing
**Runs:** Keeps running and executes on schedule
**Setup time:** 1 minute

```bash
# Start the scheduler (runs in foreground)
poetry run python scripts/continuous_scheduler.py

# Or run in background
nohup poetry run python scripts/continuous_scheduler.py > logs/scheduler.log 2>&1 &
```

**Advantages:**
- Works on any OS (Windows, Mac, Linux)
- Easy to test and debug
- No system configuration needed

**Disadvantages:**
- Must keep running (use screen/tmux for persistence)
- Will stop if server reboots (unless configured as service)

---

### Option 3: Windows Task Scheduler

**When to use:** Windows servers/desktops
**Runs:** At specific times
**Setup time:** 5 minutes

1. Open **Task Scheduler**
2. Click **Create Basic Task**
3. Name: "PCRM Daily Research"
4. Trigger: **Daily** at 6:00 PM
5. Action: **Start a program**
   - Program: `poetry` (or full path to poetry.exe)
   - Arguments: `run python scripts/daily_research.py`
   - Start in: `C:\path\to\pcrm-book`
6. Finish

---

### Option 4: systemd Timer (Linux) - **Production Linux Servers**

**When to use:** Production Linux servers
**Runs:** At specific times with automatic retries
**Setup time:** 5 minutes

```bash
# Run the setup helper
./scripts/setup_scheduler.sh
# Choose option 2

# Or manually:
sudo cp scripts/systemd/pcrm-research.service /etc/systemd/system/
sudo cp scripts/systemd/pcrm-research.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable pcrm-research.timer
sudo systemctl start pcrm-research.timer
```

**Check status:**
```bash
sudo systemctl status pcrm-research.timer
sudo systemctl list-timers
journalctl -u pcrm-research.service -f  # Live logs
```

---

### Option 5: Apache Airflow - **Enterprise Data Pipelines**

**When to use:** Complex workflows, enterprise environments
**Runs:** Sophisticated scheduling with DAG dependencies
**Setup time:** 30 minutes (if Airflow already setup)

```bash
# Copy DAG to Airflow
cp scripts/airflow_dag.py ~/airflow/dags/

# Airflow will automatically detect and schedule it
```

**Features:**
- Task dependencies (data collection → analysis → report)
- Automatic retries on failure
- Email notifications
- Web UI for monitoring
- Data lineage tracking

**Configuration:**
Edit `scripts/airflow_dag.py`:
- `schedule_interval='0 18 * * *'` - When to run
- `email=['your@email.com']` - Alert recipients
- Customize tasks for your workflow

---

### Option 6: Cloud Schedulers - **Serverless**

#### AWS EventBridge + Lambda

```bash
# 1. Package the code
cd /path/to/pcrm-book
zip -r pcrm-agents.zip src/ scripts/

# 2. Create Lambda function
# - Runtime: Python 3.11
# - Handler: scripts.daily_research.lambda_handler
# - Memory: 512 MB
# - Timeout: 5 minutes

# 3. Create EventBridge rule
# - Schedule: cron(0 18 * * ? *)
# - Target: Lambda function
```

#### GCP Cloud Scheduler + Cloud Functions

```bash
# Deploy as Cloud Function
gcloud functions deploy pcrm-daily-research \
  --runtime python311 \
  --trigger-http \
  --entry-point daily_research_pipeline

# Create Cloud Scheduler job
gcloud scheduler jobs create http pcrm-research \
  --schedule "0 18 * * *" \
  --uri "https://YOUR-REGION-PROJECT.cloudfunctions.net/pcrm-daily-research"
```

---

## 🎯 Quick Start: Get Running in 60 Seconds

**The fastest way to test:**

```bash
# 1. Run manually first to verify it works
cd /path/to/pcrm-book
poetry run python scripts/daily_research.py

# 2. If successful, set up automation
./scripts/setup_scheduler.sh
```

---

## ⚙️ Customization

### Change Tickers

**Option A: Environment Variable**
```bash
export RESEARCH_TICKERS="AAPL,MSFT,GOOGL,AMZN,TSLA"
```

**Option B: Edit Script**
Edit `scripts/daily_research.py`:
```python
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
```

### Change Schedule Time

Edit the cron expression:
```bash
# Format: minute hour day month weekday
# Examples:
0 9 * * *     # 9:00 AM daily
30 16 * * *   # 4:30 PM daily
0 18 * * 1-5  # 6:00 PM weekdays only
0 0 * * 0     # Midnight every Sunday
```

### Add Email Notifications

```python
# Add to daily_research.py
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'alerts@yourcompany.com'
    msg['To'] = 'you@email.com'

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your@gmail.com', 'app-password')
        server.send_message(msg)

# Call after research completes
send_email("Daily Research Complete", report_text)
```

### Store Results in Database

```python
# Add to daily_research.py
import sqlite3

def save_to_database(results):
    conn = sqlite3.connect('research.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_research (
            date TEXT,
            ticker TEXT,
            var_95 REAL,
            volatility REAL,
            rsi REAL
        )
    ''')

    # Insert results
    for ticker in results['tickers']:
        cursor.execute(
            'INSERT INTO daily_research VALUES (?, ?, ?, ?, ?)',
            (today, ticker, var[ticker], vol[ticker], rsi[ticker])
        )

    conn.commit()
    conn.close()
```

---

## 📊 Example Output

When the automated research runs, you'll see:

```
============================================================
Daily Market Research - 2025-01-15 18:00:00
============================================================

1. Collecting market data...
   ✓ Collected 252 days of data for 8 assets

2. Generating market summary...

   LATEST PRICES:
   🟢 SPY: $450.23 (+0.45%)
   🔴 TLT: $95.67 (-0.32%)
   🟢 GLD: $180.45 (+0.15%)

3. Analyzing risk metrics...

   RISK METRICS (95% VaR, Annual Volatility):
   SPY: VaR=-1.25%, Vol=15.2%
   TLT: VaR=-0.98%, Vol=12.1%
   GLD: VaR=-1.10%, Vol=13.5%

4. Checking momentum indicators...

   RSI (14-day):
   SPY: 58.3 - ✓ Neutral
   TLT: 45.2 - ✓ Neutral
   GLD: 72.1 - ⚠️  OVERBOUGHT

[... more analysis ...]

7. Saving report...
   ✓ Report saved to output/daily_reports/daily_report_20250115_180000.txt

============================================================
Research Complete!
============================================================
```

Reports are saved to: `output/daily_reports/`

---

## 🔔 Monitoring & Alerts

### Check if it's running

```bash
# Cron
crontab -l

# systemd
sudo systemctl status pcrm-research.timer

# Continuous scheduler
ps aux | grep continuous_scheduler.py

# Check recent runs
ls -lt output/daily_reports/ | head
tail -n 50 logs/daily_research.log
```

### Set up alerts for failures

Add to cron job:
```bash
0 18 * * * cd /path/to/pcrm-book && poetry run python scripts/daily_research.py >> logs/daily_research.log 2>&1 || echo "Research failed!" | mail -s "PCRM Alert" you@email.com
```

Or use monitoring tools:
- **Healthchecks.io** - Free ping monitoring
- **UptimeRobot** - Web endpoint monitoring
- **DataDog** - Enterprise monitoring
- **Prometheus + Grafana** - Self-hosted

---

## 🐛 Troubleshooting

### Script doesn't run

```bash
# Test manually first
cd /path/to/pcrm-book
poetry run python scripts/daily_research.py

# Check permissions
chmod +x scripts/daily_research.py

# Check cron is running
sudo systemctl status cron  # or crond

# Check logs
tail -f logs/daily_research.log
```

### No output/empty logs

```bash
# Redirect stderr to see errors
poetry run python scripts/daily_research.py 2>&1 | tee logs/debug.log

# Check environment
poetry run python -c "from src.agents import DataCollectionAgent; print('OK')"
```

### Data collection fails

```bash
# Network issue - check internet
ping yahoo.com

# Rate limiting - add delays
# Edit daily_research.py to add time.sleep(1) between requests
```

---

## 🚀 Advanced: Multi-Strategy Research

Create custom research scripts:

```python
# scripts/weekly_portfolio_rebalance.py
from src.agents import *

def weekly_rebalance():
    """Run every Sunday to determine rebalancing needs."""
    # Your logic here
    pass

# Schedule: 0 20 * * 0 (8 PM Sundays)
```

```python
# scripts/intraday_monitor.py
from src.agents import *

def check_positions():
    """Run every hour during market hours."""
    # Your logic here
    pass

# Schedule: 0 9-16 * * 1-5 (9 AM-4 PM weekdays)
```

---

## 📅 Recommended Schedule

For most users:

```bash
# Market close analysis (4:15 PM ET weekdays)
15 16 * * 1-5 cd /path/to/pcrm-book && poetry run python scripts/daily_research.py

# Weekly deep dive (Sunday 8 PM)
0 20 * * 0 cd /path/to/pcrm-book && poetry run python scripts/weekly_analysis.py
```

---

## ✅ Production Checklist

Before going live with automation:

- [ ] Test script manually and verify output
- [ ] Check logs directory exists and is writable
- [ ] Verify network connectivity to data sources
- [ ] Set up log rotation (logrotate)
- [ ] Configure email alerts for failures
- [ ] Test schedule timing in your timezone
- [ ] Set up monitoring/healthchecks
- [ ] Document your configuration
- [ ] Create backup/restore procedures
- [ ] Test error handling (network down, invalid ticker, etc.)

---

## 📚 Related Documentation

- Main setup: [README.md](README.md)
- Production deployment: [PRODUCTION.md](PRODUCTION.md)
- Agent capabilities: [src/agents/README.md](src/agents/README.md)
- Example usage: [code/agents_example.ipynb](code/agents_example.ipynb)

---

**Need help?** Check the [GitHub Issues](https://github.com/fortitudo-tech/pcrm-book/issues)
