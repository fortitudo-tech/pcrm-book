"""Tests for StatisticalAnalysisAgent."""

import pytest
import pandas as pd
import numpy as np
from scipy import stats
from src.agents.statistical_analysis_agent import StatisticalAnalysisAgent


class TestStatisticalAnalysisAgent:
    """Test cases for StatisticalAnalysisAgent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        return StatisticalAnalysisAgent()

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        np.random.seed(42)
        dates = pd.date_range('2023-01-01', periods=252, freq='D')
        data = {
            'Asset1': np.random.randn(252) * 0.01,
            'Asset2': np.random.randn(252) * 0.015,
            'Asset3': np.random.randn(252) * 0.02
        }
        return pd.DataFrame(data, index=dates)

    def test_initialization(self, agent):
        """Test agent initialization."""
        assert agent.name == "StatisticalAnalysisAgent"

    def test_execute_descriptive(self, agent, sample_data):
        """Test executing descriptive statistics."""
        result = agent.execute(sample_data, analysis_type='descriptive')

        assert 'basic_stats' in result
        assert 'skewness' in result
        assert 'kurtosis' in result
        assert isinstance(result['basic_stats'], pd.DataFrame)

    def test_execute_correlation(self, agent, sample_data):
        """Test executing correlation analysis."""
        result = agent.execute(sample_data, analysis_type='correlation')

        assert 'correlation' in result
        assert 'covariance' in result
        assert isinstance(result['correlation'], pd.DataFrame)
        assert result['correlation'].shape == (3, 3)

    def test_execute_distribution(self, agent, sample_data):
        """Test executing distribution analysis."""
        result = agent.execute(sample_data, analysis_type='distribution')

        assert 'Asset1' in result
        assert 'mean' in result['Asset1']
        assert 'median' in result['Asset1']
        assert 'skewness' in result['Asset1']

    def test_execute_timeseries(self, agent, sample_data):
        """Test executing time series analysis."""
        result = agent.execute(sample_data, analysis_type='timeseries')

        assert 'Asset1' in result
        assert 'autocorr_lag1' in result['Asset1']

    def test_execute_invalid_type(self, agent, sample_data):
        """Test invalid analysis type."""
        with pytest.raises(ValueError):
            agent.execute(sample_data, analysis_type='invalid')

    def test_descriptive_statistics(self, agent, sample_data):
        """Test descriptive statistics calculation."""
        result = agent.descriptive_statistics(sample_data)

        assert 'basic_stats' in result
        assert 'skewness' in result
        assert 'kurtosis' in result
        assert 'range' in result
        assert 'iqr' in result
        assert 'missing_count' in result

    def test_correlation_analysis_pearson(self, agent, sample_data):
        """Test Pearson correlation analysis."""
        result = agent.correlation_analysis(sample_data, method='pearson')

        assert 'correlation' in result
        assert 'covariance' in result
        assert 'correlation_pvalues' in result
        # Check correlation matrix is symmetric
        assert np.allclose(
            result['correlation'].values,
            result['correlation'].values.T
        )

    def test_correlation_analysis_spearman(self, agent, sample_data):
        """Test Spearman correlation analysis."""
        result = agent.correlation_analysis(sample_data, method='spearman')

        assert 'correlation' in result
        assert 'covariance' in result
        # Spearman should not have p-values in current implementation
        assert 'correlation_pvalues' not in result

    def test_distribution_analysis(self, agent, sample_data):
        """Test distribution analysis."""
        result = agent.distribution_analysis(sample_data, test_normal=True)

        for asset in sample_data.columns:
            assert asset in result
            assert 'mean' in result[asset]
            assert 'median' in result[asset]
            assert 'std' in result[asset]
            assert 'jarque_bera_test' in result[asset]

    def test_timeseries_analysis(self, agent, sample_data):
        """Test time series analysis."""
        result = agent.timeseries_analysis(sample_data, test_stationarity=False)

        for asset in sample_data.columns:
            assert asset in result
            assert 'autocorr_lag1' in result[asset]

    def test_outlier_detection_iqr(self, agent, sample_data):
        """Test outlier detection using IQR method."""
        result = agent.outlier_detection(sample_data, method='iqr')

        for asset in sample_data.columns:
            assert asset in result
            assert 'outlier_count' in result[asset]
            assert 'outlier_pct' in result[asset]
            assert 'outlier_indices' in result[asset]

    def test_outlier_detection_zscore(self, agent, sample_data):
        """Test outlier detection using z-score method."""
        result = agent.outlier_detection(sample_data, method='zscore', threshold=3)

        for asset in sample_data.columns:
            assert asset in result
            assert isinstance(result[asset]['outlier_count'], (int, np.integer))

    def test_outlier_detection_invalid_method(self, agent, sample_data):
        """Test invalid outlier detection method."""
        with pytest.raises(ValueError):
            agent.outlier_detection(sample_data, method='invalid')

    def test_hypothesis_test_ttest_one_sample(self, agent):
        """Test one-sample t-test."""
        data = pd.Series(np.random.randn(100))
        result = agent.hypothesis_test(data, test_type='ttest', popmean=0)

        assert 'test_type' in result
        assert 'statistic' in result
        assert 'p_value' in result
        assert 'significant' in result

    def test_hypothesis_test_ttest_two_sample(self, agent):
        """Test two-sample t-test."""
        data1 = pd.Series(np.random.randn(100))
        data2 = pd.Series(np.random.randn(100) + 0.5)
        result = agent.hypothesis_test(data1, data2, test_type='ttest')

        assert result['test_type'] == 'ttest'
        assert 'p_value' in result

    def test_hypothesis_test_mannwhitney(self, agent):
        """Test Mann-Whitney U test."""
        data1 = pd.Series(np.random.randn(100))
        data2 = pd.Series(np.random.randn(100) + 0.5)
        result = agent.hypothesis_test(data1, data2, test_type='mannwhitney')

        assert result['test_type'] == 'mannwhitney'
        assert 'p_value' in result

    def test_hypothesis_test_invalid_type(self, agent):
        """Test invalid hypothesis test type."""
        data = pd.Series(np.random.randn(100))
        with pytest.raises(ValueError):
            agent.hypothesis_test(data, test_type='invalid')

    def test_validate_input(self, agent):
        """Test input validation."""
        assert agent.validate_input(pd.DataFrame()) is True
        assert agent.validate_input(None) is False
