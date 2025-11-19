"""
Tests for Langfuse observability integration with Pydantic AI.

Note: Langfuse integration with Pydantic AI is automatic via Agent.instrument_all().
These tests verify that the basic setup works correctly.
"""

import pytest
import os
from agent.config import config


class TestLangfuseEnvironment:
    """Tests for Langfuse environment configuration."""

    def test_langfuse_env_vars_exist_in_example(self):
        """Test that .env.example contains Langfuse variables."""
        env_example_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.example")

        with open(env_example_path, "r") as f:
            content = f.read()

        assert "LANGFUSE_PUBLIC_KEY" in content
        assert "LANGFUSE_SECRET_KEY" in content
        assert "LANGFUSE_HOST" in content
        assert "ENABLE_LANGFUSE_TRACING" in content

    def test_config_module_loads(self):
        """Test that config module loads without errors."""
        assert config is not None
        assert hasattr(config, 'database')
        assert hasattr(config, 'llm')
        assert hasattr(config, 'app')


class TestAgentInstrumentation:
    """Tests for Agent instrumentation setup."""

    def test_agent_import_without_errors(self):
        """Test that agent module imports successfully with instrumentation."""
        try:
            from agent.agent import rag_agent
            assert rag_agent is not None
        except Exception as e:
            pytest.fail(f"Agent import failed: {e}")

    def test_agent_has_tools(self):
        """Test that agent has tools registered."""
        from agent.agent import rag_agent

        # The agent should have tools registered
        assert hasattr(rag_agent, 'tools')
        assert len(rag_agent.tools) > 0
