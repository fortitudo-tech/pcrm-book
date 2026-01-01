"""
Statistical Analysis Agent for quantitative financial analysis.

This agent performs statistical analysis on financial data including
descriptive statistics, correlation analysis, hypothesis testing, and
time series analysis.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Optional, Tuple, Any
import warnings

from .base_agent import BaseAgent


class StatisticalAnalysisAgent(BaseAgent):
    """
    Agent specialized in statistical analysis of financial data.

    This agent can:
    - Compute descriptive statistics
    - Perform correlation and covariance analysis
    - Conduct hypothesis testing
    - Analyze distributions
    - Perform time series analysis
    - Detect outliers and anomalies
    """

    def __init__(self, **kwargs):
        """Initialize the Statistical Analysis Agent."""
        super().__init__(
            name="StatisticalAnalysisAgent",
            description="Performs statistical analysis on financial data",
            **kwargs
        )

    def execute(
        self,
        data: pd.DataFrame,
        analysis_type: str = "descriptive",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute statistical analysis on the provided data.

        Args:
            data: DataFrame containing the data to analyze
            analysis_type: Type of analysis ('descriptive', 'correlation',
                          'distribution', 'timeseries')
            **kwargs: Additional parameters for specific analysis types

        Returns:
            Dictionary containing analysis results
        """
        self.logger.info(f"Performing {analysis_type} analysis")

        if not self.validate_input(data):
            raise ValueError("Invalid input data")

        if analysis_type == "descriptive":
            return self.descriptive_statistics(data, **kwargs)
        elif analysis_type == "correlation":
            return self.correlation_analysis(data, **kwargs)
        elif analysis_type == "distribution":
            return self.distribution_analysis(data, **kwargs)
        elif analysis_type == "timeseries":
            return self.timeseries_analysis(data, **kwargs)
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")

    def descriptive_statistics(
        self,
        data: pd.DataFrame,
        percentiles: List[float] = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]
    ) -> Dict[str, pd.DataFrame]:
        """
        Compute comprehensive descriptive statistics.

        Args:
            data: DataFrame to analyze
            percentiles: List of percentiles to compute

        Returns:
            Dictionary containing various statistical measures
        """
        self.logger.info("Computing descriptive statistics")

        results = {}

        # Basic statistics
        results['basic_stats'] = data.describe(percentiles=percentiles)

        # Additional moments
        results['skewness'] = data.skew()
        results['kurtosis'] = data.kurtosis()

        # Range and spread
        results['range'] = data.max() - data.min()
        results['iqr'] = data.quantile(0.75) - data.quantile(0.25)

        # Missing values
        results['missing_count'] = data.isnull().sum()
        results['missing_pct'] = (data.isnull().sum() / len(data)) * 100

        self.logger.info("Descriptive statistics completed")
        return results

    def correlation_analysis(
        self,
        data: pd.DataFrame,
        method: str = "pearson"
    ) -> Dict[str, pd.DataFrame]:
        """
        Perform correlation and covariance analysis.

        Args:
            data: DataFrame to analyze
            method: Correlation method ('pearson', 'spearman', 'kendall')

        Returns:
            Dictionary with correlation and covariance matrices
        """
        self.logger.info(f"Computing {method} correlation")

        results = {}

        # Correlation matrix
        results['correlation'] = data.corr(method=method)

        # Covariance matrix
        results['covariance'] = data.cov()

        # Correlation significance (for Pearson only)
        if method == "pearson":
            n = len(data)
            corr = results['correlation'].values
            # t-statistic for correlation
            t_stat = corr * np.sqrt((n - 2) / (1 - corr**2))
            p_values = 2 * (1 - stats.t.cdf(np.abs(t_stat), n - 2))
            results['correlation_pvalues'] = pd.DataFrame(
                p_values,
                index=results['correlation'].index,
                columns=results['correlation'].columns
            )

        self.logger.info("Correlation analysis completed")
        return results

    def distribution_analysis(
        self,
        data: pd.DataFrame,
        test_normal: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze the distribution of data.

        Args:
            data: DataFrame to analyze
            test_normal: Whether to test for normality

        Returns:
            Dictionary with distribution analysis results
        """
        self.logger.info("Analyzing distributions")

        results = {}

        for column in data.columns:
            col_results = {}

            # Remove NaN values
            clean_data = data[column].dropna()

            if len(clean_data) == 0:
                self.logger.warning(f"Column {column} has no valid data")
                continue

            # Basic distribution properties
            col_results['mean'] = clean_data.mean()
            col_results['median'] = clean_data.median()
            col_results['std'] = clean_data.std()
            col_results['skewness'] = clean_data.skew()
            col_results['kurtosis'] = clean_data.kurtosis()

            # Normality tests
            if test_normal and len(clean_data) >= 3:
                # Shapiro-Wilk test (best for n < 5000)
                if len(clean_data) < 5000:
                    stat, p_value = stats.shapiro(clean_data)
                    col_results['shapiro_test'] = {
                        'statistic': stat,
                        'p_value': p_value,
                        'is_normal': p_value > 0.05
                    }

                # Jarque-Bera test
                stat, p_value = stats.jarque_bera(clean_data)
                col_results['jarque_bera_test'] = {
                    'statistic': stat,
                    'p_value': p_value,
                    'is_normal': p_value > 0.05
                }

            results[column] = col_results

        self.logger.info("Distribution analysis completed")
        return results

    def timeseries_analysis(
        self,
        data: pd.DataFrame,
        test_stationarity: bool = True
    ) -> Dict[str, Any]:
        """
        Perform time series analysis.

        Args:
            data: DataFrame to analyze (should have datetime index)
            test_stationarity: Whether to test for stationarity

        Returns:
            Dictionary with time series analysis results
        """
        self.logger.info("Performing time series analysis")

        results = {}

        for column in data.columns:
            col_results = {}

            # Remove NaN values
            clean_data = data[column].dropna()

            if len(clean_data) == 0:
                self.logger.warning(f"Column {column} has no valid data")
                continue

            # Autocorrelation
            if len(clean_data) > 1:
                col_results['autocorr_lag1'] = clean_data.autocorr(lag=1)

            # Stationarity test (Augmented Dickey-Fuller)
            if test_stationarity and len(clean_data) >= 12:
                try:
                    from statsmodels.tsa.stattools import adfuller
                    adf_result = adfuller(clean_data, autolag='AIC')
                    col_results['adf_test'] = {
                        'statistic': adf_result[0],
                        'p_value': adf_result[1],
                        'is_stationary': adf_result[1] < 0.05,
                        'critical_values': adf_result[4]
                    }
                except ImportError:
                    self.logger.warning("statsmodels not available for ADF test")

            results[column] = col_results

        self.logger.info("Time series analysis completed")
        return results

    def outlier_detection(
        self,
        data: pd.DataFrame,
        method: str = "iqr",
        threshold: float = 1.5
    ) -> Dict[str, Any]:
        """
        Detect outliers in the data.

        Args:
            data: DataFrame to analyze
            method: Detection method ('iqr', 'zscore', 'modified_zscore')
            threshold: Threshold for outlier detection

        Returns:
            Dictionary with outlier detection results
        """
        self.logger.info(f"Detecting outliers using {method} method")

        results = {}

        for column in data.columns:
            clean_data = data[column].dropna()

            if len(clean_data) == 0:
                continue

            if method == "iqr":
                Q1 = clean_data.quantile(0.25)
                Q3 = clean_data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                outliers = (clean_data < lower_bound) | (clean_data > upper_bound)

            elif method == "zscore":
                z_scores = np.abs(stats.zscore(clean_data))
                outliers = z_scores > threshold

            elif method == "modified_zscore":
                median = clean_data.median()
                mad = np.median(np.abs(clean_data - median))
                modified_z_scores = 0.6745 * (clean_data - median) / mad
                outliers = np.abs(modified_z_scores) > threshold

            else:
                raise ValueError(f"Unknown method: {method}")

            results[column] = {
                'outlier_count': outliers.sum(),
                'outlier_pct': (outliers.sum() / len(clean_data)) * 100,
                'outlier_indices': data.index[outliers].tolist()
            }

        self.logger.info("Outlier detection completed")
        return results

    def hypothesis_test(
        self,
        data1: pd.Series,
        data2: Optional[pd.Series] = None,
        test_type: str = "ttest",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform hypothesis testing.

        Args:
            data1: First data series
            data2: Second data series (for two-sample tests)
            test_type: Type of test ('ttest', 'mannwhitney', 'kstest')
            **kwargs: Additional test parameters

        Returns:
            Dictionary with test results
        """
        self.logger.info(f"Performing {test_type} hypothesis test")

        # Clean data
        data1 = data1.dropna()
        if data2 is not None:
            data2 = data2.dropna()

        if test_type == "ttest":
            if data2 is None:
                # One-sample t-test
                stat, p_value = stats.ttest_1samp(
                    data1,
                    kwargs.get('popmean', 0)
                )
            else:
                # Two-sample t-test
                stat, p_value = stats.ttest_ind(data1, data2)

        elif test_type == "mannwhitney":
            if data2 is None:
                raise ValueError("Mann-Whitney test requires two samples")
            stat, p_value = stats.mannwhitneyu(data1, data2)

        elif test_type == "kstest":
            if data2 is None:
                # One-sample KS test
                stat, p_value = stats.kstest(
                    data1,
                    kwargs.get('cdf', 'norm')
                )
            else:
                # Two-sample KS test
                stat, p_value = stats.ks_2samp(data1, data2)

        else:
            raise ValueError(f"Unknown test type: {test_type}")

        result = {
            'test_type': test_type,
            'statistic': stat,
            'p_value': p_value,
            'significant': p_value < kwargs.get('alpha', 0.05)
        }

        self.logger.info("Hypothesis test completed")
        return result
