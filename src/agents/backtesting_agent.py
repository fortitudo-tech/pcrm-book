"""
Backtesting Agent for strategy validation and performance analysis.

This agent provides comprehensive backtesting capabilities for trading
strategies, including performance metrics, transaction costs, and
portfolio rebalancing.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Callable, Any, Union
from datetime import datetime

from .base_agent import BaseAgent


class BacktestingAgent(BaseAgent):
    """
    Agent specialized in backtesting trading strategies.

    This agent can:
    - Backtest trading strategies
    - Calculate performance metrics
    - Account for transaction costs
    - Handle portfolio rebalancing
    - Generate performance reports
    - Compare multiple strategies
    """

    def __init__(self, **kwargs):
        """Initialize the Backtesting Agent."""
        super().__init__(
            name="BacktestingAgent",
            description="Backtests and validates trading strategies",
            **kwargs
        )

    def execute(
        self,
        prices: pd.DataFrame,
        strategy: Union[Callable, pd.DataFrame],
        initial_capital: float = 100000.0,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute backtest for a trading strategy.

        Args:
            prices: DataFrame with price data
            strategy: Strategy function or DataFrame with weights/positions
            initial_capital: Initial capital amount
            **kwargs: Additional backtesting parameters

        Returns:
            Dictionary with backtest results
        """
        self.logger.info("Running backtest")

        if not self.validate_input(prices):
            raise ValueError("Invalid price data")

        # Get strategy signals/weights
        if callable(strategy):
            weights = strategy(prices, **kwargs)
        else:
            weights = strategy

        # Run backtest
        results = self.run_backtest(
            prices=prices,
            weights=weights,
            initial_capital=initial_capital,
            **kwargs
        )

        self.logger.info("Backtest completed")
        return results

    def run_backtest(
        self,
        prices: pd.DataFrame,
        weights: pd.DataFrame,
        initial_capital: float = 100000.0,
        commission: float = 0.001,
        slippage: float = 0.0005,
        rebalance_frequency: str = 'daily'
    ) -> Dict[str, Any]:
        """
        Run comprehensive backtest.

        Args:
            prices: DataFrame with price data
            weights: DataFrame with portfolio weights
            initial_capital: Initial capital
            commission: Commission rate (e.g., 0.001 = 0.1%)
            slippage: Slippage rate
            rebalance_frequency: Rebalancing frequency ('daily', 'weekly', 'monthly')

        Returns:
            Dictionary with backtest results
        """
        self.logger.info("Executing backtest simulation")

        # Calculate returns
        returns = prices.pct_change()

        # Align weights and returns
        aligned_weights = weights.reindex(returns.index).fillna(0)

        # Portfolio returns (before costs)
        portfolio_returns = (aligned_weights.shift(1) * returns).sum(axis=1)

        # Calculate transaction costs
        weight_changes = aligned_weights.diff().abs()

        # Apply rebalancing frequency
        if rebalance_frequency == 'weekly':
            # Only rebalance on specific days
            rebalance_mask = pd.Series(False, index=weight_changes.index)
            rebalance_mask[::5] = True  # Simplified: every 5 days
            weight_changes = weight_changes * rebalance_mask.values.reshape(-1, 1)
        elif rebalance_frequency == 'monthly':
            rebalance_mask = pd.Series(False, index=weight_changes.index)
            rebalance_mask[::21] = True  # Simplified: every 21 days
            weight_changes = weight_changes * rebalance_mask.values.reshape(-1, 1)

        # Total transaction costs
        transaction_costs = weight_changes.sum(axis=1) * (commission + slippage)

        # Net portfolio returns (after costs)
        net_returns = portfolio_returns - transaction_costs

        # Calculate portfolio value
        portfolio_value = initial_capital * (1 + net_returns).cumprod()
        portfolio_value.iloc[0] = initial_capital

        # Calculate performance metrics
        metrics = self.calculate_performance_metrics(
            returns=net_returns,
            portfolio_value=portfolio_value
        )

        # Generate results
        results = {
            'portfolio_value': portfolio_value,
            'returns': net_returns,
            'gross_returns': portfolio_returns,
            'transaction_costs': transaction_costs,
            'weights': aligned_weights,
            'metrics': metrics,
            'final_value': portfolio_value.iloc[-1],
            'total_return': (portfolio_value.iloc[-1] / initial_capital) - 1
        }

        self.logger.info(f"Final portfolio value: ${results['final_value']:,.2f}")
        return results

    def calculate_performance_metrics(
        self,
        returns: pd.Series,
        portfolio_value: pd.Series,
        risk_free_rate: float = 0.0,
        periods_per_year: int = 252
    ) -> Dict[str, float]:
        """
        Calculate comprehensive performance metrics.

        Args:
            returns: Series of portfolio returns
            portfolio_value: Series of portfolio values
            risk_free_rate: Annual risk-free rate
            periods_per_year: Number of periods per year

        Returns:
            Dictionary with performance metrics
        """
        self.logger.info("Calculating performance metrics")

        # Basic statistics
        total_return = (portfolio_value.iloc[-1] / portfolio_value.iloc[0]) - 1
        total_days = len(returns)
        years = total_days / periods_per_year

        # Annualized metrics
        annual_return = (1 + total_return) ** (1 / years) - 1
        annual_volatility = returns.std() * np.sqrt(periods_per_year)

        # Risk-adjusted metrics
        excess_returns = returns - risk_free_rate / periods_per_year
        sharpe_ratio = (excess_returns.mean() / returns.std()) * np.sqrt(periods_per_year)

        # Downside metrics
        downside_returns = returns[returns < 0]
        sortino_ratio = (
            (excess_returns.mean() / downside_returns.std()) *
            np.sqrt(periods_per_year)
        ) if len(downside_returns) > 0 else np.nan

        # Drawdown analysis
        cumulative_returns = (1 + returns).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min()

        # Calmar ratio
        calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else np.nan

        # Win rate
        win_rate = (returns > 0).sum() / len(returns)

        # Profit factor
        gross_profits = returns[returns > 0].sum()
        gross_losses = abs(returns[returns < 0].sum())
        profit_factor = gross_profits / gross_losses if gross_losses != 0 else np.nan

        metrics = {
            'total_return': total_return,
            'annual_return': annual_return,
            'annual_volatility': annual_volatility,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'max_drawdown': max_drawdown,
            'calmar_ratio': calmar_ratio,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'total_trades': len(returns),
            'years': years
        }

        self.logger.info("Performance metrics calculated")
        return metrics

    def compare_strategies(
        self,
        prices: pd.DataFrame,
        strategies: Dict[str, Union[Callable, pd.DataFrame]],
        initial_capital: float = 100000.0,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Compare multiple strategies.

        Args:
            prices: DataFrame with price data
            strategies: Dictionary of strategy name -> strategy function/weights
            initial_capital: Initial capital
            **kwargs: Additional backtesting parameters

        Returns:
            Dictionary with comparison results
        """
        self.logger.info(f"Comparing {len(strategies)} strategies")

        results = {}
        all_metrics = []

        for name, strategy in strategies.items():
            self.logger.info(f"Testing strategy: {name}")

            # Run backtest for this strategy
            strategy_results = self.execute(
                prices=prices,
                strategy=strategy,
                initial_capital=initial_capital,
                **kwargs
            )

            results[name] = strategy_results

            # Collect metrics for comparison
            metrics_df = pd.Series(strategy_results['metrics'], name=name)
            all_metrics.append(metrics_df)

        # Create comparison DataFrame
        comparison = pd.DataFrame(all_metrics)

        # Add portfolio values for visualization
        portfolio_values = pd.DataFrame({
            name: results[name]['portfolio_value']
            for name in strategies.keys()
        })

        comparison_results = {
            'individual_results': results,
            'metrics_comparison': comparison,
            'portfolio_values': portfolio_values
        }

        self.logger.info("Strategy comparison completed")
        return comparison_results

    def walk_forward_analysis(
        self,
        prices: pd.DataFrame,
        strategy: Callable,
        train_period: int = 252,
        test_period: int = 63,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform walk-forward analysis.

        Args:
            prices: DataFrame with price data
            strategy: Strategy function
            train_period: Training period length
            test_period: Testing period length
            **kwargs: Additional parameters

        Returns:
            Dictionary with walk-forward results
        """
        self.logger.info("Performing walk-forward analysis")

        results = []
        total_periods = len(prices)
        current_position = train_period

        while current_position + test_period <= total_periods:
            # Define train and test windows
            train_start = current_position - train_period
            train_end = current_position
            test_end = current_position + test_period

            # Train data
            train_prices = prices.iloc[train_start:train_end]

            # Test data
            test_prices = prices.iloc[train_end:test_end]

            # Generate strategy on training data
            weights = strategy(train_prices, **kwargs)

            # Test on out-of-sample data
            test_results = self.run_backtest(
                prices=test_prices,
                weights=weights.reindex(test_prices.index).fillna(0),
                **kwargs
            )

            results.append({
                'train_period': (train_start, train_end),
                'test_period': (train_end, test_end),
                'metrics': test_results['metrics'],
                'returns': test_results['returns']
            })

            # Move forward
            current_position += test_period

        # Combine all test period results
        all_returns = pd.concat([r['returns'] for r in results])
        combined_portfolio = (1 + all_returns).cumprod() * kwargs.get('initial_capital', 100000)

        overall_metrics = self.calculate_performance_metrics(
            returns=all_returns,
            portfolio_value=combined_portfolio
        )

        walk_forward_results = {
            'period_results': results,
            'combined_returns': all_returns,
            'combined_portfolio': combined_portfolio,
            'overall_metrics': overall_metrics,
            'num_periods': len(results)
        }

        self.logger.info("Walk-forward analysis completed")
        return walk_forward_results

    def monte_carlo_simulation(
        self,
        returns: pd.Series,
        num_simulations: int = 1000,
        num_periods: int = 252,
        initial_capital: float = 100000.0
    ) -> Dict[str, Any]:
        """
        Perform Monte Carlo simulation of portfolio returns.

        Args:
            returns: Historical returns series
            num_simulations: Number of simulation paths
            num_periods: Number of periods to simulate
            initial_capital: Initial capital

        Returns:
            Dictionary with simulation results
        """
        self.logger.info(f"Running {num_simulations} Monte Carlo simulations")

        # Calculate historical statistics
        mean_return = returns.mean()
        std_return = returns.std()

        # Generate random returns
        simulated_returns = np.random.normal(
            mean_return,
            std_return,
            size=(num_simulations, num_periods)
        )

        # Calculate portfolio paths
        portfolio_paths = initial_capital * (1 + simulated_returns).cumprod(axis=1)

        # Calculate statistics
        final_values = portfolio_paths[:, -1]
        percentiles = np.percentile(final_values, [5, 25, 50, 75, 95])

        results = {
            'portfolio_paths': portfolio_paths,
            'final_values': final_values,
            'mean_final_value': final_values.mean(),
            'percentiles': {
                '5th': percentiles[0],
                '25th': percentiles[1],
                '50th': percentiles[2],
                '75th': percentiles[3],
                '95th': percentiles[4]
            },
            'probability_of_loss': (final_values < initial_capital).sum() / num_simulations
        }

        self.logger.info("Monte Carlo simulation completed")
        return results

    def generate_report(
        self,
        backtest_results: Dict[str, Any],
        strategy_name: str = "Strategy"
    ) -> str:
        """
        Generate a formatted backtest report.

        Args:
            backtest_results: Results from backtest
            strategy_name: Name of the strategy

        Returns:
            Formatted report string
        """
        self.logger.info("Generating backtest report")

        metrics = backtest_results['metrics']

        report = f"""
{'='*60}
Backtest Report: {strategy_name}
{'='*60}

Performance Metrics:
------------------------------------------------------------
Total Return:        {metrics['total_return']*100:>10.2f}%
Annual Return:       {metrics['annual_return']*100:>10.2f}%
Annual Volatility:   {metrics['annual_volatility']*100:>10.2f}%

Risk-Adjusted Metrics:
------------------------------------------------------------
Sharpe Ratio:        {metrics['sharpe_ratio']:>10.2f}
Sortino Ratio:       {metrics['sortino_ratio']:>10.2f}
Calmar Ratio:        {metrics['calmar_ratio']:>10.2f}

Risk Metrics:
------------------------------------------------------------
Maximum Drawdown:    {metrics['max_drawdown']*100:>10.2f}%

Trading Statistics:
------------------------------------------------------------
Win Rate:            {metrics['win_rate']*100:>10.2f}%
Profit Factor:       {metrics['profit_factor']:>10.2f}
Total Trades:        {metrics['total_trades']:>10.0f}

Portfolio Statistics:
------------------------------------------------------------
Final Value:         ${backtest_results['final_value']:>15,.2f}
Years:               {metrics['years']:>10.2f}

{'='*60}
"""

        return report
