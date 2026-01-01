#!/bin/bash
# Setup automated daily research scheduler

echo "==================================================="
echo "PCRM Agents - Daily Research Scheduler Setup"
echo "==================================================="
echo ""

# Get project directory
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
echo "Project directory: $PROJECT_DIR"

# Create logs directory
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/output/daily_reports"

echo ""
echo "Select scheduling option:"
echo "1. Cron (Linux/Mac) - Runs at specific time daily"
echo "2. systemd timer (Linux) - More advanced scheduling"
echo "3. Show manual setup instructions"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "=== CRON SETUP ==="
        echo ""
        echo "Add this line to your crontab (crontab -e):"
        echo ""
        echo "# Daily market research at 6:00 PM Eastern Time"
        echo "0 18 * * * cd $PROJECT_DIR && poetry run python scripts/daily_research.py >> logs/daily_research.log 2>&1"
        echo ""
        echo "Other common schedules:"
        echo "# 9:00 AM daily: 0 9 * * *"
        echo "# 4:00 PM daily: 0 16 * * *"
        echo "# 6:30 PM daily: 30 18 * * *"
        echo "# Weekdays only at 5 PM: 0 17 * * 1-5"
        echo ""
        read -p "Do you want to add the 6 PM schedule now? (y/n): " add_cron

        if [ "$add_cron" = "y" ]; then
            (crontab -l 2>/dev/null; echo "0 18 * * * cd $PROJECT_DIR && poetry run python scripts/daily_research.py >> $PROJECT_DIR/logs/daily_research.log 2>&1") | crontab -
            echo "✓ Cron job added! View with: crontab -l"
        fi
        ;;

    2)
        echo ""
        echo "=== SYSTEMD TIMER SETUP ==="
        echo ""

        # Create service file
        SERVICE_FILE="/tmp/pcrm-research.service"
        cat > "$SERVICE_FILE" << EOF
[Unit]
Description=PCRM Daily Market Research
After=network.target

[Service]
Type=oneshot
User=$USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$(which poetry) run python $PROJECT_DIR/scripts/daily_research.py
StandardOutput=append:$PROJECT_DIR/logs/daily_research.log
StandardError=append:$PROJECT_DIR/logs/daily_research.log

[Install]
WantedBy=multi-user.target
EOF

        # Create timer file
        TIMER_FILE="/tmp/pcrm-research.timer"
        cat > "$TIMER_FILE" << EOF
[Unit]
Description=Run PCRM research daily at 6 PM
Requires=pcrm-research.service

[Timer]
OnCalendar=*-*-* 18:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

        echo "Service file created: $SERVICE_FILE"
        echo "Timer file created: $TIMER_FILE"
        echo ""
        echo "To install, run these commands:"
        echo "  sudo cp $SERVICE_FILE /etc/systemd/system/"
        echo "  sudo cp $TIMER_FILE /etc/systemd/system/"
        echo "  sudo systemctl daemon-reload"
        echo "  sudo systemctl enable pcrm-research.timer"
        echo "  sudo systemctl start pcrm-research.timer"
        echo ""
        echo "To check status:"
        echo "  sudo systemctl status pcrm-research.timer"
        echo "  sudo systemctl list-timers"
        ;;

    3)
        echo ""
        echo "=== MANUAL SETUP INSTRUCTIONS ==="
        echo ""
        echo "OPTION A: Run manually anytime"
        echo "  cd $PROJECT_DIR"
        echo "  poetry run python scripts/daily_research.py"
        echo ""
        echo "OPTION B: Windows Task Scheduler"
        echo "  1. Open Task Scheduler"
        echo "  2. Create Basic Task"
        echo "  3. Trigger: Daily at 6:00 PM"
        echo "  4. Action: Start a program"
        echo "  5. Program: poetry"
        echo "  6. Arguments: run python scripts/daily_research.py"
        echo "  7. Start in: $PROJECT_DIR"
        echo ""
        echo "OPTION C: Python scheduler (runs continuously)"
        echo "  See scripts/continuous_scheduler.py"
        echo ""
        echo "OPTION D: Cloud scheduler (AWS EventBridge, GCP Scheduler, etc.)"
        echo "  Deploy as Lambda/Cloud Function"
        echo "  See PRODUCTION.md for details"
        ;;
esac

echo ""
echo "=== ENVIRONMENT VARIABLES ==="
echo "You can customize behavior with these variables:"
echo "  RESEARCH_TICKERS=SPY,QQQ,TLT,GLD  # Custom ticker list"
echo "  AGENT_LOG_LEVEL=INFO              # Logging verbosity"
echo ""
echo "Add to your .env file or set in your cron job"
echo ""
echo "Setup complete!"
