# -*- coding: utf-8 -*-
"""Database manager module for SQLite operations."""

import sqlite3
from typing import List, Tuple, Optional
from pathlib import Path
import logging

from .logger import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """Manager for SQLite database operations."""

    def __init__(self, db_path: Path):
        """Initialize the database manager.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

        logger.info(f"🗄️  Database manager initialized: {db_path}")

    def connect(self) -> None:
        """Establish connection to the database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            logger.info("✅ Connected to database")
        except sqlite3.Error as e:
            logger.error(f"❌ Error connecting to database: {e}")
            raise

    def disconnect(self) -> None:
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("🔌 Disconnected from database")

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

    def create_tables(self) -> None:
        """Create all necessary tables in the database."""
        try:
            # Create events table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    data TEXT NOT NULL,
                    local TEXT NOT NULL,
                    descricao TEXT NOT NULL
                )
            ''')
            logger.info("✅ Created/verified 'eventos' table")

            # Create questions and answers table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS perguntas_respostas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pergunta TEXT NOT NULL,
                    resposta TEXT NOT NULL
                )
            ''')
            logger.info("✅ Created/verified 'perguntas_respostas' table")

            self.connection.commit()

        except sqlite3.Error as e:
            logger.error(f"❌ Error creating tables: {e}")
            raise

    def insert_event(self, nome: str, data: str, local: str, descricao: str) -> int:
        """Insert a new event into the database.

        Args:
            nome: Event name
            data: Event date
            local: Event location
            descricao: Event description

        Returns:
            ID of the inserted event
        """
        try:
            self.cursor.execute(
                "INSERT INTO eventos (nome, data, local, descricao) VALUES (?, ?, ?, ?)",
                (nome, data, local, descricao)
            )
            self.connection.commit()
            event_id = self.cursor.lastrowid
            logger.info(f"✅ Inserted event: {nome} (ID: {event_id})")
            return event_id
        except sqlite3.Error as e:
            logger.error(f"❌ Error inserting event: {e}")
            raise

    def get_all_events(self) -> List[Tuple[str, str, str, str]]:
        """Get all events from the database.

        Returns:
            List of tuples containing (nome, data, local, descricao)
        """
        try:
            self.cursor.execute("SELECT nome, data, local, descricao FROM eventos")
            events = self.cursor.fetchall()
            logger.info(f"📊 Retrieved {len(events)} events")
            return events
        except sqlite3.Error as e:
            logger.error(f"❌ Error retrieving events: {e}")
            raise

    def get_events_as_context(self) -> str:
        """Get all events formatted as context string.

        Returns:
            Formatted context string with all events
        """
        events = self.get_all_events()
        context = "Informações sobre eventos:\n\n"
        
        for event in events:
            nome, data, local, descricao = event
            context += f"- Nome: {nome}\n  Data: {data}\n  Local: {local}\n  Descrição: {descricao}\n\n"
        
        return context

    def insert_question_answer(self, pergunta: str, resposta: str) -> int:
        """Insert a new question and answer pair.

        Args:
            pergunta: The question
            resposta: The answer

        Returns:
            ID of the inserted record
        """
        try:
            self.cursor.execute(
                "INSERT INTO perguntas_respostas (pergunta, resposta) VALUES (?, ?)",
                (pergunta, resposta)
            )
            self.connection.commit()
            qa_id = self.cursor.lastrowid
            logger.info(f"✅ Inserted Q&A pair (ID: {qa_id})")
            return qa_id
        except sqlite3.Error as e:
            logger.error(f"❌ Error inserting Q&A pair: {e}")
            raise

    def get_all_qa_pairs(self) -> List[Tuple[str, str]]:
        """Get all question and answer pairs.

        Returns:
            List of tuples containing (pergunta, resposta)
        """
        try:
            self.cursor.execute("SELECT pergunta, resposta FROM perguntas_respostas")
            qa_pairs = self.cursor.fetchall()
            logger.info(f"📊 Retrieved {len(qa_pairs)} Q&A pairs")
            return qa_pairs
        except sqlite3.Error as e:
            logger.error(f"❌ Error retrieving Q&A pairs: {e}")
            raise

    def get_qa_count(self) -> int:
        """Get the count of question and answer pairs.

        Returns:
            Number of Q&A pairs in the database
        """
        try:
            self.cursor.execute("SELECT COUNT(*) FROM perguntas_respostas")
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            logger.error(f"❌ Error getting Q&A count: {e}")
            raise

    def seed_sample_data(self) -> None:
        """Seed the database with sample events if empty."""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM eventos")
            if self.cursor.fetchone()[0] == 0:
                logger.info("🌱 Seeding sample events...")
                
                sample_events = [
                    ("Festival de Música", "2023-12-15", "Parque Central", "Um festival com bandas internacionais."),
                    ("Feira de Tecnologia", "2024-02-20", "Centro de Eventos", "Apresentação das últimas inovações tecnológicas."),
                ]
                
                for event in sample_events:
                    self.insert_event(*event)
                
                logger.info("✅ Sample events seeded successfully")
        except sqlite3.Error as e:
            logger.error(f"❌ Error seeding sample data: {e}")
            raise
