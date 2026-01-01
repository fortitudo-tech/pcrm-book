"""
Risk Analytics Agent for portfolio risk assessment.

This agent performs comprehensive risk analysis including VaR, CVaR,
volatility analysis, drawdowns, and other risk metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
from scipy import stats

from .base_agent import BaseAgent


class RiskAnalyticsAgent(BaseAgent):
    """
    Agent specialized in portfolio risk analytics.

    This agent can:
    - Calculate Value at Risk (VaR)
    - Compute Conditional Value at Risk (CVaR)
    - Analyze volatility and correlations
    - Calculate maximum drawdown
    - Compute various risk-adjusted performance metrics
    - Perform stress testing and scenario analysis
    """

    def __init__(self, **kwargs):
        """Initialize the Risk Analytics Agent."""
        super().__init__(
            name="RiskAnalyticsAgent",
            description="Analyzes portfolio risk and computes risk metrics",
            **kwargs
        )

    def execute(
        self,
        returns: pd.DataFrame,
        metric: str = "var",
        **kwargs
    ) -> Union[float, pd.Series, Dict[str, Any]]:
        """
        Execute risk analysis on the provided returns.

        Args:
            returns: DataFrame of asset returns
            metric: Risk metric to calculate ('var', 'cvar', 'volatility',
                   'sharpe', 'all')
            **kwargs: Additional parameters for specific metrics

        Returns:
            Calculated risk metric(s)
        """
        self.logger.info(f"Calculating {metric}")

        if not self.validate_input(returns):
            raise ValueError("Invalid input data")

        if metric == "var":
            return self.value_at_risk(returns, **kwargs)
        elif metric == "cvar":
            return self.conditional_value_at_risk(returns, **kwargs)
        elif metric == "volatility":
            return self.calculate_volatility(returns, **kwargs)
        elif metric == "sharpe":
            return self.sharpe_ratio(returns, **kwargs)
        elif metric == "all":
            return self.comprehensive_risk_analysis(returns, **kwargs)
        else:
            raise ValueError(f"Unknown metric: {metric}")

    def value_at_risk(
        self,
        returns: Union[pd.Series, pd.DataFrame],
        confidence_level: float = 0.95,
        method: str = "historical"
    ) -> Union[float, pd.Series]:
        """
        Calculate Value at Risk (VaR).

        Args:
            returns: Return series or DataFrame
            confidence_level: Confidence level (default: 0.95)
            method: Calculation method ('historical', 'parametric', 'cornish_fisher')

        Returns:
            VaR value(s)
        """
        self.logger.info(f"Calculating VaR using {method} method")

        alpha = 1 - confidence_level

        if method == "historical":
            # Historical VaR
            var = returns.quantile(alpha, axis=0)

        elif method == "parametric":
            # Parametric VaR (assumes normal distribution)
            mean = returns.mean()
            std = returns.std()
            var = mean + std * stats.norm.ppf(alpha)

        elif method == "cornish_fisher":
            # Cornish-Fisher VaR (accounts for skewness and kurtosis)
            mean = returns.mean()
            std = returns.std()
            skew = returns.skew()
            kurt = returns.kurtosis()

            z = stats.norm.ppf(alpha)
            z_cf = (z +
                   (z**2 - 1) * skew / 6 +
                   (z**3 - 3*z) * kurt / 24 -
                   (2*z**3 - 5*z) * skew**2 / 36)

            var = mean + std * z_cf

        else:
            raise ValueError(f"Unknown method: {method}")

        self.logger.info("VaR calculation completed")
        return var

    def conditional_value_at_risk(
        self,
        returns: Union[pd.Series, pd.DataFrame],
        confidence_level: float = 0.95,
        method: str = "historical"
    ) -> Union[float, pd.Series]:
        """
        Calculate Conditional Value at Risk (CVaR/Expected Shortfall).

        Args:
            returns: Return series or DataFrame
            confidence_level: Confidence level (default: 0.95)
            method: Calculation method ('historical', 'parametric')

        Returns:
            CVaR value(s)
        """
        self.logger.info(f"Calculating CVaR using {method} method")

        alpha = 1 - confidence_level

        if method == "historical":
            # Historical CVaR
            if isinstance(returns, pd.DataFrame):
                cvar = returns.apply(
                    lambda x: x[x <= x.quantile(alpha)].mean()
                )
            else:
                var = returns.quantile(alpha)
                cvar = returns[returns <= var].mean()

        elif method == "parametric":
            # Parametric CVaR (assumes normal distribution)
            mean = returns.mean()
            std = returns.std()
            z = stats.norm.ppf(alpha)
            cvar = mean - std * stats.norm.pdf(z) / alpha

        else:
            raise ValueError(f"Unknown method: {method}")

        self.logger.info("CVaR calculation completed")
        return cvar

    def calculate_volatility(
        self,
        returns: Union[pd.Series, pd.DataFrame],
        annualize: bool = True,
        periods_per_year: int = 252
    ) -> Union[float, pd.Series]:
        """
        Calculate volatility (standard deviation of returns).

        Args:
            returns: Return series or DataFrame
            annualize: Whether to annualize the volatility
            periods_per_year: Number of periods per year (default: 252 for daily)

        Returns:
            Volatility value(s)
        """
        self.logger.info("Calculating volatility")

        vol = returns.std()

        if annualize:
            vol = vol * np.sqrt(periods_per_year)

        self.logger.info("Volatility calculation completed")
        return vol

    def maximum_drawdown(
        self,
        returns: Union[pd.Series, pd.DataFrame]
    ) -> Union[float, pd.Series]:
        """
        Calculate maximum drawdown.

        Args:
            returns: Return series or DataFrame

        Returns:
            Maximum drawdown value(s)
        """
        self.logger.info("Calculating maximum drawdown")

        # Calculate cumulative returns
        cum_returns = (1 + returns).cumprod()

        # Calculate running maximum
        running_max = cum_returns.expanding().max()

        # Calculate drawdown
        drawdown = (cum_returns - running_max) / running_max

        # Get maximum drawdown
        max_dd = drawdown.min()

        self.logger.info("Maximum drawdown calculation completed")
        return max_dd

    def sharpe_ratio(
        self,
        returns: Union[pd.Series, pd.DataFrame],
        risk_free_rate: float = 0.0,
        annualize: bool = True,
        periods_per_year: int = 252
    ) -> Union[float, pd.Series]:
        """
        Calculate Sharpe ratio.

        Args:
            returns: Return series or DataFrame
            risk_free_rate: Risk-free rate (default: 0.0)
            annualize: Whether to annualize the ratio
            periods_per_year: Number of periods per year

        Returns:
            Sharpe ratio value(s)
        """
        self.logger.info("Calculating Sharpe ratio")

        excess_returns = returns - risk_free_rate / periods_per_year
        sharpe = excess_returns.mean() / returns.std()

        if annualize:
            sharpe = sharpe * np.sqrt(periods_per_year)

        self.logger.info("Sharpe ratio calculation completed")
        return sharpe

    def sortino_ratio(
        self,
        returns: Union[pd.Series, pd.DataFrame],
        risk_free_rate: float = 0.0,
        annualize: bool = True,
        periods_per_year: int = 252
    ) -> Union[float, pd.Series]:
        """
        Calculate Sortino ratio (uses downside deviation).

        Args:
            returns: Return series or DataFrame
            risk_free_rate: Risk-free rate (default: 0.0)
            annualize: Whether to annualize the ratio
            periods_per_year: Number of periods per year

        Returns:
            Sortino ratio value(s)
        """
        self.logger.info("Calculating Sortino ratio")

        excess_returns = returns - risk_free_rate / periods_per_year

        # Calculate downside deviation
        downside_returns = excess_returns[excess_returns < 0]
        downside_std = downside_returns.std()

        sortino = excess_returns.mean() / downside_std

        if annualize:
            sortino = sortino * np.sqrt(periods_per_year)

        self.logger.info("Sortino ratio calculation completed")
        return sortino

    def calmar_ratio(
        self,
        returns: Union[pd.Series, pd.DataFrame],
        annualize: bool = True,
        periods_per_year: int = 252
    ) -> Union[float, pd.Series]:
        """
        Calculate Calmar ratio (return / max drawdown).

        Args:
            returns: Return series or DataFrame
            annualize: Whether to annualize the ratio
            periods_per_year: Number of periods per year

        Returns:
            Calmar ratio value(s)
        """
        self.logger.info("Calculating Calmar ratio")

        annual_return = returns.mean()
        if annualize:
            annual_return = annual_return * periods_per_year

        max_dd = abs(self.maximum_drawdown(returns))

        calmar = annual_return / max_dd

        self.logger.info("Calmar ratio calculation completed")
        return calmar

    def comprehensive_risk_analysis(
        self,
        returns: Union[pd.Series, pd.DataFrame],
        confidence_level: float = 0.95,
        risk_free_rate: float = 0.0,
        periods_per_year: int = 252
    ) -> Dict[str, Any]:
        """
        Perform comprehensive risk analysis.

        Args:
            returns: Return series or DataFrame
            confidence_level: Confidence level for VaR/CVaR
            risk_free_rate: Risk-free rate for Sharpe ratio
            periods_per_year: Number of periods per year

        Returns:
            Dictionary with all risk metrics
        """
        self.logger.info("Performing comprehensive risk analysis")

        results = {
            'return_metrics': {
                'mean': returns.mean() * periods_per_year,
                'median': returns.median() * periods_per_year,
                'std': returns.std() * np.sqrt(periods_per_year)
            },
            'risk_metrics': {
                'var_95': self.value_at_risk(returns, confidence_level),
                'cvar_95': self.conditional_value_at_risk(returns, confidence_level),
                'volatility': self.calculate_volatility(returns, periods_per_year=periods_per_year),
                'max_drawdown': self.maximum_drawdown(returns)
            },
            'performance_metrics': {
                'sharpe_ratio': self.sharpe_ratio(
                    returns, risk_free_rate, periods_per_year=periods_per_year
                ),
                'sortino_ratio': self.sortino_ratio(
                    returns, risk_free_rate, periods_per_year=periods_per_year
                ),
                'calmar_ratio': self.calmar_ratio(returns, periods_per_year=periods_per_year)
            }
        }

        self.logger.info("Comprehensive risk analysis completed")
        return results

    def stress_test(
        self,
        returns: pd.DataFrame,
        scenario: Dict[str, float]
    ) -> pd.Series:
        """
        Perform stress testing with custom scenarios.

        Args:
            returns: DataFrame of asset returns
            scenario: Dictionary mapping asset names to scenario returns

        Returns:
            Series with stressed returns
        """
        self.logger.info("Performing stress test")

        stressed_returns = returns.copy()

        for asset, shock in scenario.items():
            if asset in stressed_returns.columns:
                stressed_returns[asset] = stressed_returns[asset] + shock

        self.logger.info("Stress test completed")
        return stressed_returns
