#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Basic usage example for OpenAI Database Assistant."""

import os
from pathlib import Path

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database_assistant import (
    Settings,
    DatabaseManager,
    SimilaritySearch,
    OpenAIAssistant,
    setup_logger,
)


def main():
    """Demonstrate basic usage of the assistant."""
    
    # Setup logging
    logger = setup_logger(level="INFO", log_file="logs/example.log")
    logger.info("🚀 Starting basic usage example")

    try:
        # Load settings from environment variables or .env file
        settings = Settings()
        settings.ensure_directories()

        # Initialize database manager
        db_manager = DatabaseManager(settings.database_path)

        # Initialize similarity search
        similarity_search = SimilaritySearch(threshold=settings.similarity_threshold)

        # Initialize OpenAI Assistant
        ai_assistant = OpenAIAssistant(settings)

        # Setup database
        with db_manager:
            db_manager.create_tables()
            db_manager.seed_sample_data()

        # Load similarity search with existing Q&A pairs
        with db_manager:
            qa_pairs = db_manager.get_all_qa_pairs()
            similarity_search.fit(qa_pairs)

        # Get context from database
        with db_manager:
            context = db_manager.get_events_as_context()

        print("\n" + "=" * 60)
        print("Contexto do Banco de Dados:")
        print("=" * 60)
        print(context)

        # Example questions
        questions = [
            "Quais eventos estão disponíveis?",
            "Me fale sobre o Festival de Música",
            "Quando será a Feira de Tecnologia?",
        ]

        for i, question in enumerate(questions, 1):
            print(f"\n{'=' * 60}")
            print(f"Pergunta {i}: {question}")
            print('=' * 60)

            # Search for similar question
            cached_answer = similarity_search.search(question)
            
            if cached_answer:
                print(f"\n💡 Resposta (do cache): {cached_answer}")
            else:
                # Generate new response
                logger.info("🤔 Generating new response...")
                response = ai_assistant.generate_response(context, question)
                print(f"\n💡 Resposta (gerada): {response}")

                # Cache the response
                if settings.cache_enabled:
                    with db_manager:
                        db_manager.insert_question_answer(question, response)
                    similarity_search.update([(question, response)])

        logger.info("✅ Example completed successfully")

    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
