#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Streaming Response Example for OpenAI Database Assistant.

This example demonstrates how to implement streaming responses
from the OpenAI API for real-time user feedback.
"""

from typing import Iterator, Optional
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database_assistant import (
    DatabaseManager,
    SimilaritySearch,
    OpenAIAssistant,
    Settings,
    setup_logger,
)


class StreamingOpenAIAssistant(OpenAIAssistant):
    """Extended OpenAI Assistant with streaming support."""

    def generate_response_stream(
        self,
        context: str,
        question: str,
        system_prompt: Optional[str] = None,
    ) -> Iterator[str]:
        """Generate a streaming response for a question.

        Args:
            context: The context or background information
            question: The question to answer
            system_prompt: Optional system prompt

        Yields:
            Chunks of the generated response
        """
        logger = setup_logger(name="streaming")
        system_prompt = system_prompt or self.settings.assistant_system_prompt

        try:
            logger.debug(f"📝 Generating streaming response for: {question[:50]}...")

            # Create the prompt
            prompt = f"{context}\n\nPergunta: {question}\nResposta:"

            # Call the OpenAI API with streaming
            stream = self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.settings.openai_temperature,
                stream=True,
            )

            # Yield chunks as they arrive
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    yield content

            logger.info("✅ Streaming response completed")

        except Exception as e:
            logger.error(f"❌ Error generating streaming response: {e}")
            raise


def print_streaming_response(response: Iterator[str]) -> str:
    """Print streaming response character by character.

    Args:
        response: Iterator of response chunks

    Returns:
        Complete response string
    """
    import time

    complete_response = []
    print("Assistente: ", end="", flush=True)

    for chunk in response:
        complete_response.append(chunk)
        print(chunk, end="", flush=True)
        time.sleep(0.01)  # Simulate typing effect

    print()  # New line
    return "".join(complete_response)


def interactive_streaming_mode(
    db_manager: DatabaseManager,
    similarity_search: SimilaritySearch,
    ai_assistant: StreamingOpenAIAssistant,
    settings: Settings,
) -> None:
    """Run the assistant in interactive streaming mode.

    Args:
        db_manager: Database manager instance
        similarity_search: Similarity search instance
        ai_assistant: OpenAI assistant instance
        settings: Configuration settings
    """
    logger = setup_logger(name="streaming")

    # Get context from database
    with db_manager:
        context = db_manager.get_events_as_context()

    logger.info("🎯 Interactive streaming mode started. Type 'sair' or 'exit' to stop.")
    print(f"\n{context}")

    try:
        while True:
            try:
                question = input("\nVocê: ").strip()

                if not question:
                    continue

                if question.lower() in ["sair", "exit", "q"]:
                    logger.info("👋 Goodbye!")
                    break

                # Search for similar question
                cached_answer = similarity_search.search(question)

                if cached_answer:
                    print(f"\nAssistente: {cached_answer} (Resposta recuperada do banco de dados)")
                else:
                    # Generate new streaming response
                    logger.info("🤔 Generating streaming response...")
                    response_stream = ai_assistant.generate_response_stream(context, question)
                    complete_response = print_streaming_response(response_stream)

                    # Cache the response
                    if settings.cache_enabled:
                        with db_manager:
                            db_manager.insert_question_answer(question, complete_response)
                        similarity_search.update([(question, complete_response)])

            except EOFError:
                logger.info("\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"❌ Error: {e}")

    except KeyboardInterrupt:
        logger.info("\n👋 Goodbye!")


def main():
    """Main function demonstrating streaming responses."""
    logger = setup_logger(name="streaming")

    # Load settings
    settings = Settings()
    settings.ensure_directories()

    # Initialize components
    db_manager = DatabaseManager(settings.database_path)
    similarity_search = SimilaritySearch(threshold=settings.similarity_threshold)
    ai_assistant = StreamingOpenAIAssistant(settings)

    # Setup database
    with db_manager:
        db_manager.create_tables()
        db_manager.seed_sample_data()

    # Load similarity search
    with db_manager:
        qa_pairs = db_manager.get_all_qa_pairs()
        similarity_search.fit(qa_pairs)

    # Run interactive streaming mode
    interactive_streaming_mode(db_manager, similarity_search, ai_assistant, settings)


if __name__ == "__main__":
    main()
