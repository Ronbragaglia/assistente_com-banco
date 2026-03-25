# -*- coding: utf-8 -*-
"""Tests for database module."""

import pytest
import sqlite3
from pathlib import Path
from typing import List, Tuple

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database_assistant.database import DatabaseManager


@pytest.fixture
def temp_db_path(tmp_path: Path) -> Path:
    """Create a temporary database path."""
    return tmp_path / "test.db"


@pytest.fixture
def db_manager(temp_db_path: Path) -> DatabaseManager:
    """Create a database manager with temporary database."""
    return DatabaseManager(temp_db_path)


@pytest.fixture
def sample_events() -> List[Tuple[str, str, str, str]]:
    """Sample events for testing."""
    return [
        ("Festival de Música", "2023-12-15", "Parque Central", "Um festival com bandas internacionais."),
        ("Feira de Tecnologia", "2024-02-20", "Centro de Eventos", "Apresentação das últimas inovações tecnológicas."),
        ("Workshop de Python", "2024-03-10", "Sala de Conferências", "Workshop introdutório sobre Python"),
    ]


@pytest.fixture
def sample_qa_pairs() -> List[Tuple[str, str]]:
    """Sample Q&A pairs for testing."""
    return [
        ("Quais eventos estão disponíveis?", "Temos 3 eventos disponíveis: Festival de Música, Feira de Tecnologia e Workshop de Python."),
        ("Quando é o Festival de Música?", "O Festival de Música será em 15 de dezembro de 2023."),
        ("Onde será a Feira de Tecnologia?", "A Feira de Tecnologia será no Centro de Eventos."),
    ]


class TestDatabaseManager:
    """Test cases for DatabaseManager class."""

    def test_initialization(self, temp_db_path: Path):
        """Test database manager initialization."""
        db_manager = DatabaseManager(temp_db_path)
        assert db_manager.db_path == temp_db_path
        assert db_manager.connection is None
        assert db_manager.cursor is None

    def test_connect(self, db_manager: DatabaseManager):
        """Test database connection."""
        db_manager.connect()
        assert db_manager.connection is not None
        assert db_manager.cursor is not None
        db_manager.disconnect()

    def test_disconnect(self, db_manager: DatabaseManager):
        """Test database disconnection."""
        db_manager.connect()
        db_manager.disconnect()
        assert db_manager.connection is None
        assert db_manager.cursor is None

    def test_context_manager(self, db_manager: DatabaseManager):
        """Test context manager usage."""
        with db_manager:
            assert db_manager.connection is not None
            assert db_manager.cursor is not None
        assert db_manager.connection is None
        assert db_manager.cursor is None

    def test_create_tables(self, db_manager: DatabaseManager):
        """Test table creation."""
        with db_manager:
            db_manager.create_tables()
            
            # Check if tables exist
            db_manager.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='eventos'"
            )
            assert db_manager.cursor.fetchone() is not None
            
            db_manager.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='perguntas_respostas'"
            )
            assert db_manager.cursor.fetchone() is not None

    def test_insert_event(self, db_manager: DatabaseManager):
        """Test event insertion."""
        with db_manager:
            db_manager.create_tables()
            event_id = db_manager.insert_event(
                nome="Test Event",
                data="2024-01-01",
                local="Test Location",
                descricao="Test Description"
            )
            assert event_id > 0
            
            # Verify insertion
            db_manager.cursor.execute("SELECT * FROM eventos WHERE id=?", (event_id,))
            event = db_manager.cursor.fetchone()
            assert event is not None
            assert event[1] == "Test Event"

    def test_insert_multiple_events(self, db_manager: DatabaseManager, sample_events: List[Tuple[str, str, str, str]]):
        """Test insertion of multiple events."""
        with db_manager:
            db_manager.create_tables()
            event_ids = []
            for event in sample_events:
                event_id = db_manager.insert_event(*event)
                event_ids.append(event_id)
            
            assert len(event_ids) == len(sample_events)
            assert all(eid > 0 for eid in event_ids)

    def test_get_all_events_empty(self, db_manager: DatabaseManager):
        """Test getting all events from empty database."""
        with db_manager:
            db_manager.create_tables()
            events = db_manager.get_all_events()
            assert events == []

    def test_get_all_events(self, db_manager: DatabaseManager, sample_events: List[Tuple[str, str, str, str]]):
        """Test getting all events."""
        with db_manager:
            db_manager.create_tables()
            for event in sample_events:
                db_manager.insert_event(*event)
            
            events = db_manager.get_all_events()
            assert len(events) == len(sample_events)
            
            # Check first event
            assert events[0][0] == sample_events[0][0]  # nome
            assert events[0][1] == sample_events[0][1]  # data
            assert events[0][2] == sample_events[0][2]  # local
            assert events[0][3] == sample_events[0][3]  # descricao

    def test_get_events_as_context(self, db_manager: DatabaseManager, sample_events: List[Tuple[str, str, str, str]]):
        """Test getting events as context string."""
        with db_manager:
            db_manager.create_tables()
            for event in sample_events:
                db_manager.insert_event(*event)
            
            context = db_manager.get_events_as_context()
            assert "Informações sobre eventos:" in context
            assert sample_events[0][0] in context  # nome
            assert sample_events[0][1] in context  # data
            assert sample_events[0][2] in context  # local
            assert sample_events[0][3] in context  # descricao

    def test_insert_question_answer(self, db_manager: DatabaseManager):
        """Test Q&A pair insertion."""
        with db_manager:
            db_manager.create_tables()
            qa_id = db_manager.insert_question_answer(
                pergunta="Test Question",
                resposta="Test Answer"
            )
            assert qa_id > 0
            
            # Verify insertion
            db_manager.cursor.execute("SELECT * FROM perguntas_respostas WHERE id=?", (qa_id,))
            qa = db_manager.cursor.fetchone()
            assert qa is not None
            assert qa[1] == "Test Question"
            assert qa[2] == "Test Answer"

    def test_insert_multiple_qa_pairs(self, db_manager: DatabaseManager, sample_qa_pairs: List[Tuple[str, str]]):
        """Test insertion of multiple Q&A pairs."""
        with db_manager:
            db_manager.create_tables()
            qa_ids = []
            for qa in sample_qa_pairs:
                qa_id = db_manager.insert_question_answer(*qa)
                qa_ids.append(qa_id)
            
            assert len(qa_ids) == len(sample_qa_pairs)
            assert all(qid > 0 for qid in qa_ids)

    def test_get_all_qa_pairs_empty(self, db_manager: DatabaseManager):
        """Test getting all Q&A pairs from empty database."""
        with db_manager:
            db_manager.create_tables()
            qa_pairs = db_manager.get_all_qa_pairs()
            assert qa_pairs == []

    def test_get_all_qa_pairs(self, db_manager: DatabaseManager, sample_qa_pairs: List[Tuple[str, str]]):
        """Test getting all Q&A pairs."""
        with db_manager:
            db_manager.create_tables()
            for qa in sample_qa_pairs:
                db_manager.insert_question_answer(*qa)
            
            qa_pairs = db_manager.get_all_qa_pairs()
            assert len(qa_pairs) == len(sample_qa_pairs)
            
            # Check first Q&A pair
            assert qa_pairs[0][0] == sample_qa_pairs[0][0]  # pergunta
            assert qa_pairs[0][1] == sample_qa_pairs[0][1]  # resposta

    def test_get_qa_count_empty(self, db_manager: DatabaseManager):
        """Test getting Q&A count from empty database."""
        with db_manager:
            db_manager.create_tables()
            count = db_manager.get_qa_count()
            assert count == 0

    def test_get_qa_count(self, db_manager: DatabaseManager, sample_qa_pairs: List[Tuple[str, str]]):
        """Test getting Q&A count."""
        with db_manager:
            db_manager.create_tables()
            for qa in sample_qa_pairs:
                db_manager.insert_question_answer(*qa)
            
            count = db_manager.get_qa_count()
            assert count == len(sample_qa_pairs)

    def test_seed_sample_data(self, db_manager: DatabaseManager):
        """Test seeding sample data."""
        with db_manager:
            db_manager.create_tables()
            db_manager.seed_sample_data()
            
            # Check if events were seeded
            events = db_manager.get_all_events()
            assert len(events) > 0

    def test_seed_sample_data_only_once(self, db_manager: DatabaseManager):
        """Test that sample data is seeded only once."""
        with db_manager:
            db_manager.create_tables()
            db_manager.seed_sample_data()
            first_count = db_manager.get_qa_count()
            
            # Seed again
            db_manager.seed_sample_data()
            second_count = db_manager.get_qa_count()
            
            # Count should be the same
            assert first_count == second_count

    def test_database_persistence(self, temp_db_path: Path):
        """Test that data persists across connections."""
        # Insert data with first connection
        db_manager1 = DatabaseManager(temp_db_path)
        with db_manager1:
            db_manager1.create_tables()
            event_id = db_manager1.insert_event(
                nome="Persistent Event",
                data="2024-01-01",
                local="Test Location",
                descricao="Test Description"
            )
        
        # Read data with second connection
        db_manager2 = DatabaseManager(temp_db_path)
        with db_manager2:
            events = db_manager2.get_all_events()
            assert len(events) == 1
            assert events[0][0] == "Persistent Event"

    def test_sqlite_error_handling(self, temp_db_path: Path):
        """Test SQLite error handling."""
        db_manager = DatabaseManager(temp_db_path)
        
        # Try to connect to invalid path
        invalid_path = Path("/invalid/path/to/database.db")
        db_manager_invalid = DatabaseManager(invalid_path)
        
        with pytest.raises(sqlite3.Error):
            db_manager_invalid.connect()

    def test_concurrent_connections(self, temp_db_path: Path):
        """Test concurrent database connections."""
        db_manager1 = DatabaseManager(temp_db_path)
        db_manager2 = DatabaseManager(temp_db_path)
        
        with db_manager1:
            db_manager1.create_tables()
            db_manager1.insert_event(
                nome="Event 1",
                data="2024-01-01",
                local="Location 1",
                descricao="Description 1"
            )
        
        with db_manager2:
            events = db_manager2.get_all_events()
            assert len(events) == 1
            assert events[0][0] == "Event 1"

    def test_large_text_handling(self, db_manager: DatabaseManager):
        """Test handling of large text fields."""
        large_text = "A" * 10000  # 10KB of text
        
        with db_manager:
            db_manager.create_tables()
            event_id = db_manager.insert_event(
                nome="Large Text Event",
                data="2024-01-01",
                local="Test Location",
                descricao=large_text
            )
            
            events = db_manager.get_all_events()
            assert len(events) == 1
            assert events[0][3] == large_text

    def test_special_characters(self, db_manager: DatabaseManager):
        """Test handling of special characters."""
        special_text = "Test with émojis 🎉 and special chars: á, ñ, ç, @, #, $, %, &"
        
        with db_manager:
            db_manager.create_tables()
            event_id = db_manager.insert_event(
                nome="Special Chars Event",
                data="2024-01-01",
                local="Test Location",
                descricao=special_text
            )
            
            events = db_manager.get_all_events()
            assert len(events) == 1
            assert events[0][3] == special_text

    def test_unicode_support(self, db_manager: DatabaseManager):
        """Test Unicode support."""
        unicode_text = "Teste com caracteres unicode: 中文, 日本語, 한국어, العربية, עברית"
        
        with db_manager:
            db_manager.create_tables()
            qa_id = db_manager.insert_question_answer(
                pergunta=unicode_text,
                resposta=unicode_text
            )
            
            qa_pairs = db_manager.get_all_qa_pairs()
            assert len(qa_pairs) == 1
            assert qa_pairs[0][0] == unicode_text
            assert qa_pairs[0][1] == unicode_text
