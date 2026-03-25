# -*- coding: utf-8 -*-
"""OpenAI Assistant module for generating responses."""

from typing import Optional
from openai import OpenAI
import logging

from .config import Settings
from .logger import get_logger

logger = get_logger(__name__)


class OpenAIAssistant:
    """Manager for OpenAI API interactions."""

    def __init__(self, settings: Optional[Settings] = None):
        """Initialize the OpenAI Assistant.

        Args:
            settings: Configuration settings (uses default if not provided)
        """
        self.settings = settings or Settings()
        self.client = OpenAI(api_key=self.settings.openai_api_key)

        logger.info(f"🤖 OpenAI Assistant initialized with model: {self.settings.openai_model}")

    def generate_response(
        self,
        context: str,
        question: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """Generate a response for a question based on context.

        Args:
            context: The context or background information
            question: The question to answer
            system_prompt: Optional system prompt (uses settings default if not provided)

        Returns:
            The generated response

        Raises:
            Exception: If the API call fails
        """
        system_prompt = system_prompt or self.settings.assistant_system_prompt

        try:
            logger.debug(f"📝 Generating response for question: {question[:50]}...")

            # Create the prompt
            prompt = f"{context}\n\nPergunta: {question}\nResposta:"

            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.settings.openai_temperature,
            )

            # Extract the response
            answer = response.choices[0].message.content
            logger.info(f"✅ Response generated: {len(answer)} characters")

            return answer

        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            raise

    def generate_response_with_history(
        self,
        context: str,
        conversation_history: list,
        system_prompt: Optional[str] = None,
    ) -> str:
        """Generate a response with conversation history.

        Args:
            context: The context or background information
            conversation_history: List of message dictionaries with 'role' and 'content'
            system_prompt: Optional system prompt (uses settings default if not provided)

        Returns:
            The generated response

        Raises:
            Exception: If the API call fails
        """
        system_prompt = system_prompt or self.settings.assistant_system_prompt

        try:
            logger.debug(f"📝 Generating response with conversation history")

            # Build messages list
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context},
            ]

            # Add conversation history
            messages.extend(conversation_history)

            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=messages,
                temperature=self.settings.openai_temperature,
            )

            # Extract the response
            answer = response.choices[0].message.content
            logger.info(f"✅ Response generated: {len(answer)} characters")

            return answer

        except Exception as e:
            logger.error(f"❌ Error generating response with history: {e}")
            raise

    def set_model(self, model: str) -> None:
        """Change the OpenAI model.

        Args:
            model: The model name (e.g., "gpt-3.5-turbo", "gpt-4")
        """
        self.settings.openai_model = model
        logger.info(f"🔄 Model changed to: {model}")

    def set_temperature(self, temperature: float) -> None:
        """Change the temperature for responses.

        Args:
            temperature: Temperature value (0.0 to 2.0)
        """
        if not 0.0 <= temperature <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        
        self.settings.openai_temperature = temperature
        logger.info(f"🔄 Temperature changed to: {temperature}")
