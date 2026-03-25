#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Advanced usage example for OpenAI Database Assistant."""

import os
from pathlib import Path
from typing import List

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


def interactive_example():
    """Example of interactive mode with custom questions."""
    logger = setup_logger(level="INFO")
    logger.info("🚀 Starting interactive example")

    settings = Settings()
    db_manager = DatabaseManager(settings.database_path)
    similarity_search = SimilaritySearch(threshold=settings.similarity_threshold)
    ai_assistant = OpenAIAssistant(settings)

    # Setup database
    with db_manager:
        db_manager.create_tables()
        db_manager.seed_sample_data()

    # Load similarity search
    with db_manager:
        qa_pairs = db_manager.get_all_qa_pairs()
        similarity_search.fit(qa_pairs)

    # Get context
    with db_manager:
        context = db_manager.get_events_as_context()

    # Custom questions
    questions = [
        "Quais são os eventos disponíveis?",
        "Me fale mais sobre o Festival de Música",
        "Quais são os detalhes da Feira de Tecnologia?",
    ]

    for i, question in enumerate(questions, 1):
        logger.info(f"\n📝 Question {i}: {question}")
        
        cached_answer = similarity_search.search(question)
        
        if cached_answer:
            print(f"\n💡 Cached Answer: {cached_answer}")
        else:
            response = ai_assistant.generate_response(context, question)
            print(f"\n💡 Generated Response: {response}")
            
            if settings.cache_enabled:
                with db_manager:
                    db_manager.insert_question_answer(question, response)
                similarity_search.update([(question, response)])


def custom_system_prompt_example():
    """Example of using a custom system prompt."""
    logger = setup_logger(level="INFO")
    logger.info("🚀 Starting custom system prompt example")

    settings = Settings()
    db_manager = DatabaseManager(settings.database_path)
    ai_assistant = OpenAIAssistant(settings)

    # Setup database
    with db_manager:
        db_manager.create_tables()
        db_manager.seed_sample_data()

    # Get context
    with db_manager:
        context = db_manager.get_events_as_context()

    # Custom system prompt
    custom_prompt = """
    Você é um assistente de eventos especializado em fornecer informações detalhadas e úteis.
    Suas respostas devem ser:
    1. Claras e concisas
    2. Baseadas nas informações fornecidas
    3. Amigáveis e profissionais
    4. Focadas em ajudar o usuário
    """

    question = "Quais eventos você pode me recomendar?"
    response = ai_assistant.generate_response(context, question, system_prompt=custom_prompt)
    print(f"\n💡 Custom Prompt Response:\n{response}")


def similarity_threshold_example():
    """Example of experimenting with similarity thresholds."""
    logger = setup_logger(level="INFO")
    logger.info("🚀 Starting similarity threshold example")

    settings = Settings()
    db_manager = DatabaseManager(settings.database_path)
    
    # Setup database
    with db_manager:
        db_manager.create_tables()
        db_manager.seed_sample_data()

    # Add some Q&A pairs
    with db_manager:
        db_manager.insert_question_answer(
            "Quais eventos estão disponíveis?",
            "Temos dois eventos: Festival de Música em 15/12/2023 e Feira de Tecnologia em 20/02/2024."
        )
        db_manager.insert_question_answer(
            "Me fale sobre o Festival de Música",
            "O Festival de Música acontece em 15/12/2023 no Parque Central e contará com bandas internacionais."
        )

    # Test different thresholds
    thresholds = [0.5, 0.7, 0.9]
    test_questions = [
        "Que eventos tem?",
        "Fale do festival",
        "Informações sobre eventos musicais",
    ]

    for threshold in thresholds:
        logger.info(f"\n🎯 Testing with threshold: {threshold}")
        similarity_search = SimilaritySearch(threshold=threshold)
        
        with db_manager:
            qa_pairs = db_manager.get_all_qa_pairs()
            similarity_search.fit(qa_pairs)

        for question in test_questions:
            answer, score = similarity_search.search_with_score(question)
            if answer:
                logger.info(f"  Question: {question[:30]}... -> Score: {score:.4f}")
            else:
                logger.info(f"  Question: {question[:30]}... -> No match")


def batch_operations_example():
    """Example of batch operations."""
    logger = setup_logger(level="INFO")
    logger.info("🚀 Starting batch operations example")

    settings = Settings()
    db_manager = DatabaseManager(settings.database_path)

    # Setup database
    with db_manager:
        db_manager.create_tables()

    # Batch insert events
    events = [
        ("Workshop de Python", "2024-03-10", "Sala de Conferências", "Workshop introdutório sobre Python"),
        ("Meetup de IA", "2024-04-05", "Coworking Space", "Encontro de entusiastas de IA"),
        ("Hackathon", "2024-05-20", "Centro de Inovação", "Maratona de programação de 48h"),
    ]

    with db_manager:
        for event in events:
            db_manager.insert_event(*event)
        logger.info(f"✅ Inserted {len(events)} events")

    # List all events
    with db_manager:
        all_events = db_manager.get_all_events()
    
    print(f"\n📅 Total Events: {len(all_events)}")
    for event in all_events:
        print(f"  - {event[0]} ({event[1]})")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("OpenAI Database Assistant - Advanced Examples")
    print("=" * 60 + "\n")

    examples = [
        ("Interactive Mode", interactive_example),
        ("Custom System Prompt", custom_system_prompt_example),
        ("Similarity Thresholds", similarity_threshold_example),
        ("Batch Operations", batch_operations_example),
    ]

    for i, (name, func) in enumerate(examples, 1):
        print(f"\n{i}. {name}")
        print("-" * 60)

        try:
            func()
        except Exception as e:
            print(f"❌ Error in {name}: {e}")

        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
