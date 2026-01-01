#!/usr/bin/env python3
"""
Continuous scheduler for automated research.

This script runs continuously and executes research at scheduled times.
Alternative to cron for environments where cron isn't available.

Usage:
    python scripts/continuous_scheduler.py
"""

import sys
import time
import schedule
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.daily_research import daily_research_pipeline


def job():
    """Job to run on schedule."""
    print(f"\n🤖 Scheduled job starting at {datetime.now()}")
    try:
        daily_research_pipeline()
        print(f"✓ Job completed successfully at {datetime.now()}")
    except Exception as e:
        print(f"✗ Job failed at {datetime.now()}: {e}")


def main():
    """Run the continuous scheduler."""
    print("="*60)
    print("PCRM Agents - Continuous Scheduler")
    print("="*60)
    print("")
    print("Configured schedules:")

    # Schedule jobs
    # Daily at 6 PM
    schedule.every().day.at("18:00").do(job)
    print("  - Daily at 6:00 PM")

    # You can add more schedules:
    # schedule.every().day.at("09:00").do(job)  # 9 AM
    # schedule.every().monday.at("10:00").do(job)  # Monday 10 AM
    # schedule.every().hour.do(job)  # Every hour

    print("")
    print("Scheduler is running... Press Ctrl+C to stop")
    print("")

    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")


if __name__ == "__main__":
    # Install schedule if not available
    try:
        import schedule
    except ImportError:
        print("Installing schedule library...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "schedule"])
        import schedule

    main()
