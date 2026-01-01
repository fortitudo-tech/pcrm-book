"""Tests for RiskAnalyticsAgent."""

import pytest
import pandas as pd
import numpy as np
from src.agents.risk_analytics_agent import RiskAnalyticsAgent


class TestRiskAnalyticsAgent:
    """Test cases for RiskAnalyticsAgent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        return RiskAnalyticsAgent()

    @pytest.fixture
    def sample_returns(self):
        """Create sample returns data."""
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=252, freq='D')
        data = {
            'Asset1': np.random.randn(252) * 0.01 + 0.0003,
            'Asset2': np.random.randn(252) * 0.015 + 0.0004,
            'Asset3': np.random.randn(252) * 0.02 + 0.0002
        }
        return pd.DataFrame(data, index=dates)

    def test_initialization(self, agent):
        """Test agent initialization."""
        assert agent.name == "RiskAnalyticsAgent"

    def test_execute_var(self, agent, sample_returns):
        """Test executing VaR calculation."""
        result = agent.execute(sample_returns, metric='var')

        assert isinstance(result, pd.Series)
        assert len(result) == 3

    def test_execute_cvar(self, agent, sample_returns):
        """Test executing CVaR calculation."""
        result = agent.execute(sample_returns, metric='cvar')

        assert isinstance(result, pd.Series)
        assert len(result) == 3

    def test_execute_volatility(self, agent, sample_returns):
        """Test executing volatility calculation."""
        result = agent.execute(sample_returns, metric='volatility')

        assert isinstance(result, pd.Series)
        assert all(result > 0)

    def test_execute_sharpe(self, agent, sample_returns):
        """Test executing Sharpe ratio calculation."""
        result = agent.execute(sample_returns, metric='sharpe')

        assert isinstance(result, pd.Series)

    def test_execute_all(self, agent, sample_returns):
        """Test executing comprehensive risk analysis."""
        result = agent.execute(sample_returns, metric='all')

        assert isinstance(result, dict)
        assert 'return_metrics' in result
        assert 'risk_metrics' in result
        assert 'performance_metrics' in result

    def test_value_at_risk_historical(self, agent, sample_returns):
        """Test historical VaR calculation."""
        var = agent.value_at_risk(
            sample_returns,
            confidence_level=0.95,
            method='historical'
        )

        assert isinstance(var, pd.Series)
        assert len(var) == 3
        # VaR should be negative
        assert all(var < 0)

    def test_value_at_risk_parametric(self, agent, sample_returns):
        """Test parametric VaR calculation."""
        var = agent.value_at_risk(
            sample_returns,
            confidence_level=0.95,
            method='parametric'
        )

        assert isinstance(var, pd.Series)
        assert len(var) == 3

    def test_value_at_risk_cornish_fisher(self, agent, sample_returns):
        """Test Cornish-Fisher VaR calculation."""
        var = agent.value_at_risk(
            sample_returns,
            confidence_level=0.95,
            method='cornish_fisher'
        )

        assert isinstance(var, pd.Series)
        assert len(var) == 3

    def test_value_at_risk_invalid_method(self, agent, sample_returns):
        """Test invalid VaR method."""
        with pytest.raises(ValueError):
            agent.value_at_risk(sample_returns, method='invalid')

    def test_conditional_value_at_risk_historical(self, agent, sample_returns):
        """Test historical CVaR calculation."""
        cvar = agent.conditional_value_at_risk(
            sample_returns,
            confidence_level=0.95,
            method='historical'
        )

        assert isinstance(cvar, pd.Series)
        # CVaR should be more negative than VaR
        var = agent.value_at_risk(sample_returns, confidence_level=0.95)
        assert all(cvar <= var)

    def test_conditional_value_at_risk_parametric(self, agent, sample_returns):
        """Test parametric CVaR calculation."""
        cvar = agent.conditional_value_at_risk(
            sample_returns,
            confidence_level=0.95,
            method='parametric'
        )

        assert isinstance(cvar, pd.Series)

    def test_calculate_volatility(self, agent, sample_returns):
        """Test volatility calculation."""
        vol = agent.calculate_volatility(sample_returns, annualize=True)

        assert isinstance(vol, pd.Series)
        assert all(vol > 0)

    def test_calculate_volatility_no_annualize(self, agent, sample_returns):
        """Test volatility without annualization."""
        vol = agent.calculate_volatility(sample_returns, annualize=False)

        assert isinstance(vol, pd.Series)
        # Non-annualized should be smaller
        vol_annual = agent.calculate_volatility(sample_returns, annualize=True)
        assert all(vol < vol_annual)

    def test_maximum_drawdown(self, agent, sample_returns):
        """Test maximum drawdown calculation."""
        max_dd = agent.maximum_drawdown(sample_returns)

        assert isinstance(max_dd, pd.Series)
        # Max drawdown should be negative
        assert all(max_dd <= 0)

    def test_sharpe_ratio(self, agent, sample_returns):
        """Test Sharpe ratio calculation."""
        sharpe = agent.sharpe_ratio(
            sample_returns,
            risk_free_rate=0.02,
            annualize=True
        )

        assert isinstance(sharpe, pd.Series)

    def test_sortino_ratio(self, agent, sample_returns):
        """Test Sortino ratio calculation."""
        sortino = agent.sortino_ratio(
            sample_returns,
            risk_free_rate=0.02,
            annualize=True
        )

        assert isinstance(sortino, pd.Series)

    def test_calmar_ratio(self, agent, sample_returns):
        """Test Calmar ratio calculation."""
        calmar = agent.calmar_ratio(sample_returns, annualize=True)

        assert isinstance(calmar, pd.Series)

    def test_comprehensive_risk_analysis(self, agent, sample_returns):
        """Test comprehensive risk analysis."""
        result = agent.comprehensive_risk_analysis(
            sample_returns,
            confidence_level=0.95,
            risk_free_rate=0.02
        )

        assert 'return_metrics' in result
        assert 'risk_metrics' in result
        assert 'performance_metrics' in result

        # Check return metrics
        assert 'mean' in result['return_metrics']
        assert 'median' in result['return_metrics']
        assert 'std' in result['return_metrics']

        # Check risk metrics
        assert 'var_95' in result['risk_metrics']
        assert 'cvar_95' in result['risk_metrics']
        assert 'volatility' in result['risk_metrics']
        assert 'max_drawdown' in result['risk_metrics']

        # Check performance metrics
        assert 'sharpe_ratio' in result['performance_metrics']
        assert 'sortino_ratio' in result['performance_metrics']
        assert 'calmar_ratio' in result['performance_metrics']

    def test_stress_test(self, agent, sample_returns):
        """Test stress testing."""
        scenario = {
            'Asset1': -0.10,
            'Asset2': -0.15,
            'Asset3': -0.05
        }

        stressed = agent.stress_test(sample_returns, scenario)

        assert isinstance(stressed, pd.DataFrame)
        assert stressed.shape == sample_returns.shape

    def test_single_asset_calculations(self, agent):
        """Test calculations on single asset (Series)."""
        np.random.seed(42)
        returns = pd.Series(np.random.randn(252) * 0.01)

        var = agent.value_at_risk(returns, confidence_level=0.95)
        assert isinstance(var, (float, np.floating))

        cvar = agent.conditional_value_at_risk(returns, confidence_level=0.95)
        assert isinstance(cvar, (float, np.floating))

        sharpe = agent.sharpe_ratio(returns)
        assert isinstance(sharpe, (float, np.floating))
