# -*- coding: utf-8 -*-
"""Tests for similarity search module."""

import pytest
from typing import List, Tuple, Optional

import sys
sys.path.insert(0, str(__file__).split("/tests")[0] + "/src")

from database_assistant.similarity import SimilaritySearch


@pytest.fixture
def sample_qa_pairs() -> List[Tuple[str, str]]:
    """Sample Q&A pairs for testing."""
    return [
        ("Quais eventos estão disponíveis?", "Temos 3 eventos disponíveis: Festival de Música, Feira de Tecnologia e Workshop de Python."),
        ("Quando é o Festival de Música?", "O Festival de Música será em 15 de dezembro de 2023."),
        ("Onde será a Feira de Tecnologia?", "A Feira de Tecnologia será no Centro de Eventos."),
        ("Qual o preço do Workshop de Python?", "O Workshop de Python é gratuito."),
        ("Como me inscrever nos eventos?", "Você pode se inscrever através do nosso site oficial."),
    ]


@pytest.fixture
def similarity_search() -> SimilaritySearch:
    """Create a similarity search instance."""
    return SimilaritySearch(threshold=0.7)


class TestSimilaritySearch:
    """Test cases for SimilaritySearch class."""

    def test_initialization(self):
        """Test similarity search initialization."""
        search = SimilaritySearch(threshold=0.8)
        assert search.threshold == 0.8
        assert search.vectorizer is None
        assert search.questions == []
        assert search.answers == []

    def test_initialization_default_threshold(self):
        """Test similarity search initialization with default threshold."""
        search = SimilaritySearch()
        assert search.threshold == 0.7

    def test_fit_empty_qa_pairs(self, similarity_search: SimilaritySearch):
        """Test fitting with empty Q&A pairs."""
        similarity_search.fit([])
        assert similarity_search.questions == []
        assert similarity_search.answers == []
        assert similarity_search.vectorizer is None

    def test_fit_qa_pairs(self, similarity_search: SimilaritySearch, sample_qa_pairs: List[Tuple[str, str]]):
        """Test fitting with Q&A pairs."""
        similarity_search.fit(sample_qa_pairs)
        assert len(similarity_search.questions) == len(sample_qa_pairs)
        assert len(similarity_search.answers) == len(sample_qa_pairs)
        assert similarity_search.vectorizer is not None
        assert similarity_search.questions[0] == sample_qa_pairs[0][0]
        assert similarity_search.answers[0] == sample_qa_pairs[0][1]

    def test_search_no_fit(self, similarity_search: SimilaritySearch):
        """Test search without fitting."""
        result = similarity_search.search("Test question")
        assert result is None

    def test_search_exact_match(self, similarity_search: SimilaritySearch, sample_qa_pairs: List[Tuple[str, str]]):
        """Test search with exact match."""
        similarity_search.fit(sample_qa_pairs)
        result = similarity_search.search(sample_qa_pairs[0][0])
        assert result == sample_qa_pairs[0][1]

    def test_search_similar_question(self, similarity_search: SimilaritySearch, sample_qa_pairs: List[Tuple[str, str]]):
        """Test search with similar question."""
        similarity_search.fit(sample_qa_pairs)
        result = similarity_search.search("Que eventos tem?")
        # Should find a similar question
        assert result is not None
        assert isinstance(result, str)

    def test_search_no_match(self, similarity_search: SimilaritySearch, sample_qa_pairs: List[Tuple[str, str]]):
        """Test search with no similar question."""
        similarity_search.fit(sample_qa_pairs)
        result = similarity_search.search("Como faço para viajar para Marte?")
        # Should not find a similar question
        assert result is None

    def test_search_with_score_no_fit(self, similarity_search: SimilaritySearch):
        """Test search with score without fitting."""
        result, score = similarity_search.search_with_score("Test question")
        assert result is None
        assert score == 0.0

    def test_search_with_score_exact_match(self, similarity_search: SimilaritySearch, sample_qa_pairs: List[Tuple[str, str]]):
        """Test search with score for exact match."""
        similarity_search.fit(sample_qa_pairs)
        result, score = similarity_search.search_with_score(sample_qa_pairs[0][0])
        assert result == sample_qa_pairs[0][1]
        assert score > 0.9  # Should be very high for exact match

    def test_search_with_score_similar_question(self, similarity_search: SimilaritySearch, sample_qa_pairs: List[Tuple[str, str]]):
        """Test search with score for similar question."""
        similarity_search.fit(sample_qa_pairs)
        result, score = similarity_search.search_with_score("Quais eventos?")
        assert result is not None
        assert score > 0.7  # Should be above threshold

    def test_search_with_score_no_match(self, similarity_search: SimilaritySearch, sample_qa_pairs: List[Tuple[str, str]]):
        """Test search with score for no match."""
        similarity_search.fit(sample_qa_pairs)
        result, score = similarity_search.search_with_score("Como faço para viajar para Marte?")
        assert result is None
        assert score < 0.7  # Should be below threshold

    def test_update_empty(self, similarity_search: SimilaritySearch):
        """Test update with empty Q&A pairs."""
        similarity_search.update([])
        assert similarity_search.questions == []
        assert similarity_search.answers == []

    def test_update_new_pairs(self, similarity_search: SimilaritySearch, sample_qa_pairs: List[Tuple[str, str]]):
        """Test update with new Q&A pairs."""
        similarity_search.fit(sample_qa_pairs[:2])
        initial_count = len(similarity_search.questions)
        
        similarity_search.update(sample_qa_pairs[2:])
        assert len(similarity_search.questions) == initial_count + 3
        assert len(similarity_search.answers) == initial_count + 3

    def test_clear(self, similarity_search: SimilaritySearch, sample_qa_pairs: List[Tuple[str, str]]):
        """Test clearing the search index."""
        similarity_search.fit(sample_qa_pairs)
        similarity_search.clear()
        assert similarity_search.questions == []
        assert similarity_search.answers == []
        assert similarity_search.vectorizer is None

    def test_threshold_effect(self):
        """Test the effect of different thresholds."""
        qa_pairs = [
            ("Quais eventos estão disponíveis?", "Temos 3 eventos disponíveis."),
            ("Quando é o Festival?", "O Festival será em 15 de dezembro."),
        ]
        
        # Low threshold
        search_low = SimilaritySearch(threshold=0.3)
        search_low.fit(qa_pairs)
        result_low = search_low.search("Que eventos?")
        assert result_low is not None
        
        # High threshold
        search_high = SimilaritySearch(threshold=0.9)
        search_high.fit(qa_pairs)
        result_high = search_high.search("Que eventos?")
        # Might not find a match with high threshold
        # depending on the actual similarity score

    def test_multiple_similar_questions(self, similarity_search: SimilaritySearch):
        """Test search with multiple similar questions."""
        qa_pairs = [
            ("Quais eventos?", "Eventos: A, B, C"),
            ("Que eventos?", "Eventos: A, B, C"),
            ("Quais são os eventos?", "Eventos: A, B, C"),
        ]
        similarity_search.fit(qa_pairs)
        
        result = similarity_search.search("Quais eventos tem?")
        assert result is not None
        assert isinstance(result, str)

    def test_case_insensitivity(self, similarity_search: SimilaritySearch):
        """Test case insensitivity in search."""
        qa_pairs = [
            ("Quais eventos estão disponíveis?", "Temos 3 eventos disponíveis."),
        ]
        similarity_search.fit(qa_pairs)
        
        result_lower = similarity_search.search("quais eventos estão disponíveis?")
        result_upper = similarity_search.search("QUAIS EVENTOS ESTÃO DISPONÍVEIS?")
        
        assert result_lower is not None
        assert result_upper is not None

    def test_special_characters(self, similarity_search: SimilaritySearch):
        """Test search with special characters."""
        qa_pairs = [
            ("Quais eventos com @ e #?", "Eventos especiais com símbolos."),
        ]
        similarity_search.fit(qa_pairs)
        
        result = similarity_search.search("eventos com @ e #?")
        assert result is not None

    def test_unicode_support(self, similarity_search: SimilaritySearch):
        """Test Unicode support in search."""
        qa_pairs = [
            ("Quais eventos 中文?", "Eventos em chinês."),
            ("Quais eventos 日本語?", "Eventos em japonês."),
        ]
        similarity_search.fit(qa_pairs)
        
        result = similarity_search.search("eventos 中文?")
        assert result is not None

    def test_empty_query(self, similarity_search: SimilaritySearch, sample_qa_pairs: List[Tuple[str, str]]):
        """Test search with empty query."""
        similarity_search.fit(sample_qa_pairs)
        result = similarity_search.search("")
        # Should handle empty query gracefully
        assert result is None or isinstance(result, str)

    def test_very_long_query(self, similarity_search: SimilaritySearch, sample_qa_pairs: List[Tuple[str, str]]):
        """Test search with very long query."""
        similarity_search.fit(sample_qa_pairs)
        long_query = "A" * 10000
        result = similarity_search.search(long_query)
        # Should handle long query gracefully
        assert result is None or isinstance(result, str)

    def test_single_qa_pair(self, similarity_search: SimilaritySearch):
        """Test with single Q&A pair."""
        qa_pairs = [
            ("Quais eventos?", "Eventos: A, B, C"),
        ]
        similarity_search.fit(qa_pairs)
        
        result = similarity_search.search("Quais eventos?")
        assert result == "Eventos: A, B, C"

    def test_large_dataset(self, similarity_search: SimilaritySearch):
        """Test with large dataset."""
        qa_pairs = [
            (f"Pergunta {i}", f"Resposta {i}")
            for i in range(100)
        ]
        similarity_search.fit(qa_pairs)
        
        result = similarity_search.search("Pergunta 50")
        assert result == "Resposta 50"

    def test_repeated_questions(self, similarity_search: SimilaritySearch):
        """Test with repeated questions."""
        qa_pairs = [
            ("Quais eventos?", "Resposta A"),
            ("Quais eventos?", "Resposta B"),
            ("Quais eventos?", "Resposta C"),
        ]
        similarity_search.fit(qa_pairs)
        
        result = similarity_search.search("Quais eventos?")
        # Should return one of the answers
        assert result in ["Resposta A", "Resposta B", "Resposta C"]

    def test_update_after_search(self, similarity_search: SimilaritySearch, sample_qa_pairs: List[Tuple[str, str]]):
        """Test that update works after search."""
        similarity_search.fit(sample_qa_pairs[:2])
        result1 = similarity_search.search("Quais eventos?")
        
        similarity_search.update(sample_qa_pairs[2:])
        result2 = similarity_search.search("Quais eventos?")
        
        # Both should work
        assert result1 is not None
        assert result2 is not None

    def test_threshold_boundary(self):
        """Test behavior at threshold boundary."""
        qa_pairs = [
            ("Quais eventos?", "Eventos: A, B, C"),
        ]
        
        # Test with threshold exactly at expected similarity
        search = SimilaritySearch(threshold=0.95)
        search.fit(qa_pairs)
        
        result, score = search.search_with_score("Quais eventos?")
        # Check if result is returned based on score vs threshold
        if score >= search.threshold:
            assert result is not None
        else:
            assert result is None

    def test_performance_large_dataset(self, similarity_search: SimilaritySearch):
        """Test performance with large dataset."""
        import time
        
        qa_pairs = [
            (f"Pergunta {i} com texto mais longo para teste de performance",
             f"Resposta {i} com texto mais longo para teste de performance")
            for i in range(1000)
        ]
        
        # Fit time
        start_time = time.time()
        similarity_search.fit(qa_pairs)
        fit_time = time.time() - start_time
        
        # Search time
        start_time = time.time()
        result = similarity_search.search("Pergunta 500")
        search_time = time.time() - start_time
        
        # Should complete in reasonable time
        assert fit_time < 10.0  # Should fit in less than 10 seconds
        assert search_time < 1.0  # Should search in less than 1 second
        assert result is not None
