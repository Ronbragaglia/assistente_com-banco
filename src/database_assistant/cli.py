# -*- coding: utf-8 -*-
"""Command-line interface for OpenAI Database Assistant."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .config import Settings
from .logger import setup_logger, get_logger
from .database import DatabaseManager
from .similarity import SimilaritySearch
from .assistant import OpenAIAssistant


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="OpenAI Database Assistant - AI assistant with SQLite database and similarity search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  db-assistant --interactive

  # Ask a single question
  db-assistant --ask "Quais eventos estão disponíveis?"

  # Add a new event
  db-assistant --add-event "Conferência de IA" "2024-06-15" "Centro de Convenções" "Evento sobre inteligência artificial"

  # List all events
  db-assistant --list-events
        """,
    )

    # Configuration options
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (or set OPENAI_API_KEY environment variable)",
    )
    parser.add_argument(
        "--model",
        default="gpt-3.5-turbo",
        help="OpenAI model to use (default: gpt-3.5-turbo)",
    )
    parser.add_argument(
        "--database",
        type=Path,
        help="Path to SQLite database file",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to .env configuration file",
    )

    # Mode options
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode",
    )
    mode_group.add_argument(
        "--ask",
        metavar="QUESTION",
        help="Ask a single question and exit",
    )
    mode_group.add_argument(
        "--add-event",
        nargs=4,
        metavar=("NOME", "DATA", "LOCAL", "DESCRICAO"),
        help="Add a new event to the database",
    )
    mode_group.add_argument(
        "--list-events",
        action="store_true",
        help="List all events in the database",
    )

    # Logging options
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)",
    )
    parser.add_argument(
        "--log-file",
        help="Path to log file",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    # Other options
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching of responses",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 2.0.0",
    )

    args = parser.parse_args()

    # Setup logging
    logger = setup_logger(
        level=args.log_level,
        log_file=args.log_file,
        use_colors=not args.no_color,
    )

    try:
        # Load settings
        settings = Settings()
        
        # Override settings with CLI arguments
        if args.api_key:
            settings.openai_api_key = args.api_key
        if args.model:
            settings.openai_model = args.model
        if args.database:
            settings.database_path = args.database
        if args.no_cache:
            settings.cache_enabled = False
        
        # Ensure directories exist
        settings.ensure_directories()

        # Validate API key
        if not settings.openai_api_key or settings.openai_api_key.startswith("sk-"):
            logger.error("❌ Invalid or missing OpenAI API key")
            return 1

        # Initialize components
        db_manager = DatabaseManager(settings.database_path)
        similarity_search = SimilaritySearch(threshold=settings.similarity_threshold)
        ai_assistant = OpenAIAssistant(settings)

        # Connect to database and setup
        with db_manager:
            db_manager.create_tables()
            db_manager.seed_sample_data()

        # Load similarity search with existing Q&A pairs
        with db_manager:
            qa_pairs = db_manager.get_all_qa_pairs()
            similarity_search.fit(qa_pairs)

        # Run in requested mode
        if args.interactive:
            return run_interactive_mode(
                db_manager,
                similarity_search,
                ai_assistant,
                settings,
            )
        elif args.ask:
            return run_single_question(
                db_manager,
                similarity_search,
                ai_assistant,
                args.ask,
                settings,
            )
        elif args.add_event:
            return add_event(
                db_manager,
                args.add_event,
            )
        elif args.list_events:
            return list_events(db_manager)
        else:
            logger.info("ℹ️  No mode specified. Use --interactive, --ask, --add-event, or --list-events")
            return 0

    except KeyboardInterrupt:
        logger.info("\n⏹️  Interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        return 1


def run_interactive_mode(
    db_manager: DatabaseManager,
    similarity_search: SimilaritySearch,
    ai_assistant: OpenAIAssistant,
    settings: Settings,
) -> int:
    """Run the assistant in interactive mode.

    Args:
        db_manager: Database manager instance
        similarity_search: Similarity search instance
        ai_assistant: OpenAI assistant instance
        settings: Configuration settings

    Returns:
        Exit code
    """
    logger = get_logger(__name__)
    
    # Get context from database
    with db_manager:
        context = db_manager.get_events_as_context()
    
    logger.info("🎯 Interactive mode started. Type 'sair' or 'exit' to stop.")
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
                    # Generate new response
                    logger.info("🤔 Generating new response...")
                    response = ai_assistant.generate_response(context, question)
                    print(f"\nAssistente: {response}")

                    # Cache the response
                    if settings.cache_enabled:
                        with db_manager:
                            db_manager.insert_question_answer(question, response)
                        similarity_search.update([(question, response)])

            except EOFError:
                logger.info("\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"❌ Error: {e}")

        return 0

    except KeyboardInterrupt:
        logger.info("\n👋 Goodbye!")
        return 0


def run_single_question(
    db_manager: DatabaseManager,
    similarity_search: SimilaritySearch,
    ai_assistant: OpenAIAssistant,
    question: str,
    settings: Settings,
) -> int:
    """Ask a single question and exit.

    Args:
        db_manager: Database manager instance
        similarity_search: Similarity search instance
        ai_assistant: OpenAI assistant instance
        question: Question to ask
        settings: Configuration settings

    Returns:
        Exit code
    """
    logger = get_logger(__name__)
    
    # Get context from database
    with db_manager:
        context = db_manager.get_events_as_context()
    
    try:
        # Search for similar question
        cached_answer = similarity_search.search(question)
        
        if cached_answer:
            print(f"\nAssistente: {cached_answer} (Resposta recuperada do banco de dados)")
        else:
            # Generate new response
            logger.info("🤔 Generating response...")
            response = ai_assistant.generate_response(context, question)
            print(f"\nAssistente: {response}")

            # Cache the response
            if settings.cache_enabled:
                with db_manager:
                    db_manager.insert_question_answer(question, response)
        
        return 0

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return 1


def add_event(
    db_manager: DatabaseManager,
    event_data: tuple,
) -> int:
    """Add a new event to the database.

    Args:
        db_manager: Database manager instance
        event_data: Tuple of (nome, data, local, descricao)

    Returns:
        Exit code
    """
    logger = get_logger(__name__)
    
    try:
        with db_manager:
            event_id = db_manager.insert_event(*event_data)
        
        print(f"✅ Evento adicionado com sucesso! ID: {event_id}")
        return 0

    except Exception as e:
        logger.error(f"❌ Error adding event: {e}")
        return 1


def list_events(db_manager: DatabaseManager) -> int:
    """List all events in the database.

    Args:
        db_manager: Database manager instance

    Returns:
        Exit code
    """
    logger = get_logger(__name__)
    
    try:
        with db_manager:
            events = db_manager.get_all_events()
        
        if not events:
            print("Nenhum evento encontrado.")
            return 0
        
        print("\n📅 Eventos:")
        print("-" * 60)
        
        for event in events:
            nome, data, local, descricao = event
            print(f"\nNome: {nome}")
            print(f"Data: {data}")
            print(f"Local: {local}")
            print(f"Descrição: {descricao}")
            print("-" * 60)
        
        return 0

    except Exception as e:
        logger.error(f"❌ Error listing events: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
