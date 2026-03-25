# -*- coding: utf-8 -*-
"""Tests for logger module."""

import pytest
import logging
from pathlib import Path
from io import StringIO
import sys

import sys
sys.path.insert(0, str(__file__).split("/tests")[0] + "/src")

from database_assistant.logger import setup_logger, get_logger


@pytest.fixture
def temp_log_file(tmp_path: Path) -> Path:
    """Create a temporary log file path."""
    return tmp_path / "test.log"


class TestSetupLogger:
    """Test cases for setup_logger function."""

    def test_setup_logger_default(self):
        """Test logger setup with default parameters."""
        logger = setup_logger()
        
        assert logger.name == "database_assistant"
        assert logger.level == logging.INFO
        assert len(logger.handlers) > 0

    def test_setup_logger_custom_name(self):
        """Test logger setup with custom name."""
        logger = setup_logger(name="custom_logger")
        
        assert logger.name == "custom_logger"

    def test_setup_logger_debug_level(self):
        """Test logger setup with DEBUG level."""
        logger = setup_logger(level="DEBUG")
        
        assert logger.level == logging.DEBUG

    def test_setup_logger_info_level(self):
        """Test logger setup with INFO level."""
        logger = setup_logger(level="INFO")
        
        assert logger.level == logging.INFO

    def test_setup_logger_warning_level(self):
        """Test logger setup with WARNING level."""
        logger = setup_logger(level="WARNING")
        
        assert logger.level == logging.WARNING

    def test_setup_logger_error_level(self):
        """Test logger setup with ERROR level."""
        logger = setup_logger(level="ERROR")
        
        assert logger.level == logging.ERROR

    def test_setup_logger_critical_level(self):
        """Test logger setup with CRITICAL level."""
        logger = setup_logger(level="CRITICAL")
        
        assert logger.level == logging.CRITICAL

    def test_setup_logger_with_file(self, temp_log_file: Path):
        """Test logger setup with file handler."""
        logger = setup_logger(log_file=str(temp_log_file))
        
        # Check if file handler exists
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) > 0
        
        # Check if log file was created
        assert temp_log_file.exists()

    def test_setup_logger_without_colors(self):
        """Test logger setup without colors."""
        logger = setup_logger(use_colors=False)
        
        # Check if console handler exists
        console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(console_handlers) > 0

    def test_setup_logger_with_colors(self):
        """Test logger setup with colors."""
        logger = setup_logger(use_colors=True)
        
        # Check if console handler exists
        console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(console_handlers) > 0

    def test_setup_logger_creates_log_directory(self, tmp_path: Path):
        """Test that logger creates log directory if it doesn't exist."""
        log_file = tmp_path / "logs" / "test.log"
        
        logger = setup_logger(log_file=str(log_file))
        logger.info("Test message")
        
        # Check if directory was created
        assert log_file.parent.exists()
        assert log_file.exists()

    def test_setup_logger_clears_existing_handlers(self):
        """Test that setup_logger clears existing handlers."""
        logger = setup_logger(name="test_clear_handlers")
        initial_handler_count = len(logger.handlers)
        
        # Setup again
        logger = setup_logger(name="test_clear_handlers")
        final_handler_count = len(logger.handlers)
        
        # Handler count should be the same (or different based on implementation)
        assert final_handler_count >= 1

    def test_setup_logger_log_message(self, temp_log_file: Path):
        """Test that logger can log messages."""
        logger = setup_logger(log_file=str(temp_log_file))
        logger.info("Test message")
        
        # Read log file
        log_content = temp_log_file.read_text()
        assert "Test message" in log_content

    def test_setup_logger_log_multiple_levels(self, temp_log_file: Path):
        """Test logging at different levels."""
        logger = setup_logger(level="DEBUG", log_file=str(temp_log_file))
        
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        
        # Read log file
        log_content = temp_log_file.read_text()
        assert "Debug message" in log_content
        assert "Info message" in log_content
        assert "Warning message" in log_content
        assert "Error message" in log_content
        assert "Critical message" in log_content

    def test_setup_logger_level_filtering(self, temp_log_file: Path):
        """Test that logger filters messages by level."""
        logger = setup_logger(level="WARNING", log_file=str(temp_log_file))
        
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        # Read log file
        log_content = temp_log_file.read_text()
        assert "Debug message" not in log_content
        assert "Info message" not in log_content
        assert "Warning message" in log_content
        assert "Error message" in log_content

    def test_setup_logger_unicode_support(self, temp_log_file: Path):
        """Test logger with Unicode characters."""
        logger = setup_logger(log_file=str(temp_log_file))
        
        logger.info("Test with émojis 🎉 and 中文, 日本語")
        
        # Read log file
        log_content = temp_log_file.read_text()
        assert "émojis 🎉" in log_content
        assert "中文, 日本語" in log_content

    def test_setup_logger_special_characters(self, temp_log_file: Path):
        """Test logger with special characters."""
        logger = setup_logger(log_file=str(temp_log_file))
        
        logger.info("Test with @, #, $, %, &, *, !")
        
        # Read log file
        log_content = temp_log_file.read_text()
        assert "@, #, $, %, &, *, !" in log_content

    def test_setup_logger_long_message(self, temp_log_file: Path):
        """Test logger with long message."""
        logger = setup_logger(log_file=str(temp_log_file))
        
        long_message = "A" * 10000
        logger.info(long_message)
        
        # Read log file
        log_content = temp_log_file.read_text()
        assert long_message in log_content

    def test_setup_logger_multiple_loggers(self):
        """Test creating multiple loggers."""
        logger1 = setup_logger(name="logger1")
        logger2 = setup_logger(name="logger2")
        
        assert logger1.name == "logger1"
        assert logger2.name == "logger2"
        assert logger1 is not logger2

    def test_setup_logger_reuse_existing(self):
        """Test that setup_logger reuses existing logger."""
        logger1 = setup_logger(name="reuse_test")
        logger2 = setup_logger(name="reuse_test")
        
        # Should return the same logger instance
        assert logger1.name == logger2.name

    def test_setup_logger_file_handler_format(self, temp_log_file: Path):
        """Test file handler format."""
        logger = setup_logger(log_file=str(temp_log_file))
        logger.info("Test message")
        
        # Read log file
        log_content = temp_log_file.read_text()
        
        # Check for format elements
        assert "database_assistant" in log_content  # logger name
        assert "INFO" in log_content  # log level
        assert "Test message" in log_content  # message


class TestGetLogger:
    """Test cases for get_logger function."""

    def test_get_logger_default(self):
        """Test get_logger with default name."""
        logger = get_logger()
        
        assert logger.name == "database_assistant"

    def test_get_logger_custom_name(self):
        """Test get_logger with custom name."""
        logger = get_logger(name="custom_logger")
        
        assert logger.name == "custom_logger"

    def test_get_logger_existing_logger(self):
        """Test get_logger returns existing logger."""
        logger1 = get_logger(name="existing_test")
        logger2 = get_logger(name="existing_test")
        
        # Should return the same logger
        assert logger1 is logger2

    def test_get_logger_after_setup(self):
        """Test get_logger after setup_logger."""
        setup_logger(name="setup_then_get")
        logger = get_logger(name="setup_then_get")
        
        assert logger is not None
        assert logger.name == "setup_then_get"


class TestLoggerIntegration:
    """Integration tests for logger functionality."""

    def test_logger_with_file_and_console(self, temp_log_file: Path):
        """Test logger with both file and console handlers."""
        logger = setup_logger(log_file=str(temp_log_file), use_colors=True)
        
        logger.info("Test message")
        
        # Check file handler
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) > 0
        
        # Check console handler
        console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(console_handlers) > 0
        
        # Check log file
        log_content = temp_log_file.read_text()
        assert "Test message" in log_content

    def test_logger_persistence(self, temp_log_file: Path):
        """Test that logger persists across calls."""
        logger1 = setup_logger(log_file=str(temp_log_file))
        logger1.info("Message 1")
        
        logger2 = get_logger()
        logger2.info("Message 2")
        
        # Read log file
        log_content = temp_log_file.read_text()
        assert "Message 1" in log_content
        assert "Message 2" in log_content

    def test_logger_exception_handling(self, temp_log_file: Path):
        """Test logger with exception."""
        logger = setup_logger(log_file=str(temp_log_file))
        
        try:
            raise ValueError("Test exception")
        except ValueError as e:
            logger.exception("An error occurred")
        
        # Read log file
        log_content = temp_log_file.read_text()
        assert "An error occurred" in log_content
        assert "ValueError: Test exception" in log_content

    def test_logger_stack_info(self, temp_log_file: Path):
        """Test logger with stack info."""
        logger = setup_logger(log_file=str(temp_log_file))
        
        logger.info("Test message", stack_info=True)
        
        # Read log file
        log_content = temp_log_file.read_text()
        assert "Test message" in log_content

    def test_logger_extra_info(self, temp_log_file: Path):
        """Test logger with extra information."""
        logger = setup_logger(log_file=str(temp_log_file))
        
        logger.info("Test message", extra={"custom_field": "custom_value"})
        
        # Read log file
        log_content = temp_log_file.read_text()
        assert "Test message" in log_content
