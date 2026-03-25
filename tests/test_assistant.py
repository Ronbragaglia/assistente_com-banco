# -*- coding: utf-8 -*-
"""Tests for OpenAI assistant module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Optional

import sys
sys.path.insert(0, str(__file__).split("/tests")[0] + "/src")

from database_assistant.assistant import OpenAIAssistant
from database_assistant.config import Settings


@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    return Settings(
        openai_api_key="test-api-key",
        openai_model="gpt-3.5-turbo",
        openai_temperature=0.7,
    )


@pytest.fixture
def mock_openai_client():
    """Create a mock OpenAI client."""
    with patch('database_assistant.assistant.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        yield mock_client


@pytest.fixture
def assistant(mock_settings, mock_openai_client):
    """Create an OpenAI assistant instance with mocked client."""
    return OpenAIAssistant(mock_settings)


class TestOpenAIAssistant:
    """Test cases for OpenAIAssistant class."""

    def test_initialization(self, mock_settings):
        """Test assistant initialization."""
        with patch('database_assistant.assistant.OpenAI') as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            
            assistant = OpenAIAssistant(mock_settings)
            
            assert assistant.settings == mock_settings
            assert assistant.client == mock_client

    def test_initialization_default_settings(self):
        """Test assistant initialization with default settings."""
        with patch('database_assistant.assistant.OpenAI') as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            
            assistant = OpenAIAssistant()
            
            assert assistant.settings is not None
            assert assistant.client == mock_client

    def test_generate_response_success(self, assistant, mock_openai_client):
        """Test successful response generation."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        context = "Context information"
        question = "Test question"
        
        response = assistant.generate_response(context, question)
        
        assert response == "Test response"
        mock_openai_client.chat.completions.create.assert_called_once()

    def test_generate_response_with_custom_system_prompt(self, assistant, mock_openai_client):
        """Test response generation with custom system prompt."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        context = "Context information"
        question = "Test question"
        custom_prompt = "Custom system prompt"
        
        response = assistant.generate_response(context, question, system_prompt=custom_prompt)
        
        assert response == "Test response"
        
        # Verify the call
        call_args = mock_openai_client.chat.completions.create.call_args
        messages = call_args.kwargs['messages']
        assert messages[0]['content'] == custom_prompt

    def test_generate_response_api_error(self, assistant, mock_openai_client):
        """Test response generation with API error."""
        # Mock API error
        mock_openai_client.chat.completions.create.side_effect = Exception("API Error")
        
        context = "Context information"
        question = "Test question"
        
        with pytest.raises(Exception) as exc_info:
            assistant.generate_response(context, question)
        
        assert "API Error" in str(exc_info.value)

    def test_generate_response_with_history_success(self, assistant, mock_openai_client):
        """Test response generation with conversation history."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        context = "Context information"
        conversation_history = [
            {"role": "user", "content": "Previous question"},
            {"role": "assistant", "content": "Previous answer"},
        ]
        
        response = assistant.generate_response_with_history(context, conversation_history)
        
        assert response == "Test response"
        mock_openai_client.chat.completions.create.assert_called_once()

    def test_generate_response_with_history_custom_prompt(self, assistant, mock_openai_client):
        """Test response generation with history and custom prompt."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        context = "Context information"
        conversation_history = [
            {"role": "user", "content": "Previous question"},
        ]
        custom_prompt = "Custom system prompt"
        
        response = assistant.generate_response_with_history(
            context, conversation_history, system_prompt=custom_prompt
        )
        
        assert response == "Test response"
        
        # Verify the call
        call_args = mock_openai_client.chat.completions.create.call_args
        messages = call_args.kwargs['messages']
        assert messages[0]['content'] == custom_prompt

    def test_generate_response_with_history_api_error(self, assistant, mock_openai_client):
        """Test response generation with history and API error."""
        # Mock API error
        mock_openai_client.chat.completions.create.side_effect = Exception("API Error")
        
        context = "Context information"
        conversation_history = []
        
        with pytest.raises(Exception) as exc_info:
            assistant.generate_response_with_history(context, conversation_history)
        
        assert "API Error" in str(exc_info.value)

    def test_set_model(self, assistant):
        """Test changing the model."""
        new_model = "gpt-4"
        assistant.set_model(new_model)
        
        assert assistant.settings.openai_model == new_model

    def test_set_temperature_valid(self, assistant):
        """Test setting temperature with valid value."""
        new_temperature = 0.5
        assistant.set_temperature(new_temperature)
        
        assert assistant.settings.openai_temperature == new_temperature

    def test_set_temperature_invalid_low(self, assistant):
        """Test setting temperature with invalid low value."""
        with pytest.raises(ValueError) as exc_info:
            assistant.set_temperature(-0.1)
        
        assert "Temperature must be between 0.0 and 2.0" in str(exc_info.value)

    def test_set_temperature_invalid_high(self, assistant):
        """Test setting temperature with invalid high value."""
        with pytest.raises(ValueError) as exc_info:
            assistant.set_temperature(2.1)
        
        assert "Temperature must be between 0.0 and 2.0" in str(exc_info.value)

    def test_set_temperature_boundary_low(self, assistant):
        """Test setting temperature at lower boundary."""
        assistant.set_temperature(0.0)
        assert assistant.settings.openai_temperature == 0.0

    def test_set_temperature_boundary_high(self, assistant):
        """Test setting temperature at upper boundary."""
        assistant.set_temperature(2.0)
        assert assistant.settings.openai_temperature == 2.0

    def test_generate_response_uses_settings_model(self, assistant, mock_openai_client):
        """Test that response generation uses the configured model."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        context = "Context information"
        question = "Test question"
        
        assistant.generate_response(context, question)
        
        # Verify the model used
        call_args = mock_openai_client.chat.completions.create.call_args
        assert call_args.kwargs['model'] == assistant.settings.openai_model

    def test_generate_response_uses_settings_temperature(self, assistant, mock_openai_client):
        """Test that response generation uses the configured temperature."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        context = "Context information"
        question = "Test question"
        
        assistant.generate_response(context, question)
        
        # Verify the temperature used
        call_args = mock_openai_client.chat.completions.create.call_args
        assert call_args.kwargs['temperature'] == assistant.settings.openai_temperature

    def test_generate_response_uses_settings_system_prompt(self, assistant, mock_openai_client):
        """Test that response generation uses the configured system prompt."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        context = "Context information"
        question = "Test question"
        
        assistant.generate_response(context, question)
        
        # Verify the system prompt used
        call_args = mock_openai_client.chat.completions.create.call_args
        messages = call_args.kwargs['messages']
        assert messages[0]['content'] == assistant.settings.assistant_system_prompt

    def test_generate_response_with_long_context(self, assistant, mock_openai_client):
        """Test response generation with long context."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        long_context = "A" * 10000  # 10KB of context
        question = "Test question"
        
        response = assistant.generate_response(long_context, question)
        
        assert response == "Test response"

    def test_generate_response_with_special_characters(self, assistant, mock_openai_client):
        """Test response generation with special characters."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response with émojis 🎉"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        context = "Context with @, #, $, %, &"
        question = "Question with émojis 🎉"
        
        response = assistant.generate_response(context, question)
        
        assert response == "Test response with émojis 🎉"

    def test_generate_response_with_unicode(self, assistant, mock_openai_client):
        """Test response generation with Unicode characters."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Resposta em 中文, 日本語, 한국어"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        context = "Contexto em 中文"
        question = "Pergunta em 日本語"
        
        response = assistant.generate_response(context, question)
        
        assert response == "Resposta em 中文, 日本語, 한국어"

    def test_multiple_generate_responses(self, assistant, mock_openai_client):
        """Test multiple response generations."""
        # Mock the API responses
        mock_responses = [
            MagicMock(choices=[MagicMock(message=MagicMock(content=f"Response {i}"))])
            for i in range(3)
        ]
        mock_openai_client.chat.completions.create.side_effect = mock_responses
        
        context = "Context information"
        
        for i in range(3):
            question = f"Test question {i}"
            response = assistant.generate_response(context, question)
            assert response == f"Response {i}"

    def test_generate_response_empty_context(self, assistant, mock_openai_client):
        """Test response generation with empty context."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        context = ""
        question = "Test question"
        
        response = assistant.generate_response(context, question)
        
        assert response == "Test response"

    def test_generate_response_empty_question(self, assistant, mock_openai_client):
        """Test response generation with empty question."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        context = "Context information"
        question = ""
        
        response = assistant.generate_response(context, question)
        
        assert response == "Test response"

    def test_generate_response_with_history_empty_history(self, assistant, mock_openai_client):
        """Test response generation with empty history."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        context = "Context information"
        conversation_history = []
        
        response = assistant.generate_response_with_history(context, conversation_history)
        
        assert response == "Test response"

    def test_generate_response_with_history_long_history(self, assistant, mock_openai_client):
        """Test response generation with long conversation history."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        context = "Context information"
        conversation_history = [
            {"role": "user", "content": f"Question {i}"}
            for i in range(50)
        ]
        
        response = assistant.generate_response_with_history(context, conversation_history)
        
        assert response == "Test response"
