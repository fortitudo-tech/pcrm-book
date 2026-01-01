"""Tests for DataCollectionAgent."""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from src.agents.data_collection_agent import DataCollectionAgent


class TestDataCollectionAgent:
    """Test cases for DataCollectionAgent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        return DataCollectionAgent()

    @pytest.fixture
    def sample_prices(self):
        """Create sample price data."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        data = {
            'AAPL': np.random.randn(100).cumsum() + 100,
            'MSFT': np.random.randn(100).cumsum() + 200,
        }
        return pd.DataFrame(data, index=dates)

    def test_initialization(self, agent):
        """Test agent initialization."""
        assert agent.name == "DataCollectionAgent"
        assert agent.cache == {}

    @patch('src.agents.data_collection_agent.yf.download')
    def test_execute_single_ticker(self, mock_download, agent, sample_prices):
        """Test downloading data for single ticker."""
        mock_download.return_value = sample_prices

        result = agent.execute(tickers='AAPL', period='1y')

        assert result is not None
        mock_download.assert_called_once()

    @patch('src.agents.data_collection_agent.yf.download')
    def test_execute_multiple_tickers(self, mock_download, agent, sample_prices):
        """Test downloading data for multiple tickers."""
        mock_download.return_value = sample_prices

        result = agent.execute(tickers=['AAPL', 'MSFT'], period='1y')

        assert result is not None
        mock_download.assert_called_once()

    @patch('src.agents.data_collection_agent.yf.Ticker')
    def test_get_ticker_info(self, mock_ticker, agent):
        """Test getting ticker information."""
        mock_ticker_instance = Mock()
        mock_ticker_instance.info = {'symbol': 'AAPL', 'name': 'Apple Inc.'}
        mock_ticker.return_value = mock_ticker_instance

        result = agent.get_ticker_info('AAPL')

        assert result['symbol'] == 'AAPL'
        assert result['name'] == 'Apple Inc.'

    @patch('src.agents.data_collection_agent.yf.Ticker')
    def test_get_dividends(self, mock_ticker, agent):
        """Test getting dividend data."""
        mock_ticker_instance = Mock()
        dates = pd.date_range('2023-01-01', periods=4, freq='Q')
        mock_ticker_instance.dividends = pd.Series([0.22, 0.23, 0.24, 0.24], index=dates)
        mock_ticker.return_value = mock_ticker_instance

        result = agent.get_dividends('AAPL')

        assert len(result) == 4
        assert isinstance(result, pd.Series)

    @patch('src.agents.data_collection_agent.yf.Ticker')
    def test_get_splits(self, mock_ticker, agent):
        """Test getting stock split data."""
        mock_ticker_instance = Mock()
        dates = pd.date_range('2020-01-01', periods=2, freq='Y')
        mock_ticker_instance.splits = pd.Series([4.0, 2.0], index=dates)
        mock_ticker.return_value = mock_ticker_instance

        result = agent.get_splits('AAPL')

        assert len(result) == 2
        assert isinstance(result, pd.Series)

    @patch('src.agents.data_collection_agent.yf.Ticker')
    def test_get_financial_statements(self, mock_ticker, agent):
        """Test getting financial statements."""
        mock_ticker_instance = Mock()
        mock_ticker_instance.financials = pd.DataFrame({'Revenue': [100, 200]})
        mock_ticker.return_value = mock_ticker_instance

        result = agent.get_financial_statements('AAPL', statement_type='income')

        assert isinstance(result, pd.DataFrame)
        assert 'Revenue' in result.index

    def test_calculate_returns_simple(self, agent, sample_prices):
        """Test calculating simple returns."""
        returns = agent.calculate_returns(sample_prices, method='simple')

        assert isinstance(returns, pd.DataFrame)
        assert returns.shape[0] == sample_prices.shape[0]
        # First row should be NaN
        assert pd.isna(returns.iloc[0]).all()

    def test_calculate_returns_log(self, agent, sample_prices):
        """Test calculating log returns."""
        returns = agent.calculate_returns(sample_prices, method='log')

        assert isinstance(returns, pd.DataFrame)
        assert returns.shape[0] == sample_prices.shape[0]

    def test_calculate_returns_invalid_method(self, agent, sample_prices):
        """Test invalid return calculation method."""
        with pytest.raises(ValueError):
            agent.calculate_returns(sample_prices, method='invalid')

    def test_validate_data(self, agent, sample_prices):
        """Test data validation."""
        result = agent.validate_data(sample_prices)

        assert 'total_rows' in result
        assert 'missing_values' in result
        assert 'date_range' in result
        assert 'columns' in result
        assert 'duplicates' in result
        assert result['total_rows'] == len(sample_prices)

    def test_validate_data_with_missing(self, agent):
        """Test validation with missing values."""
        data = pd.DataFrame({
            'A': [1, np.nan, 3],
            'B': [4, 5, np.nan]
        })

        result = agent.validate_data(data)

        assert result['missing_values']['A'] == 1
        assert result['missing_values']['B'] == 1

    @patch('src.agents.data_collection_agent.yf.download')
    def test_execute_error_handling(self, mock_download, agent):
        """Test error handling during data download."""
        mock_download.side_effect = Exception("Network error")

        with pytest.raises(Exception):
            agent.execute(tickers='AAPL', period='1y')
