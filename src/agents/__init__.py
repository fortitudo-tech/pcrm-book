"""
Research agents for financial data analysis and portfolio management.

This module provides AI-powered research agents for:
- Data collection and management
- Statistical analysis
- Risk analytics
- Market research
- Backtesting and strategy validation
"""

__version__ = "1.0.0"

from .base_agent import BaseAgent
from .data_collection_agent import DataCollectionAgent
from .statistical_analysis_agent import StatisticalAnalysisAgent
from .risk_analytics_agent import RiskAnalyticsAgent
from .market_research_agent import MarketResearchAgent
from .backtesting_agent import BacktestingAgent
from .config import AgentConfig, config

__all__ = [
    'BaseAgent',
    'DataCollectionAgent',
    'StatisticalAnalysisAgent',
    'RiskAnalyticsAgent',
    'MarketResearchAgent',
    'BacktestingAgent',
    'AgentConfig',
    'config',
]
