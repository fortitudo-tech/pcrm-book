"""Tests for BacktestingAgent."""

import pytest
import pandas as pd
import numpy as np
from src.agents.backtesting_agent import BacktestingAgent


class TestBacktestingAgent:
    """Test cases for BacktestingAgent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        return BacktestingAgent()

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
    def equal_weights(self, sample_prices):
        """Create equal weight strategy."""
        n_assets = len(sample_prices.columns)
        return pd.DataFrame(
            1 / n_assets,
            index=sample_prices.index,
            columns=sample_prices.columns
        )

    def test_initialization(self, agent):
        """Test agent initialization."""
        assert agent.name == "BacktestingAgent"

    def test_execute_with_weights(self, agent, sample_prices, equal_weights):
        """Test executing backtest with weight DataFrame."""
        result = agent.execute(
            prices=sample_prices,
            strategy=equal_weights,
            initial_capital=100000
        )

        assert 'portfolio_value' in result
        assert 'returns' in result
        assert 'metrics' in result
        assert 'final_value' in result
        assert result['final_value'] > 0

    def test_run_backtest(self, agent, sample_prices, equal_weights):
        """Test running backtest."""
        result = agent.run_backtest(
            prices=sample_prices,
            weights=equal_weights,
            initial_capital=100000,
            commission=0.001,
            slippage=0.0005
        )

        assert 'portfolio_value' in result
        assert 'returns' in result
        assert 'gross_returns' in result
        assert 'transaction_costs' in result
        assert 'weights' in result
        assert 'metrics' in result

        # Transaction costs should be positive
        assert (result['transaction_costs'] >= 0).all()

        # Portfolio value should start at initial capital
        assert result['portfolio_value'].iloc[0] == 100000

    def test_calculate_performance_metrics(self, agent):
        """Test performance metrics calculation."""
        np.random.seed(42)
        returns = pd.Series(np.random.randn(252) * 0.01)
        portfolio_value = 100000 * (1 + returns).cumprod()

        metrics = agent.calculate_performance_metrics(returns, portfolio_value)

        assert 'total_return' in metrics
        assert 'annual_return' in metrics
        assert 'annual_volatility' in metrics
        assert 'sharpe_ratio' in metrics
        assert 'sortino_ratio' in metrics
        assert 'max_drawdown' in metrics
        assert 'calmar_ratio' in metrics
        assert 'win_rate' in metrics
        assert 'profit_factor' in metrics
        assert 'years' in metrics

        # Win rate should be between 0 and 1
        assert 0 <= metrics['win_rate'] <= 1

    def test_compare_strategies(self, agent, sample_prices, equal_weights):
        """Test comparing multiple strategies."""
        # Create a second strategy (70-30 split)
        strategy2 = pd.DataFrame(
            index=sample_prices.index,
            columns=sample_prices.columns
        )
        strategy2.iloc[:, 0] = 0.7
        strategy2.iloc[:, 1:] = 0.15

        strategies = {
            'Equal Weight': equal_weights,
            '70-30 Split': strategy2
        }

        result = agent.compare_strategies(
            prices=sample_prices,
            strategies=strategies,
            initial_capital=100000
        )

        assert 'individual_results' in result
        assert 'metrics_comparison' in result
        assert 'portfolio_values' in result

        assert 'Equal Weight' in result['individual_results']
        assert '70-30 Split' in result['individual_results']

        assert len(result['metrics_comparison']) == 2

    def test_walk_forward_analysis(self, agent, sample_prices):
        """Test walk-forward analysis."""
        def simple_strategy(prices, **kwargs):
            """Simple equal weight strategy."""
            n_assets = len(prices.columns)
            return pd.DataFrame(
                1 / n_assets,
                index=prices.index,
                columns=prices.columns
            )

        result = agent.walk_forward_analysis(
            prices=sample_prices,
            strategy=simple_strategy,
            train_period=60,
            test_period=20,
            initial_capital=100000
        )

        assert 'period_results' in result
        assert 'combined_returns' in result
        assert 'combined_portfolio' in result
        assert 'overall_metrics' in result
        assert 'num_periods' in result

        assert result['num_periods'] > 0

    def test_monte_carlo_simulation(self, agent):
        """Test Monte Carlo simulation."""
        np.random.seed(42)
        returns = pd.Series(np.random.randn(252) * 0.01)

        result = agent.monte_carlo_simulation(
            returns=returns,
            num_simulations=100,
            num_periods=252,
            initial_capital=100000
        )

        assert 'portfolio_paths' in result
        assert 'final_values' in result
        assert 'mean_final_value' in result
        assert 'percentiles' in result
        assert 'probability_of_loss' in result

        assert result['portfolio_paths'].shape == (100, 252)
        assert len(result['final_values']) == 100

        # Percentiles should be in order
        percentiles = result['percentiles']
        assert percentiles['5th'] <= percentiles['25th']
        assert percentiles['25th'] <= percentiles['50th']
        assert percentiles['50th'] <= percentiles['75th']
        assert percentiles['75th'] <= percentiles['95th']

    def test_generate_report(self, agent, sample_prices, equal_weights):
        """Test report generation."""
        result = agent.execute(
            prices=sample_prices,
            strategy=equal_weights,
            initial_capital=100000
        )

        report = agent.generate_report(result, "Test Strategy")

        assert isinstance(report, str)
        assert "Test Strategy" in report
        assert "Total Return" in report
        assert "Sharpe Ratio" in report
        assert "Maximum Drawdown" in report

    def test_rebalancing_frequencies(self, agent, sample_prices, equal_weights):
        """Test different rebalancing frequencies."""
        frequencies = ['daily', 'weekly', 'monthly']

        for freq in frequencies:
            result = agent.run_backtest(
                prices=sample_prices,
                weights=equal_weights,
                initial_capital=100000,
                rebalance_frequency=freq
            )

            assert 'portfolio_value' in result
            assert 'transaction_costs' in result

    def test_transaction_costs_impact(self, agent, sample_prices, equal_weights):
        """Test impact of transaction costs."""
        # Run without costs
        result_no_costs = agent.run_backtest(
            prices=sample_prices,
            weights=equal_weights,
            initial_capital=100000,
            commission=0.0,
            slippage=0.0
        )

        # Run with costs
        result_with_costs = agent.run_backtest(
            prices=sample_prices,
            weights=equal_weights,
            initial_capital=100000,
            commission=0.01,
            slippage=0.01
        )

        # Final value should be lower with costs
        assert (
            result_with_costs['final_value'] <=
            result_no_costs['final_value']
        )

    def test_validate_input(self, agent):
        """Test input validation."""
        assert agent.validate_input(pd.DataFrame()) is True
        assert agent.validate_input(None) is False
