"""Tests for MarketResearchAgent."""

import pytest
import pandas as pd
import numpy as np
from src.agents.market_research_agent import MarketResearchAgent


class TestMarketResearchAgent:
    """Test cases for MarketResearchAgent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        return MarketResearchAgent()

    @pytest.fixture
    def sample_prices(self):
        """Create sample price data."""
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=252, freq='D')
        data = {
            'Asset1': np.random.randn(252).cumsum() + 100,
            'Asset2': np.random.randn(252).cumsum() + 200,
            'Asset3': np.random.randn(252).cumsum() + 150
        }
        return pd.DataFrame(data, index=dates)

    @pytest.fixture
    def sample_returns(self, sample_prices):
        """Create sample returns from prices."""
        return sample_prices.pct_change().dropna()

    def test_initialization(self, agent):
        """Test agent initialization."""
        assert agent.name == "MarketResearchAgent"

    def test_execute_trend(self, agent, sample_prices):
        """Test executing trend analysis."""
        result = agent.execute(sample_prices, analysis_type='trend')

        assert 'SMA_20' in result
        assert 'trend_signal' in result
        assert isinstance(result['SMA_20'], pd.DataFrame)

    def test_execute_momentum(self, agent, sample_prices):
        """Test executing momentum analysis."""
        result = agent.execute(sample_prices, analysis_type='momentum')

        assert 'ROC' in result
        assert 'RSI' in result
        assert 'MACD' in result

    def test_execute_regime(self, agent, sample_returns):
        """Test executing regime detection."""
        result = agent.execute(sample_returns, analysis_type='regime')

        assert 'regime' in result
        assert 'volatility' in result

    def test_execute_technical(self, agent, sample_prices):
        """Test executing technical indicators."""
        result = agent.execute(sample_prices, analysis_type='technical')

        assert 'trend' in result
        assert 'momentum' in result
        assert 'volatility' in result

    def test_execute_invalid_type(self, agent, sample_prices):
        """Test invalid analysis type."""
        with pytest.raises(ValueError):
            agent.execute(sample_prices, analysis_type='invalid')

    def test_trend_analysis(self, agent, sample_prices):
        """Test trend analysis."""
        result = agent.trend_analysis(sample_prices, windows=[20, 50])

        assert 'SMA_20' in result
        assert 'SMA_50' in result
        assert 'trend_signal' in result
        assert 'trend_strength' in result
        assert result['SMA_20'].shape == sample_prices.shape

    def test_momentum_analysis(self, agent, sample_prices):
        """Test momentum analysis."""
        result = agent.momentum_analysis(sample_prices, period=14)

        assert 'ROC' in result
        assert 'RSI' in result
        assert 'MACD' in result
        assert 'MACD_signal' in result
        assert 'MACD_histogram' in result

        # RSI should be between 0 and 100
        rsi_values = result['RSI'].dropna()
        assert all((rsi_values >= 0).all())
        assert all((rsi_values <= 100).all())

    def test_volatility_indicators(self, agent, sample_prices):
        """Test volatility indicators."""
        result = agent.volatility_indicators(sample_prices, window=20)

        assert 'BB_middle' in result
        assert 'BB_upper' in result
        assert 'BB_lower' in result
        assert 'BB_width' in result
        assert 'ATR' in result

        # Upper band should be above lower band
        for col in sample_prices.columns:
            valid_data = (
                ~result['BB_upper'][col].isna() &
                ~result['BB_lower'][col].isna()
            )
            assert all(
                result['BB_upper'][col][valid_data] >=
                result['BB_lower'][col][valid_data]
            )

    def test_technical_indicators(self, agent, sample_prices):
        """Test comprehensive technical indicators."""
        result = agent.technical_indicators(sample_prices)

        assert 'trend' in result
        assert 'momentum' in result
        assert 'volatility' in result

    def test_regime_detection_volatility(self, agent, sample_returns):
        """Test volatility-based regime detection."""
        result = agent.regime_detection(
            sample_returns,
            method='volatility',
            window=60
        )

        assert 'regime' in result
        assert 'volatility' in result
        assert isinstance(result['regime'], pd.DataFrame)

    def test_regime_detection_correlation(self, agent, sample_returns):
        """Test correlation-based regime detection."""
        result = agent.regime_detection(
            sample_returns,
            method='correlation',
            window=60
        )

        assert 'regime' in result
        assert 'correlation' in result

    def test_regime_detection_invalid_method(self, agent, sample_returns):
        """Test invalid regime detection method."""
        with pytest.raises(ValueError):
            agent.regime_detection(sample_returns, method='invalid')

    def test_support_resistance(self, agent, sample_prices):
        """Test support and resistance level identification."""
        result = agent.support_resistance(
            sample_prices['Asset1'],
            window=20,
            num_levels=3
        )

        assert 'resistance' in result
        assert 'support' in result
        assert 'current_price' in result
        assert len(result['resistance']) <= 3
        assert len(result['support']) <= 3

    def test_comparative_analysis(self, agent, sample_prices):
        """Test comparative analysis."""
        result = agent.comparative_analysis(sample_prices)

        assert 'correlation' in result
        assert 'normalized_prices' in result
        assert 'performance_rank' in result

    def test_comparative_analysis_with_benchmark(self, agent, sample_prices):
        """Test comparative analysis with benchmark."""
        benchmark = sample_prices['Asset1']
        result = agent.comparative_analysis(sample_prices, benchmark=benchmark)

        assert 'relative_returns' in result
        assert 'relative_performance' in result
        assert 'correlation' in result

    def test_market_summary(self, agent, sample_prices, sample_returns):
        """Test market summary generation."""
        result = agent.market_summary(sample_prices, sample_returns)

        assert 'latest_prices' in result
        assert 'price_change_1d' in result
        assert 'volatility_20d' in result
        assert 'current_trend' in result

        assert len(result['latest_prices']) == 3

    def test_market_summary_without_returns(self, agent, sample_prices):
        """Test market summary without providing returns."""
        result = agent.market_summary(sample_prices)

        assert 'latest_prices' in result
        assert 'price_change_1d' in result
