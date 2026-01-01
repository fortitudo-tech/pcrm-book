"""
Market Research Agent for financial market analysis.

This agent performs market research including trend analysis, momentum
indicators, technical analysis, and market regime detection.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta

from .base_agent import BaseAgent


class MarketResearchAgent(BaseAgent):
    """
    Agent specialized in market research and analysis.

    This agent can:
    - Analyze price trends and momentum
    - Calculate technical indicators
    - Detect market regimes and structural breaks
    - Identify support and resistance levels
    - Analyze market microstructure
    - Perform comparative analysis across assets
    """

    def __init__(self, **kwargs):
        """Initialize the Market Research Agent."""
        super().__init__(
            name="MarketResearchAgent",
            description="Performs market research and trend analysis",
            **kwargs
        )

    def execute(
        self,
        data: pd.DataFrame,
        analysis_type: str = "trend",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute market research analysis.

        Args:
            data: DataFrame with price data
            analysis_type: Type of analysis ('trend', 'momentum', 'regime',
                          'technical')
            **kwargs: Additional parameters

        Returns:
            Dictionary with analysis results
        """
        self.logger.info(f"Performing {analysis_type} analysis")

        if not self.validate_input(data):
            raise ValueError("Invalid input data")

        if analysis_type == "trend":
            return self.trend_analysis(data, **kwargs)
        elif analysis_type == "momentum":
            return self.momentum_analysis(data, **kwargs)
        elif analysis_type == "regime":
            return self.regime_detection(data, **kwargs)
        elif analysis_type == "technical":
            return self.technical_indicators(data, **kwargs)
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")

    def trend_analysis(
        self,
        prices: pd.DataFrame,
        windows: List[int] = [20, 50, 200]
    ) -> Dict[str, pd.DataFrame]:
        """
        Analyze price trends using moving averages.

        Args:
            prices: DataFrame with price data
            windows: List of window sizes for moving averages

        Returns:
            Dictionary with trend analysis results
        """
        self.logger.info("Analyzing trends")

        results = {}

        # Calculate moving averages
        for window in windows:
            results[f'SMA_{window}'] = prices.rolling(window=window).mean()

        # Calculate trend signals
        results['trend_signal'] = pd.DataFrame(index=prices.index)

        for col in prices.columns:
            # Simple trend: price above/below MA
            if f'SMA_{windows[0]}' in results:
                results['trend_signal'][col] = np.where(
                    prices[col] > results[f'SMA_{windows[0]}'][col],
                    1,  # Uptrend
                    -1  # Downtrend
                )

        # Calculate trend strength
        results['trend_strength'] = pd.DataFrame(index=prices.index)

        for col in prices.columns:
            if len(windows) >= 2:
                # Trend strength based on MA alignment
                short_ma = results[f'SMA_{windows[0]}'][col]
                long_ma = results[f'SMA_{windows[-1]}'][col]
                results['trend_strength'][col] = (
                    (short_ma - long_ma) / long_ma * 100
                )

        self.logger.info("Trend analysis completed")
        return results

    def momentum_analysis(
        self,
        prices: pd.DataFrame,
        period: int = 14
    ) -> Dict[str, pd.DataFrame]:
        """
        Calculate momentum indicators.

        Args:
            prices: DataFrame with price data
            period: Lookback period for momentum calculation

        Returns:
            Dictionary with momentum indicators
        """
        self.logger.info("Calculating momentum indicators")

        results = {}

        # Rate of Change (ROC)
        results['ROC'] = ((prices - prices.shift(period)) /
                         prices.shift(period) * 100)

        # Relative Strength Index (RSI)
        results['RSI'] = pd.DataFrame(index=prices.index, columns=prices.columns)

        for col in prices.columns:
            delta = prices[col].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

            rs = gain / loss
            results['RSI'][col] = 100 - (100 / (1 + rs))

        # MACD (Moving Average Convergence Divergence)
        results['MACD'] = pd.DataFrame(index=prices.index)
        results['MACD_signal'] = pd.DataFrame(index=prices.index)
        results['MACD_histogram'] = pd.DataFrame(index=prices.index)

        for col in prices.columns:
            ema_12 = prices[col].ewm(span=12, adjust=False).mean()
            ema_26 = prices[col].ewm(span=26, adjust=False).mean()

            results['MACD'][col] = ema_12 - ema_26
            results['MACD_signal'][col] = results['MACD'][col].ewm(
                span=9, adjust=False
            ).mean()
            results['MACD_histogram'][col] = (
                results['MACD'][col] - results['MACD_signal'][col]
            )

        self.logger.info("Momentum analysis completed")
        return results

    def volatility_indicators(
        self,
        prices: pd.DataFrame,
        window: int = 20,
        num_std: float = 2.0
    ) -> Dict[str, pd.DataFrame]:
        """
        Calculate volatility-based indicators.

        Args:
            prices: DataFrame with price data
            window: Window size for calculations
            num_std: Number of standard deviations for Bollinger Bands

        Returns:
            Dictionary with volatility indicators
        """
        self.logger.info("Calculating volatility indicators")

        results = {}

        # Bollinger Bands
        results['BB_middle'] = prices.rolling(window=window).mean()
        results['BB_std'] = prices.rolling(window=window).std()
        results['BB_upper'] = results['BB_middle'] + (results['BB_std'] * num_std)
        results['BB_lower'] = results['BB_middle'] - (results['BB_std'] * num_std)

        # Bollinger Band Width
        results['BB_width'] = (
            (results['BB_upper'] - results['BB_lower']) / results['BB_middle']
        )

        # Average True Range (ATR) - simplified version
        high_low = prices.rolling(window=window).max() - prices.rolling(window=window).min()
        results['ATR'] = high_low.rolling(window=window).mean()

        self.logger.info("Volatility indicators calculated")
        return results

    def technical_indicators(
        self,
        prices: pd.DataFrame,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive technical indicators.

        Args:
            prices: DataFrame with price data
            **kwargs: Additional parameters for indicators

        Returns:
            Dictionary with all technical indicators
        """
        self.logger.info("Calculating technical indicators")

        results = {
            'trend': self.trend_analysis(
                prices,
                windows=kwargs.get('ma_windows', [20, 50, 200])
            ),
            'momentum': self.momentum_analysis(
                prices,
                period=kwargs.get('momentum_period', 14)
            ),
            'volatility': self.volatility_indicators(
                prices,
                window=kwargs.get('volatility_window', 20)
            )
        }

        self.logger.info("Technical indicators calculated")
        return results

    def regime_detection(
        self,
        returns: pd.DataFrame,
        method: str = "volatility",
        window: int = 60
    ) -> Dict[str, pd.DataFrame]:
        """
        Detect market regimes based on statistical properties.

        Args:
            returns: DataFrame with return data
            method: Detection method ('volatility', 'correlation')
            window: Rolling window size

        Returns:
            Dictionary with regime detection results
        """
        self.logger.info(f"Detecting market regimes using {method} method")

        results = {}

        if method == "volatility":
            # Volatility regime
            vol = returns.rolling(window=window).std()
            vol_median = vol.median()

            results['regime'] = pd.DataFrame(index=returns.index)
            for col in returns.columns:
                results['regime'][col] = np.where(
                    vol[col] > vol_median[col],
                    'high_vol',
                    'low_vol'
                )

            results['volatility'] = vol

        elif method == "correlation":
            # Correlation regime
            if returns.shape[1] > 1:
                rolling_corr = returns.rolling(window=window).corr()
                # Average correlation
                avg_corr = rolling_corr.groupby(level=0).mean().mean(axis=1)

                results['regime'] = pd.DataFrame(index=returns.index)
                results['regime']['market'] = np.where(
                    avg_corr > avg_corr.median(),
                    'high_correlation',
                    'low_correlation'
                )

                results['correlation'] = avg_corr
            else:
                self.logger.warning("Correlation regime requires multiple assets")

        else:
            raise ValueError(f"Unknown method: {method}")

        self.logger.info("Regime detection completed")
        return results

    def support_resistance(
        self,
        prices: pd.Series,
        window: int = 20,
        num_levels: int = 3
    ) -> Dict[str, List[float]]:
        """
        Identify support and resistance levels.

        Args:
            prices: Series with price data
            window: Window for local extrema detection
            num_levels: Number of levels to identify

        Returns:
            Dictionary with support and resistance levels
        """
        self.logger.info("Identifying support and resistance levels")

        # Find local maxima (resistance)
        local_max = prices[
            (prices.shift(1) < prices) & (prices.shift(-1) < prices)
        ]

        # Find local minima (support)
        local_min = prices[
            (prices.shift(1) > prices) & (prices.shift(-1) > prices)
        ]

        # Get top resistance levels
        resistance = sorted(local_max.nlargest(num_levels * 2).values, reverse=True)
        resistance = list(dict.fromkeys(resistance))[:num_levels]  # Remove duplicates

        # Get top support levels
        support = sorted(local_min.nsmallest(num_levels * 2).values)
        support = list(dict.fromkeys(support))[:num_levels]  # Remove duplicates

        results = {
            'resistance': resistance,
            'support': support,
            'current_price': prices.iloc[-1]
        }

        self.logger.info("Support and resistance levels identified")
        return results

    def comparative_analysis(
        self,
        data: pd.DataFrame,
        benchmark: Optional[pd.Series] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Perform comparative analysis across assets.

        Args:
            data: DataFrame with asset data
            benchmark: Optional benchmark series for comparison

        Returns:
            Dictionary with comparative analysis results
        """
        self.logger.info("Performing comparative analysis")

        results = {}

        # Calculate returns
        returns = data.pct_change()

        # Relative performance
        if benchmark is not None:
            benchmark_returns = benchmark.pct_change()
            results['relative_returns'] = returns.sub(benchmark_returns, axis=0)

            # Cumulative relative performance
            results['relative_performance'] = (
                (1 + results['relative_returns']).cumprod() - 1
            )

        # Cross-asset correlation
        results['correlation'] = returns.corr()

        # Relative strength
        # Normalized prices (base = 100)
        results['normalized_prices'] = (data / data.iloc[0]) * 100

        # Ranking
        results['performance_rank'] = returns.rank(axis=1, ascending=False)

        self.logger.info("Comparative analysis completed")
        return results

    def market_summary(
        self,
        prices: pd.DataFrame,
        returns: Optional[pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive market summary.

        Args:
            prices: DataFrame with price data
            returns: Optional DataFrame with return data

        Returns:
            Dictionary with market summary
        """
        self.logger.info("Generating market summary")

        if returns is None:
            returns = prices.pct_change()

        summary = {
            'latest_prices': prices.iloc[-1].to_dict(),
            'price_change_1d': ((prices.iloc[-1] / prices.iloc[-2]) - 1).to_dict(),
            'price_change_1w': ((prices.iloc[-1] / prices.iloc[-5]) - 1).to_dict() if len(prices) >= 5 else None,
            'price_change_1m': ((prices.iloc[-1] / prices.iloc[-21]) - 1).to_dict() if len(prices) >= 21 else None,
            'volatility_20d': returns.tail(20).std().to_dict(),
            'current_trend': self.trend_analysis(prices, windows=[20, 50])
        }

        self.logger.info("Market summary generated")
        return summary
