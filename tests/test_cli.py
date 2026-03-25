# -*- coding: utf-8 -*-
"""Tests for CLI module."""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
import sys

import sys
sys.path.insert(0, str(__file__).split("/tests")[0] + "/src")

from database_assistant.cli import main, run_interactive_mode, run_single_question, add_event, list_events


@pytest.fixture
def temp_db_path(tmp_path: Path) -> Path:
    """Create a temporary database path."""
    return tmp_path / "test.db"


@pytest.fixture
def mock_settings(temp_db_path: Path):
    """Create mock settings."""
    with patch('database_assistant.cli.Settings') as mock_settings_class:
        mock_settings = MagicMock()
        mock_settings.openai_api_key = "test-api-key"
        mock_settings.openai_model = "gpt-3.5-turbo"
        mock_settings.openai_temperature = 0.7
        mock_settings.database_path = temp_db_path
        mock_settings.cache_enabled = True
        mock_settings.similarity_threshold = 0.7
        mock_settings.assistant_system_prompt = "Test prompt"
        
        mock_settings_class.return_value = mock_settings
        yield mock_settings


@pytest.fixture
def mock_components():
    """Create mock components."""
    with patch('database_assistant.cli.DatabaseManager') as mock_db_class, \
         patch('database_assistant.cli.SimilaritySearch') as mock_search_class, \
         patch('database_assistant.cli.OpenAIAssistant') as mock_assistant_class:
        
        mock_db = MagicMock()
        mock_search = MagicMock()
        mock_assistant = MagicMock()
        
        mock_db_class.return_value = mock_db
        mock_search_class.return_value = mock_search
        mock_assistant_class.return_value = mock_assistant
        
        yield {
            'db': mock_db,
            'search': mock_search,
            'assistant': mock_assistant,
        }


class TestMain:
    """Test cases for main function."""

    @patch('sys.argv', ['db-assistant', '--version'])
    def test_main_version(self):
        """Test main with --version flag."""
        with pytest.raises(SystemExit):
            main()

    @patch('sys.argv', ['db-assistant', '--help'])
    def test_main_help(self):
        """Test main with --help flag."""
        with pytest.raises(SystemExit):
            main()

    @patch('sys.argv', ['db-assistant', '--interactive'])
    @patch('database_assistant.cli.run_interactive_mode')
    def test_main_interactive(self, mock_run_interactive):
        """Test main with --interactive flag."""
        result = main()
        assert result == 0
        mock_run_interactive.assert_called_once()

    @patch('sys.argv', ['db-assistant', '--ask', 'Test question'])
    @patch('database_assistant.cli.run_single_question')
    def test_main_ask(self, mock_run_single):
        """Test main with --ask flag."""
        result = main()
        assert result == 0
        mock_run_single.assert_called_once()

    @patch('sys.argv', ['db-assistant', '--add-event', 'Event', '2024-01-01', 'Location', 'Description'])
    @patch('database_assistant.cli.add_event')
    def test_main_add_event(self, mock_add_event):
        """Test main with --add-event flag."""
        result = main()
        assert result == 0
        mock_add_event.assert_called_once()

    @patch('sys.argv', ['db-assistant', '--list-events'])
    @patch('database_assistant.cli.list_events')
    def test_main_list_events(self, mock_list_events):
        """Test main with --list-events flag."""
        result = main()
        assert result == 0
        mock_list_events.assert_called_once()

    @patch('sys.argv', ['db-assistant'])
    def test_main_no_mode(self):
        """Test main without mode specified."""
        result = main()
        assert result == 0

    @patch('sys.argv', ['db-assistant', '--interactive'])
    @patch('database_assistant.cli.Settings')
    @patch('database_assistant.cli.DatabaseManager')
    @patch('database_assistant.cli.SimilaritySearch')
    @patch('database_assistant.cli.OpenAIAssistant')
    @patch('database_assistant.cli.run_interactive_mode')
    def test_main_invalid_api_key(self, mock_run, mock_assistant, mock_search, mock_db, mock_settings):
        """Test main with invalid API key."""
        mock_settings_instance = MagicMock()
        mock_settings_instance.openai_api_key = "invalid"
        mock_settings_instance.database_path = Path("test.db")
        mock_settings_instance.cache_enabled = True
        mock_settings_instance.openai_model = "gpt-3.5-turbo"
        mock_settings_instance.similarity_threshold = 0.7
        mock_settings_instance.ensure_directories = MagicMock()
        
        mock_settings.return_value = mock_settings_instance
        
        result = main()
        assert result == 1

    @patch('sys.argv', ['db-assistant', '--interactive'])
    @patch('database_assistant.cli.run_interactive_mode')
    def test_main_keyboard_interrupt(self, mock_run):
        """Test main with keyboard interrupt."""
        mock_run.side_effect = KeyboardInterrupt()
        result = main()
        assert result == 0

    @patch('sys.argv', ['db-assistant', '--interactive'])
    @patch('database_assistant.cli.run_interactive_mode')
    def test_main_exception(self, mock_run):
        """Test main with exception."""
        mock_run.side_effect = Exception("Test error")
        result = main()
        assert result == 1


class TestRunInteractiveMode:
    """Test cases for run_interactive_mode function."""

    @patch('builtins.input', side_effect=['Test question', 'exit'])
    @patch('builtins.print')
    def test_run_interactive_mode_success(self, mock_print, mock_input, mock_components):
        """Test interactive mode with successful interaction."""
        mock_db = mock_components['db']
        mock_search = mock_components['search']
        mock_assistant = mock_components['assistant']
        
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_db.get_events_as_context.return_value = "Context information"
        
        mock_search.search.return_value = None
        mock_assistant.generate_response.return_value = "Test response"
        
        mock_settings = MagicMock()
        mock_settings.cache_enabled = True
        
        result = run_interactive_mode(mock_db, mock_search, mock_assistant, mock_settings)
        assert result == 0

    @patch('builtins.input', side_effect=['Test question', 'exit'])
    @patch('builtins.print')
    def test_run_interactive_mode_with_cache(self, mock_print, mock_input, mock_components):
        """Test interactive mode with cached response."""
        mock_db = mock_components['db']
        mock_search = mock_components['search']
        mock_assistant = mock_components['assistant']
        
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_db.get_events_as_context.return_value = "Context information"
        
        mock_search.search.return_value = "Cached response"
        
        mock_settings = MagicMock()
        mock_settings.cache_enabled = True
        
        result = run_interactive_mode(mock_db, mock_search, mock_assistant, mock_settings)
        assert result == 0

    @patch('builtins.input', side_effect=['exit'])
    @patch('builtins.print')
    def test_run_interactive_mode_empty_input(self, mock_print, mock_input, mock_components):
        """Test interactive mode with empty input."""
        mock_db = mock_components['db']
        mock_search = mock_components['search']
        mock_assistant = mock_components['assistant']
        
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_db.get_events_as_context.return_value = "Context information"
        
        mock_settings = MagicMock()
        mock_settings.cache_enabled = True
        
        result = run_interactive_mode(mock_db, mock_search, mock_assistant, mock_settings)
        assert result == 0

    @patch('builtins.input', side_effect=['sair'])
    @patch('builtins.print')
    def test_run_interactive_mode_sair(self, mock_print, mock_input, mock_components):
        """Test interactive mode with 'sair' command."""
        mock_db = mock_components['db']
        mock_search = mock_components['search']
        mock_assistant = mock_components['assistant']
        
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_db.get_events_as_context.return_value = "Context information"
        
        mock_settings = MagicMock()
        mock_settings.cache_enabled = True
        
        result = run_interactive_mode(mock_db, mock_search, mock_assistant, mock_settings)
        assert result == 0

    @patch('builtins.input', side_effect=['q'])
    @patch('builtins.print')
    def test_run_interactive_mode_q(self, mock_print, mock_input, mock_components):
        """Test interactive mode with 'q' command."""
        mock_db = mock_components['db']
        mock_search = mock_components['search']
        mock_assistant = mock_components['assistant']
        
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_db.get_events_as_context.return_value = "Context information"
        
        mock_settings = MagicMock()
        mock_settings.cache_enabled = True
        
        result = run_interactive_mode(mock_db, mock_search, mock_assistant, mock_settings)
        assert result == 0


class TestRunSingleQuestion:
    """Test cases for run_single_question function."""

    @patch('builtins.print')
    def test_run_single_question_success(self, mock_print, mock_components):
        """Test single question with success."""
        mock_db = mock_components['db']
        mock_search = mock_components['search']
        mock_assistant = mock_components['assistant']
        
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_db.get_events_as_context.return_value = "Context information"
        
        mock_search.search.return_value = None
        mock_assistant.generate_response.return_value = "Test response"
        
        mock_settings = MagicMock()
        mock_settings.cache_enabled = True
        
        result = run_single_question(mock_db, mock_search, mock_assistant, "Test question", mock_settings)
        assert result == 0

    @patch('builtins.print')
    def test_run_single_question_with_cache(self, mock_print, mock_components):
        """Test single question with cached response."""
        mock_db = mock_components['db']
        mock_search = mock_components['search']
        mock_assistant = mock_components['assistant']
        
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_db.get_events_as_context.return_value = "Context information"
        
        mock_search.search.return_value = "Cached response"
        
        mock_settings = MagicMock()
        mock_settings.cache_enabled = True
        
        result = run_single_question(mock_db, mock_search, mock_assistant, "Test question", mock_settings)
        assert result == 0

    @patch('builtins.print')
    def test_run_single_question_error(self, mock_print, mock_components):
        """Test single question with error."""
        mock_db = mock_components['db']
        mock_search = mock_components['search']
        mock_assistant = mock_components['assistant']
        
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_db.get_events_as_context.side_effect = Exception("Database error")
        
        mock_settings = MagicMock()
        
        result = run_single_question(mock_db, mock_search, mock_assistant, "Test question", mock_settings)
        assert result == 1


class TestAddEvent:
    """Test cases for add_event function."""

    @patch('builtins.print')
    def test_add_event_success(self, mock_print, mock_components):
        """Test adding event successfully."""
        mock_db = mock_components['db']
        
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_db.insert_event.return_value = 1
        
        event_data = ("Test Event", "2024-01-01", "Test Location", "Test Description")
        result = add_event(mock_db, event_data)
        
        assert result == 0
        mock_db.insert_event.assert_called_once_with(*event_data)

    @patch('builtins.print')
    def test_add_event_error(self, mock_print, mock_components):
        """Test adding event with error."""
        mock_db = mock_components['db']
        
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_db.insert_event.side_effect = Exception("Database error")
        
        event_data = ("Test Event", "2024-01-01", "Test Location", "Test Description")
        result = add_event(mock_db, event_data)
        
        assert result == 1


class TestListEvents:
    """Test cases for list_events function."""

    @patch('builtins.print')
    def test_list_events_success(self, mock_print, mock_components):
        """Test listing events successfully."""
        mock_db = mock_components['db']
        
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_db.get_all_events.return_value = [
            ("Event 1", "2024-01-01", "Location 1", "Description 1"),
            ("Event 2", "2024-02-01", "Location 2", "Description 2"),
        ]
        
        result = list_events(mock_db)
        assert result == 0

    @patch('builtins.print')
    def test_list_events_empty(self, mock_print, mock_components):
        """Test listing events when empty."""
        mock_db = mock_components['db']
        
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_db.get_all_events.return_value = []
        
        result = list_events(mock_db)
        assert result == 0

    @patch('builtins.print')
    def test_list_events_error(self, mock_print, mock_components):
        """Test listing events with error."""
        mock_db = mock_components['db']
        
        mock_db.__enter__ = MagicMock(return_value=mock_db)
        mock_db.__exit__ = MagicMock(return_value=False)
        mock_db.get_all_events.side_effect = Exception("Database error")
        
        result = list_events(mock_db)
        assert result == 1


class TestCLIIntegration:
    """Integration tests for CLI functionality."""

    @patch('sys.argv', ['db-assistant', '--ask', 'Test question'])
    @patch('database_assistant.cli.run_single_question')
    def test_cli_integration_ask(self, mock_run_single):
        """Test CLI integration for ask command."""
        result = main()
        assert result == 0
        mock_run_single.assert_called_once()

    @patch('sys.argv', ['db-assistant', '--add-event', 'Event', '2024-01-01', 'Location', 'Description'])
    @patch('database_assistant.cli.add_event')
    def test_cli_integration_add_event(self, mock_add_event):
        """Test CLI integration for add-event command."""
        result = main()
        assert result == 0
        mock_add_event.assert_called_once()

    @patch('sys.argv', ['db-assistant', '--list-events'])
    @patch('database_assistant.cli.list_events')
    def test_cli_integration_list_events(self, mock_list_events):
        """Test CLI integration for list-events command."""
        result = main()
        assert result == 0
        mock_list_events.assert_called_once()
