# -*- coding: utf-8 -*-
"""Similarity search module using TF-IDF and cosine similarity."""

from typing import List, Tuple, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

from .logger import get_logger

logger = get_logger(__name__)


class SimilaritySearch:
    """Search for similar questions using TF-IDF and cosine similarity."""

    def __init__(self, threshold: float = 0.7):
        """Initialize the similarity search.

        Args:
            threshold: Similarity threshold for considering a match (0.0 to 1.0)
        """
        self.threshold = threshold
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.questions: List[str] = []
        self.answers: List[str] = []

        logger.info(f"🔍 Similarity search initialized with threshold: {threshold}")

    def fit(self, qa_pairs: List[Tuple[str, str]]) -> None:
        """Fit the vectorizer with existing Q&A pairs.

        Args:
            qa_pairs: List of (question, answer) tuples
        """
        if not qa_pairs:
            logger.warning("⚠️  No Q&A pairs provided for fitting")
            return

        self.questions = [qa[0] for qa in qa_pairs]
        self.answers = [qa[1] for qa in qa_pairs]

        self.vectorizer = TfidfVectorizer()
        self.vectorizer.fit(self.questions)

        logger.info(f"✅ Fitted vectorizer with {len(self.questions)} questions")

    def search(self, query: str) -> Optional[str]:
        """Search for the most similar question and return its answer.

        Args:
            query: The query question to search for

        Returns:
            The answer to the most similar question, or None if no match found
        """
        if not self.questions or self.vectorizer is None:
            logger.debug("No questions indexed for similarity search")
            return None

        try:
            # Vectorize the query and existing questions
            query_vector = self.vectorizer.transform([query])
            questions_vectors = self.vectorizer.transform(self.questions)

            # Calculate cosine similarity
            similarities = cosine_similarity(query_vector, questions_vectors).flatten()

            # Find the most similar question
            max_similarity_index = np.argmax(similarities)
            max_similarity = similarities[max_similarity_index]

            logger.debug(f"Max similarity: {max_similarity:.4f} (threshold: {self.threshold})")

            # Return answer if similarity exceeds threshold
            if max_similarity > self.threshold:
                answer = self.answers[max_similarity_index]
                logger.info(f"✅ Found similar question (similarity: {max_similarity:.4f})")
                return answer

            logger.debug("No similar question found above threshold")
            return None

        except Exception as e:
            logger.error(f"❌ Error during similarity search: {e}")
            return None

    def search_with_score(self, query: str) -> Tuple[Optional[str], float]:
        """Search for the most similar question and return answer with similarity score.

        Args:
            query: The query question to search for

        Returns:
            Tuple of (answer, similarity_score). Returns (None, 0.0) if no match found.
        """
        if not self.questions or self.vectorizer is None:
            logger.debug("No questions indexed for similarity search")
            return None, 0.0

        try:
            # Vectorize the query and existing questions
            query_vector = self.vectorizer.transform([query])
            questions_vectors = self.vectorizer.transform(self.questions)

            # Calculate cosine similarity
            similarities = cosine_similarity(query_vector, questions_vectors).flatten()

            # Find the most similar question
            max_similarity_index = np.argmax(similarities)
            max_similarity = float(similarities[max_similarity_index])

            logger.debug(f"Max similarity: {max_similarity:.4f} (threshold: {self.threshold})")

            # Return answer and score if similarity exceeds threshold
            if max_similarity > self.threshold:
                answer = self.answers[max_similarity_index]
                logger.info(f"✅ Found similar question (similarity: {max_similarity:.4f})")
                return answer, max_similarity

            logger.debug("No similar question found above threshold")
            return None, max_similarity

        except Exception as e:
            logger.error(f"❌ Error during similarity search: {e}")
            return None, 0.0

    def update(self, qa_pairs: List[Tuple[str, str]]) -> None:
        """Update the similarity search with new Q&A pairs.

        Args:
            qa_pairs: List of (question, answer) tuples to add
        """
        if not qa_pairs:
            return

        # Add new questions and answers
        for qa in qa_pairs:
            self.questions.append(qa[0])
            self.answers.append(qa[1])

        # Re-fit the vectorizer with all questions
        self.vectorizer = TfidfVectorizer()
        self.vectorizer.fit(self.questions)

        logger.info(f"✅ Updated similarity search with {len(qa_pairs)} new pairs")

    def clear(self) -> None:
        """Clear all indexed questions and answers."""
        self.questions = []
        self.answers = []
        self.vectorizer = None
        logger.info("🗑️  Cleared similarity search index")
