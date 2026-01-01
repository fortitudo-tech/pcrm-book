"""
Base agent class for all research agents.

This module provides the foundational class that all specialized research
agents inherit from, ensuring consistent interface and shared functionality.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
import logging


class BaseAgent(ABC):
    """
    Abstract base class for all research agents.

    This class provides common functionality and interface that all
    specialized agents should implement.

    Attributes:
        name (str): Name of the agent
        description (str): Description of agent's purpose
        logger (logging.Logger): Logger instance for the agent
        metadata (Dict): Additional metadata about the agent
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        log_level: int = logging.INFO,
        **kwargs
    ):
        """
        Initialize the base agent.

        Args:
            name: Name of the agent
            description: Description of agent's purpose
            log_level: Logging level (default: logging.INFO)
            **kwargs: Additional configuration parameters
        """
        self.name = name
        self.description = description
        self.metadata = kwargs
        self.created_at = datetime.now()

        # Setup logging
        self.logger = logging.getLogger(f"agents.{self.name}")
        self.logger.setLevel(log_level)

        # Create console handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(log_level)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.info(f"Initialized {self.name}")

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the agent's primary function.

        This method must be implemented by all subclasses.

        Returns:
            Results of the agent's execution
        """
        pass

    def validate_input(self, data: Any) -> bool:
        """
        Validate input data before processing.

        Args:
            data: Input data to validate

        Returns:
            True if valid, False otherwise
        """
        return data is not None

    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the agent.

        Returns:
            Dictionary containing agent information
        """
        return {
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'metadata': self.metadata
        }

    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.name}: {self.description}"
