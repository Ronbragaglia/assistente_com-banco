#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export and Import Example for OpenAI Database Assistant.

This example demonstrates how to export Q&A pairs from the database
to JSON and import them back.
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database_assistant import (
    DatabaseManager,
    SimilaritySearch,
    setup_logger,
)


def export_qa_pairs_to_json(
    db_manager: DatabaseManager,
    output_path: Path,
) -> None:
    """Export Q&A pairs from database to JSON file.

    Args:
        db_manager: Database manager instance
        output_path: Path to output JSON file
    """
    logger = setup_logger(name="export_import")

    with db_manager:
        qa_pairs = db_manager.get_all_qa_pairs()

    # Convert to list of dictionaries
    export_data = [
        {
            "id": idx,
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat(),
        }
        for idx, (question, answer) in enumerate(qa_pairs, 1)
    ]

    # Add metadata
    export_obj = {
        "version": "1.0",
        "exported_at": datetime.now().isoformat(),
        "total_pairs": len(export_data),
        "data": export_data,
    }

    # Write to JSON file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_obj, f, ensure_ascii=False, indent=2)

    logger.info(f"✅ Exported {len(export_data)} Q&A pairs to {output_path}")


def import_qa_pairs_from_json(
    db_manager: DatabaseManager,
    similarity_search: SimilaritySearch,
    input_path: Path,
) -> None:
    """Import Q&A pairs from JSON file to database.

    Args:
        db_manager: Database manager instance
        similarity_search: Similarity search instance
        input_path: Path to input JSON file
    """
    logger = setup_logger(name="export_import")

    # Read JSON file
    with open(input_path, 'r', encoding='utf-8') as f:
        import_obj = json.load(f)

    # Extract data
    qa_pairs = import_obj.get("data", [])
    version = import_obj.get("version", "unknown")
    exported_at = import_obj.get("exported_at", "unknown")

    logger.info(f"📥 Importing from version {version}, exported at {exported_at}")
    logger.info(f"📊 Found {len(qa_pairs)} Q&A pairs")

    # Import to database
    with db_manager:
        for qa in qa_pairs:
            question = qa["question"]
            answer = qa["answer"]
            db_manager.insert_question_answer(question, answer)

    # Update similarity search
    with db_manager:
        all_qa_pairs = db_manager.get_all_qa_pairs()
        similarity_search.fit(all_qa_pairs)

    logger.info(f"✅ Successfully imported {len(qa_pairs)} Q&A pairs")


def export_events_to_json(
    db_manager: DatabaseManager,
    output_path: Path,
) -> None:
    """Export events from database to JSON file.

    Args:
        db_manager: Database manager instance
        output_path: Path to output JSON file
    """
    logger = setup_logger(name="export_import")

    with db_manager:
        events = db_manager.get_all_events()

    # Convert to list of dictionaries
    export_data = [
        {
            "id": idx,
            "name": nome,
            "date": data,
            "location": local,
            "description": descricao,
        }
        for idx, (nome, data, local, descricao) in enumerate(events, 1)
    ]

    # Add metadata
    export_obj = {
        "version": "1.0",
        "exported_at": datetime.now().isoformat(),
        "total_events": len(export_data),
        "data": export_data,
    }

    # Write to JSON file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_obj, f, ensure_ascii=False, indent=2)

    logger.info(f"✅ Exported {len(export_data)} events to {output_path}")


def import_events_from_json(
    db_manager: DatabaseManager,
    input_path: Path,
) -> None:
    """Import events from JSON file to database.

    Args:
        db_manager: Database manager instance
        input_path: Path to input JSON file
    """
    logger = setup_logger(name="export_import")

    # Read JSON file
    with open(input_path, 'r', encoding='utf-8') as f:
        import_obj = json.load(f)

    # Extract data
    events = import_obj.get("data", [])
    version = import_obj.get("version", "unknown")
    exported_at = import_obj.get("exported_at", "unknown")

    logger.info(f"📥 Importing from version {version}, exported at {exported_at}")
    logger.info(f"📊 Found {len(events)} events")

    # Import to database
    with db_manager:
        for event in events:
            db_manager.insert_event(
                nome=event["name"],
                data=event["date"],
                local=event["location"],
                descricao=event["description"],
            )

    logger.info(f"✅ Successfully imported {len(events)} events")


def main():
    """Main function demonstrating export and import."""
    logger = setup_logger(name="export_import")

    # Initialize components
    db_manager = DatabaseManager(Path("data/eventos.db"))
    similarity_search = SimilaritySearch(threshold=0.7)

    # Setup database
    with db_manager:
        db_manager.create_tables()
        db_manager.seed_sample_data()

    # Export Q&A pairs
    qa_export_path = Path("exports/qa_pairs.json")
    export_qa_pairs_to_json(db_manager, qa_export_path)

    # Export events
    events_export_path = Path("exports/events.json")
    export_events_to_json(db_manager, events_export_path)

    # Import Q&A pairs (demonstration)
    qa_import_path = Path("exports/qa_pairs.json")
    if qa_import_path.exists():
        import_qa_pairs_from_json(db_manager, similarity_search, qa_import_path)

    logger.info("🎉 Export and import operations completed successfully!")


if __name__ == "__main__":
    main()
