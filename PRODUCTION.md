# Production Deployment Guide

This guide covers deploying the PCRM Book agents in a production environment.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Testing](#testing)
5. [Deployment Options](#deployment-options)
6. [Monitoring](#monitoring)
7. [Performance Optimization](#performance-optimization)
8. [Security Considerations](#security-considerations)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- Python 3.9 or higher
- 4GB RAM minimum (8GB recommended)
- 1GB free disk space
- Internet connection for data collection

### Software Dependencies

- Poetry (for dependency management)
- Git (for version control)
- Optional: Docker (for containerized deployment)

## Installation

### Option 1: Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/fortitudo-tech/pcrm-book.git
cd pcrm-book

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Option 2: Using pip

```bash
# Clone the repository
git clone https://github.com/fortitudo-tech/pcrm-book.git
cd pcrm-book

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Option 3: Using Conda

```bash
# Clone the repository
git clone https://github.com/fortitudo-tech/pcrm-book.git
cd pcrm-book

# Create and activate conda environment
conda env create -f environment.yml
conda activate pcrm-book
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Logging
AGENT_LOG_LEVEL=INFO
AGENT_LOG_FILE=/var/log/agents/agents.log

# Caching
AGENT_CACHE_DIR=/var/cache/agents
AGENT_CACHE_ENABLED=true
AGENT_CACHE_TTL=3600

# Risk Analytics
DEFAULT_CONFIDENCE_LEVEL=0.95
DEFAULT_RISK_FREE_RATE=0.02
PERIODS_PER_YEAR=252

# Backtesting
DEFAULT_INITIAL_CAPITAL=100000
DEFAULT_COMMISSION=0.001
DEFAULT_SLIPPAGE=0.0005
DEFAULT_REBALANCE_FREQ=monthly

# API Settings
MAX_RETRIES=3
RETRY_DELAY=1
REQUEST_TIMEOUT=30

# Performance
MAX_WORKERS=4
BATCH_SIZE=100
```

### Loading Configuration

```python
from src.agents.config import config

# Use configuration in your code
print(config.DEFAULT_CONFIDENCE_LEVEL)
print(config.LOG_LEVEL)
```

### Custom Configuration

```python
from src.agents.config import AgentConfig

# Override defaults
class ProductionConfig(AgentConfig):
    LOG_LEVEL = 'WARNING'
    DEFAULT_INITIAL_CAPITAL = 1000000
    MAX_WORKERS = 8

# Use custom configuration
config = ProductionConfig()
```

## Testing

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src/agents --cov-report=html

# Run specific test file
poetry run pytest tests/agents/test_risk_analytics_agent.py

# Run tests with specific marker
poetry run pytest -m "not slow"

# Run tests in parallel
poetry run pytest -n auto
```

### Test Coverage

Aim for at least 80% test coverage:

```bash
# Generate coverage report
poetry run pytest --cov=src/agents --cov-report=term-missing

# View HTML coverage report
poetry run pytest --cov=src/agents --cov-report=html
open htmlcov/index.html
```

### Continuous Integration

Tests run automatically on:
- Push to main/develop branches
- Pull requests
- Scheduled daily runs

See `.github/workflows/test.yml` for CI configuration.

## Deployment Options

### Option 1: Traditional Server Deployment

```bash
# On production server
git clone https://github.com/fortitudo-tech/pcrm-book.git
cd pcrm-book
poetry install --no-dev
poetry run python -c "from src.agents import DataCollectionAgent; print('OK')"
```

### Option 2: Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copy application
COPY src/ ./src/

# Set environment variables
ENV AGENT_LOG_LEVEL=INFO
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["python", "-m", "src.agents"]
```

Build and run:

```bash
docker build -t pcrm-agents .
docker run -d -v /data:/data pcrm-agents
```

### Option 3: Serverless Deployment (AWS Lambda)

```python
# lambda_handler.py
from src.agents import DataCollectionAgent

def lambda_handler(event, context):
    agent = DataCollectionAgent()
    tickers = event.get('tickers', ['SPY'])
    data = agent.execute(tickers=tickers, period='1mo')
    return {
        'statusCode': 200,
        'body': data.to_json()
    }
```

### Option 4: Scheduled Jobs (Cron/Airflow)

```bash
# crontab entry - run daily at 6 PM
0 18 * * * cd /path/to/pcrm-book && poetry run python scripts/daily_analysis.py
```

## Monitoring

### Logging

Configure centralized logging:

```python
import logging
from src.agents.config import AgentConfig

# Setup logging
AgentConfig.setup_logging()

# Use in agents
logger = logging.getLogger('agents.my_agent')
logger.info("Processing started")
```

### Log Aggregation

Options:
- **ELK Stack**: Elasticsearch, Logstash, Kibana
- **Splunk**: Enterprise log management
- **CloudWatch**: AWS native logging
- **Datadog**: Application monitoring

### Metrics

Track key metrics:
- Execution time
- Success/failure rates
- Data quality metrics
- API call counts
- Cache hit rates

```python
import time
from functools import wraps

def track_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        print(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper
```

### Health Checks

```python
# healthcheck.py
from src.agents import DataCollectionAgent

def health_check():
    """Basic health check."""
    try:
        agent = DataCollectionAgent()
        data = agent.execute(tickers='SPY', period='1d')
        return data is not None
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

if __name__ == "__main__":
    exit(0 if health_check() else 1)
```

## Performance Optimization

### Caching

Enable caching for frequently accessed data:

```python
from functools import lru_cache
import pandas as pd

@lru_cache(maxsize=128)
def get_cached_data(ticker, period):
    agent = DataCollectionAgent()
    return agent.execute(tickers=ticker, period=period)
```

### Parallel Processing

Use parallel processing for multiple assets:

```python
from concurrent.futures import ThreadPoolExecutor
from src.agents import DataCollectionAgent

def collect_data_parallel(tickers):
    agent = DataCollectionAgent()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(agent.execute, tickers=[ticker], period='1y')
            for ticker in tickers
        ]
        results = [f.result() for f in futures]
    return results
```

### Memory Management

For large datasets:

```python
# Process data in chunks
chunk_size = 1000
for i in range(0, len(data), chunk_size):
    chunk = data[i:i+chunk_size]
    process_chunk(chunk)
```

### Database Integration

Store results in database for faster access:

```python
import sqlite3
import pandas as pd

def cache_to_db(data, table_name):
    conn = sqlite3.connect('agents_cache.db')
    data.to_sql(table_name, conn, if_exists='replace')
    conn.close()

def load_from_db(table_name):
    conn = sqlite3.connect('agents_cache.db')
    data = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return data
```

## Security Considerations

### API Keys and Secrets

Never commit secrets to version control:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')
```

### Data Encryption

Encrypt sensitive data:

```python
from cryptography.fernet import Fernet

# Generate key (do this once, store securely)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
encrypted = cipher.encrypt(b"sensitive data")

# Decrypt
decrypted = cipher.decrypt(encrypted)
```

### Access Control

Implement role-based access:

```python
from functools import wraps

def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            raise PermissionError("Authentication required")
        return func(*args, **kwargs)
    return wrapper

@require_auth
def run_analysis():
    # Protected function
    pass
```

### Rate Limiting

Prevent API abuse:

```python
from time import sleep
from functools import wraps

def rate_limit(calls_per_minute=60):
    min_interval = 60.0 / calls_per_minute
    def decorator(func):
        last_called = [0.0]
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                sleep(left_to_wait)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator
```

## Troubleshooting

### Common Issues

#### 1. Import Errors

```bash
# Ensure src is in Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/pcrm-book"

# Or use poetry
poetry run python your_script.py
```

#### 2. Data Collection Failures

```python
# Add retry logic
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def collect_data_with_retry(ticker):
    agent = DataCollectionAgent()
    return agent.execute(tickers=ticker, period='1y')
```

#### 3. Memory Issues

```python
import gc

# Explicit garbage collection
gc.collect()

# Monitor memory usage
import psutil
process = psutil.Process()
print(f"Memory: {process.memory_info().rss / 1024 / 1024:.2f} MB")
```

#### 4. Performance Issues

```python
# Profile your code
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here
agent.execute(tickers=['SPY'], period='5y')

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from src.agents import DataCollectionAgent
agent = DataCollectionAgent(log_level=logging.DEBUG)
```

### Support

For additional help:
- Check the [GitHub Issues](https://github.com/fortitudo-tech/pcrm-book/issues)
- Review the [main README](README.md)
- Consult the [agents README](src/agents/README.md)
- Visit the [Quantamental Investing Substack](https://antonvorobets.substack.com)

## Production Checklist

Before deploying to production:

- [ ] All tests passing
- [ ] Code coverage >80%
- [ ] Configuration validated
- [ ] Logging configured
- [ ] Monitoring setup
- [ ] Secrets secured
- [ ] Backup strategy in place
- [ ] Documentation updated
- [ ] Performance tested
- [ ] Security reviewed
- [ ] Error handling implemented
- [ ] Health checks configured

## Version History

- **v1.0.0** (2025-01): Initial production release with all agents
  - DataCollectionAgent
  - StatisticalAnalysisAgent
  - RiskAnalyticsAgent
  - MarketResearchAgent
  - BacktestingAgent

## License

GPL-3.0-or-later - See LICENSE file for details.
