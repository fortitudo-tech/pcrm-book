"""
Configuration management for agents.

This module provides centralized configuration for all agents,
including logging, API settings, and default parameters.
"""

import os
import logging
from typing import Dict, Any
from pathlib import Path


class AgentConfig:
    """Configuration class for agents."""

    # Logging configuration
    LOG_LEVEL = os.getenv('AGENT_LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.getenv('AGENT_LOG_FILE', None)

    # Data collection settings
    DATA_CACHE_DIR = Path(os.getenv('AGENT_CACHE_DIR', '.cache/agents'))
    DATA_CACHE_ENABLED = os.getenv('AGENT_CACHE_ENABLED', 'true').lower() == 'true'
    DATA_CACHE_TTL = int(os.getenv('AGENT_CACHE_TTL', '3600'))  # seconds

    # Risk analytics defaults
    DEFAULT_CONFIDENCE_LEVEL = float(os.getenv('DEFAULT_CONFIDENCE_LEVEL', '0.95'))
    DEFAULT_RISK_FREE_RATE = float(os.getenv('DEFAULT_RISK_FREE_RATE', '0.02'))
    PERIODS_PER_YEAR = int(os.getenv('PERIODS_PER_YEAR', '252'))

    # Backtesting defaults
    DEFAULT_INITIAL_CAPITAL = float(os.getenv('DEFAULT_INITIAL_CAPITAL', '100000'))
    DEFAULT_COMMISSION = float(os.getenv('DEFAULT_COMMISSION', '0.001'))
    DEFAULT_SLIPPAGE = float(os.getenv('DEFAULT_SLIPPAGE', '0.0005'))
    DEFAULT_REBALANCE_FREQ = os.getenv('DEFAULT_REBALANCE_FREQ', 'monthly')

    # API settings
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', '1'))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))

    # Performance settings
    MAX_WORKERS = int(os.getenv('MAX_WORKERS', '4'))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '100'))

    @classmethod
    def get_logging_config(cls) -> Dict[str, Any]:
        """Get logging configuration dictionary."""
        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': cls.LOG_FORMAT
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': cls.LOG_LEVEL,
                    'formatter': 'standard',
                },
            },
            'loggers': {
                'agents': {
                    'handlers': ['console'],
                    'level': cls.LOG_LEVEL,
                    'propagate': False
                }
            }
        }

        # Add file handler if log file is specified
        if cls.LOG_FILE:
            config['handlers']['file'] = {
                'class': 'logging.FileHandler',
                'filename': cls.LOG_FILE,
                'level': cls.LOG_LEVEL,
                'formatter': 'standard',
            }
            config['loggers']['agents']['handlers'].append('file')

        return config

    @classmethod
    def setup_logging(cls):
        """Setup logging configuration."""
        logging.config.dictConfig(cls.get_logging_config())

    @classmethod
    def get_cache_path(cls, key: str) -> Path:
        """Get cache file path for a given key."""
        cls.DATA_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        return cls.DATA_CACHE_DIR / f"{key}.pkl"

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            attr: getattr(cls, attr)
            for attr in dir(cls)
            if not attr.startswith('_') and not callable(getattr(cls, attr))
        }

    @classmethod
    def from_env(cls, prefix: str = 'AGENT_') -> 'AgentConfig':
        """Load configuration from environment variables."""
        # Configuration is already loaded from environment in class definition
        return cls

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration values."""
        try:
            assert 0 < cls.DEFAULT_CONFIDENCE_LEVEL < 1, "Confidence level must be between 0 and 1"
            assert cls.DEFAULT_RISK_FREE_RATE >= 0, "Risk-free rate must be non-negative"
            assert cls.PERIODS_PER_YEAR > 0, "Periods per year must be positive"
            assert cls.DEFAULT_INITIAL_CAPITAL > 0, "Initial capital must be positive"
            assert 0 <= cls.DEFAULT_COMMISSION < 1, "Commission must be between 0 and 1"
            assert 0 <= cls.DEFAULT_SLIPPAGE < 1, "Slippage must be between 0 and 1"
            assert cls.MAX_RETRIES >= 0, "Max retries must be non-negative"
            assert cls.RETRY_DELAY > 0, "Retry delay must be positive"
            assert cls.REQUEST_TIMEOUT > 0, "Request timeout must be positive"
            return True
        except AssertionError as e:
            logging.error(f"Configuration validation failed: {e}")
            return False


# Create a global config instance
config = AgentConfig()

# Validate configuration on import
if not config.validate():
    logging.warning("Configuration validation failed. Using defaults.")
