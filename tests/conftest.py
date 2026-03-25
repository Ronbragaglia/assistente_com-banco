# -*- coding: utf-8 -*-
"""Shared fixtures for all tests."""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def src_dir(project_root: Path) -> Path:
    """Get the source directory."""
    return project_root / "src"


@pytest.fixture(scope="session")
def tests_dir(project_root: Path) -> Path:
    """Get the tests directory."""
    return project_root / "tests"


@pytest.fixture(scope="session")
def data_dir(project_root: Path) -> Path:
    """Get the data directory."""
    return project_root / "data"


@pytest.fixture(scope="session")
def logs_dir(project_root: Path) -> Path:
    """Get the logs directory."""
    return project_root / "logs"


@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return "This is a sample text for testing purposes."


@pytest.fixture
def sample_questions():
    """Sample questions for testing."""
    return [
        "What events are available?",
        "When is the music festival?",
        "Where will the technology fair be held?",
        "How much does the Python workshop cost?",
        "How can I register for events?",
    ]


@pytest.fixture
def sample_answers():
    """Sample answers for testing."""
    return [
        "We have 3 events available: Music Festival, Technology Fair, and Python Workshop.",
        "The Music Festival will be on December 15, 2023.",
        "The Technology Fair will be held at the Convention Center.",
        "The Python Workshop is free.",
        "You can register through our official website.",
    ]


@pytest.fixture
def sample_qa_pairs(sample_questions, sample_answers):
    """Sample Q&A pairs for testing."""
    return list(zip(sample_questions, sample_answers))


@pytest.fixture
def mock_openai_api_key():
    """Mock OpenAI API key for testing."""
    return "sk-test-api-key-1234567890"


@pytest.fixture
def mock_openai_model():
    """Mock OpenAI model for testing."""
    return "gpt-3.5-turbo"


@pytest.fixture
def mock_temperature():
    """Mock temperature for testing."""
    return 0.7


@pytest.fixture
def mock_similarity_threshold():
    """Mock similarity threshold for testing."""
    return 0.7


@pytest.fixture
def mock_database_path(tmp_path):
    """Mock database path for testing."""
    return tmp_path / "test.db"


@pytest.fixture
def mock_log_file(tmp_path):
    """Mock log file path for testing."""
    return tmp_path / "test.log"


# Custom markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "requires_api: marks tests that require API access"
    )
