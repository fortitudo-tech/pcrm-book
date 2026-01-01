# Research Agents for Financial Analysis

This module provides a collection of AI-powered research agents designed for financial data analysis, portfolio management, and quantitative research.

## Overview

The agents module contains specialized research agents that automate various aspects of financial analysis:

- **DataCollectionAgent**: Collects and manages financial market data
- **StatisticalAnalysisAgent**: Performs statistical analysis on financial data
- **RiskAnalyticsAgent**: Analyzes portfolio risk and computes risk metrics
- **MarketResearchAgent**: Conducts market research and trend analysis
- **BacktestingAgent**: Backtests and validates trading strategies

## Installation

The agents are part of the `pcrm-book` package. Ensure you have all dependencies installed:

```bash
conda env create -f environment.yml
conda activate pcrm-book
```

Or using poetry:

```bash
poetry install
```

## Quick Start

### Data Collection Agent

Collect financial data from Yahoo Finance:

```python
from src.agents import DataCollectionAgent

# Initialize the agent
agent = DataCollectionAgent()

# Download price data
prices = agent.execute(
    tickers=['AAPL', 'MSFT', 'GOOGL'],
    period='1y',
    interval='1d'
)

# Get ticker information
info = agent.get_ticker_info('AAPL')

# Get dividends
dividends = agent.get_dividends('AAPL')
```

### Statistical Analysis Agent

Perform statistical analysis on financial data:

```python
from src.agents import StatisticalAnalysisAgent

# Initialize the agent
agent = StatisticalAnalysisAgent()

# Descriptive statistics
stats = agent.execute(returns, analysis_type='descriptive')

# Correlation analysis
corr = agent.execute(returns, analysis_type='correlation')

# Distribution analysis
dist = agent.execute(returns, analysis_type='distribution')

# Detect outliers
outliers = agent.outlier_detection(returns, method='iqr')
```

### Risk Analytics Agent

Calculate risk metrics and analyze portfolio risk:

```python
from src.agents import RiskAnalyticsAgent

# Initialize the agent
agent = RiskAnalyticsAgent()

# Calculate VaR
var = agent.value_at_risk(returns, confidence_level=0.95)

# Calculate CVaR
cvar = agent.conditional_value_at_risk(returns, confidence_level=0.95)

# Comprehensive risk analysis
risk_analysis = agent.comprehensive_risk_analysis(
    returns,
    confidence_level=0.95,
    risk_free_rate=0.02
)

# Calculate Sharpe ratio
sharpe = agent.sharpe_ratio(returns, risk_free_rate=0.02)
```

### Market Research Agent

Analyze market trends and technical indicators:

```python
from src.agents import MarketResearchAgent

# Initialize the agent
agent = MarketResearchAgent()

# Trend analysis
trends = agent.trend_analysis(prices, windows=[20, 50, 200])

# Momentum indicators
momentum = agent.momentum_analysis(prices, period=14)

# Technical indicators
indicators = agent.technical_indicators(prices)

# Regime detection
regimes = agent.regime_detection(returns, method='volatility')

# Market summary
summary = agent.market_summary(prices, returns)
```

### Backtesting Agent

Backtest trading strategies:

```python
from src.agents import BacktestingAgent
import pandas as pd

# Initialize the agent
agent = BacktestingAgent()

# Define strategy weights (example: equal weight)
weights = pd.DataFrame(
    1/len(prices.columns),
    index=prices.index,
    columns=prices.columns
)

# Run backtest
results = agent.execute(
    prices=prices,
    strategy=weights,
    initial_capital=100000,
    commission=0.001
)

# Generate report
report = agent.generate_report(results, strategy_name="Equal Weight")
print(report)

# Compare strategies
strategies = {
    'Equal Weight': weights,
    'Market Cap Weight': market_cap_weights,
}
comparison = agent.compare_strategies(prices, strategies)
```

## Agent Details

### DataCollectionAgent

**Capabilities:**
- Download historical price data from Yahoo Finance
- Retrieve ticker information and fundamentals
- Collect dividend and split history
- Get financial statements (income, balance sheet, cash flow)
- Calculate returns (simple or log)
- Validate data quality

**Key Methods:**
- `execute()`: Main method to download price data
- `get_ticker_info()`: Get detailed ticker information
- `get_dividends()`: Retrieve dividend history
- `get_splits()`: Get stock split history
- `get_financial_statements()`: Fetch financial statements
- `calculate_returns()`: Calculate returns from prices
- `validate_data()`: Validate data quality

### StatisticalAnalysisAgent

**Capabilities:**
- Compute descriptive statistics (mean, median, std, skewness, kurtosis)
- Perform correlation and covariance analysis
- Conduct hypothesis testing (t-test, Mann-Whitney, KS test)
- Analyze distributions and test for normality
- Perform time series analysis (stationarity tests, autocorrelation)
- Detect outliers using multiple methods

**Key Methods:**
- `execute()`: Main method for statistical analysis
- `descriptive_statistics()`: Comprehensive descriptive stats
- `correlation_analysis()`: Correlation and covariance
- `distribution_analysis()`: Distribution properties and tests
- `timeseries_analysis()`: Time series specific analysis
- `outlier_detection()`: Detect outliers (IQR, z-score, modified z-score)
- `hypothesis_test()`: Conduct hypothesis tests

### RiskAnalyticsAgent

**Capabilities:**
- Calculate Value at Risk (VaR) using multiple methods
- Compute Conditional Value at Risk (CVaR/Expected Shortfall)
- Analyze volatility (historical and implied)
- Calculate maximum drawdown
- Compute risk-adjusted performance metrics (Sharpe, Sortino, Calmar)
- Perform stress testing and scenario analysis

**Key Methods:**
- `execute()`: Main method for risk analysis
- `value_at_risk()`: Calculate VaR (historical, parametric, Cornish-Fisher)
- `conditional_value_at_risk()`: Calculate CVaR
- `calculate_volatility()`: Compute volatility
- `maximum_drawdown()`: Calculate max drawdown
- `sharpe_ratio()`: Sharpe ratio
- `sortino_ratio()`: Sortino ratio
- `calmar_ratio()`: Calmar ratio
- `comprehensive_risk_analysis()`: All risk metrics
- `stress_test()`: Stress testing with scenarios

### MarketResearchAgent

**Capabilities:**
- Analyze price trends using moving averages
- Calculate momentum indicators (RSI, MACD, ROC)
- Compute volatility indicators (Bollinger Bands, ATR)
- Detect market regimes (volatility, correlation)
- Identify support and resistance levels
- Perform comparative analysis across assets
- Generate market summaries

**Key Methods:**
- `execute()`: Main method for market research
- `trend_analysis()`: Trend analysis with moving averages
- `momentum_analysis()`: Momentum indicators
- `volatility_indicators()`: Volatility-based indicators
- `technical_indicators()`: Comprehensive technical analysis
- `regime_detection()`: Market regime detection
- `support_resistance()`: Support/resistance levels
- `comparative_analysis()`: Cross-asset comparison
- `market_summary()`: Comprehensive market summary

### BacktestingAgent

**Capabilities:**
- Backtest trading strategies with transaction costs
- Calculate comprehensive performance metrics
- Handle portfolio rebalancing at different frequencies
- Compare multiple strategies
- Perform walk-forward analysis
- Run Monte Carlo simulations
- Generate detailed performance reports

**Key Methods:**
- `execute()`: Main method to run backtest
- `run_backtest()`: Comprehensive backtest with costs
- `calculate_performance_metrics()`: Performance metrics
- `compare_strategies()`: Compare multiple strategies
- `walk_forward_analysis()`: Walk-forward validation
- `monte_carlo_simulation()`: Monte Carlo simulation
- `generate_report()`: Generate formatted report

## Advanced Usage

### Combining Multiple Agents

Agents can be combined to create comprehensive analysis workflows:

```python
from src.agents import (
    DataCollectionAgent,
    StatisticalAnalysisAgent,
    RiskAnalyticsAgent,
    MarketResearchAgent,
    BacktestingAgent
)

# 1. Collect data
data_agent = DataCollectionAgent()
prices = data_agent.execute(['SPY', 'TLT', 'GLD'], period='5y')

# 2. Calculate returns
returns = data_agent.calculate_returns(prices['Adj Close'])

# 3. Statistical analysis
stats_agent = StatisticalAnalysisAgent()
correlation = stats_agent.correlation_analysis(returns)

# 4. Risk analysis
risk_agent = RiskAnalyticsAgent()
risk_metrics = risk_agent.comprehensive_risk_analysis(returns)

# 5. Market research
market_agent = MarketResearchAgent()
trends = market_agent.trend_analysis(prices['Adj Close'])
momentum = market_agent.momentum_analysis(prices['Adj Close'])

# 6. Backtest strategy
backtest_agent = BacktestingAgent()
# Define your strategy weights here
results = backtest_agent.execute(prices['Adj Close'], strategy_weights)
```

### Custom Strategy Backtesting

Create custom strategies and backtest them:

```python
def momentum_strategy(prices, lookback=60, top_n=2):
    """Select top N assets based on momentum."""
    returns = prices.pct_change(lookback)
    weights = pd.DataFrame(0, index=prices.index, columns=prices.columns)

    for date in weights.index[lookback:]:
        # Get momentum for this date
        mom = returns.loc[date]
        # Select top N
        top_assets = mom.nlargest(top_n).index
        # Equal weight
        weights.loc[date, top_assets] = 1 / top_n

    return weights

# Backtest the strategy
backtest_agent = BacktestingAgent()
results = backtest_agent.execute(
    prices=prices['Adj Close'],
    strategy=momentum_strategy,
    initial_capital=100000,
    commission=0.001,
    lookback=60,
    top_n=2
)

print(backtest_agent.generate_report(results, "Momentum Strategy"))
```

## Integration with Book Examples

These agents complement the Portfolio Construction and Risk Management book examples:

- **Chapter 1**: Use `MarketResearchAgent` for market regime analysis
- **Chapter 2**: Use `StatisticalAnalysisAgent` for distribution analysis
- **Chapter 3**: Use `RiskAnalyticsAgent` for VaR and CVaR calculations
- **Chapter 4**: Use `DataCollectionAgent` for data gathering
- **Chapter 5**: Use `BacktestingAgent` for portfolio optimization validation
- **Chapter 6**: Combine all agents for comprehensive portfolio analysis
- **Chapter 7**: Use agents for real-world case studies

## Best Practices

1. **Data Quality**: Always validate data using `DataCollectionAgent.validate_data()`
2. **Risk Management**: Use multiple risk metrics, not just one
3. **Backtesting**: Account for transaction costs and use walk-forward analysis
4. **Statistical Significance**: Check p-values when making inferences
5. **Regime Awareness**: Consider market regimes in your analysis
6. **Diversification**: Analyze correlations before portfolio construction

## Logging

All agents support logging. You can configure logging level when initializing:

```python
import logging

agent = DataCollectionAgent(log_level=logging.DEBUG)
```

Or configure logging globally:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Performance Considerations

- **Data Caching**: `DataCollectionAgent` includes basic caching
- **Vectorization**: All calculations use NumPy/Pandas vectorized operations
- **Memory**: Be mindful of memory when using large datasets or Monte Carlo simulations
- **Parallel Processing**: For multiple backtests, consider using parallel processing

## Contributing

Contributions to enhance these agents are welcome. Please follow the existing code style and add appropriate tests.

## License

This code is licensed under GPL-3.0-or-later, consistent with the pcrm-book repository.

## Support

For questions or issues:
- Check the main repository README
- Review the book chapters
- Post in the community Discussions forum
- Visit the Quantamental Investing Substack publication

## Changelog

### Version 1.0.0
- Initial release with 5 research agents
- Comprehensive data collection capabilities
- Advanced statistical analysis
- Risk analytics with VaR/CVaR
- Market research and technical analysis
- Backtesting framework with transaction costs
