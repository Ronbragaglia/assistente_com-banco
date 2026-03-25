# -*- coding: utf-8 -*-
"""Tests for configuration module."""

import pytest
from pathlib import Path
from pydantic import ValidationError

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database_assistant.config import Settings


class TestSettings:
    """Test cases for Settings class."""

    def test_default_values(self):
        """Test that default values are set correctly."""
        settings = Settings(
            openai_api_key="test-key"
        )
        
        assert settings.openai_model == "gpt-3.5-turbo"
        assert settings.openai_temperature == 0.7
        assert settings.assistant_name == "Assistente de Eventos"
        assert settings.similarity_threshold == 0.7
        assert settings.log_level == "INFO"
        assert settings.cache_enabled is True

    def test_custom_values(self):
        """Test that custom values are set correctly."""
        settings = Settings(
            openai_api_key="test-key",
            openai_model="gpt-4",
            openai_temperature=0.5,
            assistant_name="Custom Assistant",
            similarity_threshold=0.8,
            log_level="DEBUG",
        )
        
        assert settings.openai_model == "gpt-4"
        assert settings.openai_temperature == 0.5
        assert settings.assistant_name == "Custom Assistant"
        assert settings.similarity_threshold == 0.8
        assert settings.log_level == "DEBUG"

    def test_validate_log_level_valid(self):
        """Test validation of valid log levels."""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            settings = Settings(
                openai_api_key="test-key",
                log_level=level
            )
            assert settings.log_level == level

    def test_validate_log_level_invalid(self):
        """Test validation of invalid log levels."""
        with pytest.raises(ValidationError):
            Settings(
                openai_api_key="test-key",
                log_level="INVALID"
            )

    def test_temperature_range(self):
        """Test temperature range validation."""
        # Valid range
        Settings(
            openai_api_key="test-key",
            openai_temperature=0.0
        )
        Settings(
            openai_api_key="test-key",
            openai_temperature=2.0
        )
        
        # Invalid range
        with pytest.raises(ValidationError):
            Settings(
                openai_api_key="test-key",
                openai_temperature=-0.1
            )
        with pytest.raises(ValidationError):
            Settings(
                openai_api_key="test-key",
                openai_temperature=2.1
            )

    def test_similarity_threshold_range(self):
        """Test similarity threshold range validation."""
        # Valid range
        Settings(
            openai_api_key="test-key",
            similarity_threshold=0.0
        )
        Settings(
            openai_api_key="test-key",
            similarity_threshold=1.0
        )
        
        # Invalid range
        with pytest.raises(ValidationError):
            Settings(
                openai_api_key="test-key",
                similarity_threshold=-0.1
            )
        with pytest.raises(ValidationError):
            Settings(
                openai_api_key="test-key",
                similarity_threshold=1.1
            )

    def test_ensure_directories(self):
        """Test that directories are created."""
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            settings = Settings(
                openai_api_key="test-key",
                data_dir=Path(tmpdir) / "data",
                logs_dir=Path(tmpdir) / "logs",
                database_path=Path(tmpdir) / "data" / "test.db",
            )
            
            settings.ensure_directories()
            
            assert settings.data_dir.exists()
            assert settings.logs_dir.exists()
            assert settings.database_path.parent.exists()

    def test_cache_configuration(self):
        """Test cache configuration."""
        settings = Settings(
            openai_api_key="test-key",
            cache_enabled=True,
        )
        assert settings.cache_enabled is True
        
        settings = Settings(
            openai_api_key="test-key",
            cache_enabled=False,
        )
        assert settings.cache_enabled is False
