"""
Apache Airflow DAG for automated daily research.

This DAG runs comprehensive market research daily and can be extended
with additional tasks like sending email reports, storing to database, etc.

Place this file in your Airflow DAGs folder.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from pathlib import Path
import sys

# Add project to path
PROJECT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from src.agents import (
    DataCollectionAgent,
    RiskAnalyticsAgent,
    MarketResearchAgent,
)


def collect_market_data(**context):
    """Task 1: Collect market data."""
    print("Collecting market data...")

    agent = DataCollectionAgent()
    tickers = ['SPY', 'QQQ', 'TLT', 'GLD', 'VTI']

    prices = agent.execute(tickers=tickers, period='1y')

    # Push to XCom for downstream tasks
    context['task_instance'].xcom_push(key='prices', value=prices.to_json())
    context['task_instance'].xcom_push(key='tickers', value=tickers)

    return "Data collection complete"


def analyze_risk(**context):
    """Task 2: Analyze risk metrics."""
    print("Analyzing risk...")

    # Pull data from XCom
    import pandas as pd
    prices_json = context['task_instance'].xcom_pull(
        task_ids='collect_data',
        key='prices'
    )
    prices = pd.read_json(prices_json)

    agent = RiskAnalyticsAgent()
    returns = prices.pct_change().dropna()

    var = agent.value_at_risk(returns, confidence_level=0.95)

    # Push results
    context['task_instance'].xcom_push(key='var', value=var.to_dict())

    return "Risk analysis complete"


def research_market(**context):
    """Task 3: Market research and signals."""
    print("Researching market...")

    import pandas as pd
    prices_json = context['task_instance'].xcom_pull(
        task_ids='collect_data',
        key='prices'
    )
    prices = pd.read_json(prices_json)

    agent = MarketResearchAgent()

    momentum = agent.momentum_analysis(prices)
    regimes = agent.regime_detection(prices.pct_change().dropna())

    # Push results
    context['task_instance'].xcom_push(
        key='rsi',
        value=momentum['RSI'].iloc[-1].to_dict()
    )

    return "Market research complete"


def generate_report(**context):
    """Task 4: Generate and save report."""
    print("Generating report...")

    tickers = context['task_instance'].xcom_pull(
        task_ids='collect_data',
        key='tickers'
    )
    var = context['task_instance'].xcom_pull(
        task_ids='analyze_risk',
        key='var'
    )
    rsi = context['task_instance'].xcom_pull(
        task_ids='research_market',
        key='rsi'
    )

    # Generate report
    report = f"""
    DAILY MARKET RESEARCH REPORT
    Date: {datetime.now().strftime('%Y-%m-%d')}
    ================================

    TICKERS ANALYZED: {', '.join(tickers)}

    RISK METRICS (VaR 95%):
    {var}

    MOMENTUM (RSI):
    {rsi}

    """

    # Save report
    output_dir = PROJECT_DIR / 'output' / 'airflow_reports'
    output_dir.mkdir(parents=True, exist_ok=True)

    report_file = output_dir / f"report_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(report_file, 'w') as f:
        f.write(report)

    print(f"Report saved to {report_file}")

    # Push for email
    context['task_instance'].xcom_push(key='report', value=report)

    return str(report_file)


# Default arguments
default_args = {
    'owner': 'pcrm-agents',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email': ['your-email@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'daily_market_research',
    default_args=default_args,
    description='Daily automated market research',
    schedule_interval='0 18 * * *',  # 6 PM daily
    catchup=False,
    tags=['finance', 'research', 'daily'],
)

# Define tasks
task_collect = PythonOperator(
    task_id='collect_data',
    python_callable=collect_market_data,
    dag=dag,
)

task_risk = PythonOperator(
    task_id='analyze_risk',
    python_callable=analyze_risk,
    dag=dag,
)

task_research = PythonOperator(
    task_id='research_market',
    python_callable=research_market,
    dag=dag,
)

task_report = PythonOperator(
    task_id='generate_report',
    python_callable=generate_report,
    dag=dag,
)

# Optional: Send email with report
# task_email = EmailOperator(
#     task_id='send_email',
#     to='your-email@example.com',
#     subject='Daily Market Research Report - {{ ds }}',
#     html_content='{{ task_instance.xcom_pull(task_ids="generate_report", key="report") }}',
#     dag=dag,
# )

# Define task dependencies
task_collect >> [task_risk, task_research] >> task_report
# task_report >> task_email  # Uncomment if using email
