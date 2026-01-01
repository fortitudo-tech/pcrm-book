"""Tests for BaseAgent."""

import pytest
import logging
from src.agents.base_agent import BaseAgent


class ConcreteAgent(BaseAgent):
    """Concrete implementation for testing."""

    def execute(self, *args, **kwargs):
        """Test execution method."""
        return "executed"


class TestBaseAgent:
    """Test cases for BaseAgent."""

    def test_initialization(self):
        """Test agent initialization."""
        agent = ConcreteAgent(
            name="TestAgent",
            description="Test description",
            custom_param="value"
        )

        assert agent.name == "TestAgent"
        assert agent.description == "Test description"
        assert agent.metadata["custom_param"] == "value"
        assert agent.created_at is not None

    def test_logging_setup(self):
        """Test that logging is properly configured."""
        agent = ConcreteAgent(
            name="LogTestAgent",
            log_level=logging.DEBUG
        )

        assert agent.logger is not None
        assert agent.logger.level == logging.DEBUG

    def test_execute_method(self):
        """Test execute method is implemented."""
        agent = ConcreteAgent(name="ExecuteTest")
        result = agent.execute()

        assert result == "executed"

    def test_validate_input(self):
        """Test input validation."""
        agent = ConcreteAgent(name="ValidationTest")

        assert agent.validate_input("data") is True
        assert agent.validate_input(None) is False

    def test_get_info(self):
        """Test get_info method."""
        agent = ConcreteAgent(
            name="InfoTest",
            description="Info description",
            param1="value1"
        )

        info = agent.get_info()

        assert info["name"] == "InfoTest"
        assert info["description"] == "Info description"
        assert "created_at" in info
        assert info["metadata"]["param1"] == "value1"

    def test_repr(self):
        """Test string representation."""
        agent = ConcreteAgent(name="ReprTest")

        assert "ConcreteAgent" in repr(agent)
        assert "ReprTest" in repr(agent)

    def test_str(self):
        """Test human-readable string."""
        agent = ConcreteAgent(
            name="StrTest",
            description="String test"
        )

        str_repr = str(agent)
        assert "StrTest" in str_repr
        assert "String test" in str_repr

    def test_abstract_base_class(self):
        """Test that BaseAgent cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseAgent(name="DirectInstantiation")
