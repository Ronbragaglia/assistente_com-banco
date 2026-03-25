#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Advanced Similarity Analysis Example for OpenAI Database Assistant.

This example demonstrates advanced similarity analysis techniques
including batch processing, threshold optimization, and similarity clustering.
"""

from typing import List, Tuple, Dict, Any
from pathlib import Path
import numpy as np
from collections import defaultdict

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database_assistant import (
    DatabaseManager,
    SimilaritySearch,
    setup_logger,
)


def find_all_similar_questions(
    similarity_search: SimilaritySearch,
    query: str,
    min_similarity: float = 0.0,
) -> List[Tuple[str, str, float]]:
    """Find all similar questions with their similarity scores.

    Args:
        similarity_search: Similarity search instance
        query: Query question
        min_similarity: Minimum similarity threshold

    Returns:
        List of (question, answer, similarity_score) tuples
    """
    logger = setup_logger(name="similarity_analysis")

    if not similarity_search.questions or similarity_search.vectorizer is None:
        logger.warning("⚠️  No questions indexed for similarity search")
        return []

    try:
        # Vectorize the query and existing questions
        query_vector = similarity_search.vectorizer.transform([query])
        questions_vectors = similarity_search.vectorizer.transform(
            similarity_search.questions
        )

        # Calculate cosine similarity
        similarities = np.cosine_similarity(query_vector, questions_vectors).flatten()

        # Get all results above minimum threshold
        results = []
        for idx, similarity in enumerate(similarities):
            if similarity >= min_similarity:
                results.append((
                    similarity_search.questions[idx],
                    similarity_search.answers[idx],
                    float(similarity)
                ))

        # Sort by similarity (descending)
        results.sort(key=lambda x: x[2], reverse=True)

        logger.info(f"✅ Found {len(results)} similar questions")
        return results

    except Exception as e:
        logger.error(f"❌ Error finding similar questions: {e}")
        return []


def optimize_similarity_threshold(
    similarity_search: SimilaritySearch,
    test_queries: List[str],
    expected_answers: List[str],
) -> float:
    """Optimize similarity threshold for best accuracy.

    Args:
        similarity_search: Similarity search instance
        test_queries: List of test queries
        expected_answers: List of expected answers

    Returns:
        Optimal threshold value
    """
    logger = setup_logger(name="similarity_analysis")

    if len(test_queries) != len(expected_answers):
        raise ValueError("Test queries and expected answers must have the same length")

    # Test different thresholds
    thresholds = np.arange(0.0, 1.0, 0.1)
    best_threshold = 0.7
    best_accuracy = 0.0

    for threshold in thresholds:
        correct = 0
        total = len(test_queries)

        for query, expected in zip(test_queries, expected_answers):
            answer = similarity_search.search(query)
            if answer and answer == expected:
                correct += 1

        accuracy = correct / total
        logger.info(f"Threshold {threshold:.1f}: Accuracy {accuracy:.2%}")

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_threshold = threshold

    logger.info(f"🎯 Optimal threshold: {best_threshold:.1f} (Accuracy: {best_accuracy:.2%})")
    return best_threshold


def cluster_similar_questions(
    similarity_search: SimilaritySearch,
    cluster_threshold: float = 0.8,
) -> Dict[str, List[Tuple[str, str]]]:
    """Cluster similar questions together.

    Args:
        similarity_search: Similarity search instance
        cluster_threshold: Threshold for clustering

    Returns:
        Dictionary mapping cluster IDs to question-answer pairs
    """
    logger = setup_logger(name="similarity_analysis")

    if not similarity_search.questions or similarity_search.vectorizer is None:
        logger.warning("⚠️  No questions indexed for clustering")
        return {}

    try:
        # Vectorize all questions
        questions_vectors = similarity_search.vectorizer.transform(
            similarity_search.questions
        )

        # Calculate similarity matrix
        similarity_matrix = np.cosine_similarity(questions_vectors)

        # Cluster questions
        clusters = defaultdict(list)
        visited = set()

        for i in range(len(similarity_search.questions)):
            if i in visited:
                continue

            # Start new cluster
            cluster_id = f"cluster_{len(clusters)}"
            clusters[cluster_id].append((
                similarity_search.questions[i],
                similarity_search.answers[i]
            ))
            visited.add(i)

            # Find similar questions
            for j in range(len(similarity_search.questions)):
                if j not in visited and similarity_matrix[i][j] >= cluster_threshold:
                    clusters[cluster_id].append((
                        similarity_search.questions[j],
                        similarity_search.answers[j]
                    ))
                    visited.add(j)

        logger.info(f"✅ Created {len(clusters)} clusters")
        return dict(clusters)

    except Exception as e:
        logger.error(f"❌ Error clustering questions: {e}")
        return {}


def analyze_similarity_distribution(
    similarity_search: SimilaritySearch,
    query: str,
) -> Dict[str, Any]:
    """Analyze the distribution of similarity scores.

    Args:
        similarity_search: Similarity search instance
        query: Query question

    Returns:
        Dictionary with statistics about similarity distribution
    """
    logger = setup_logger(name="similarity_analysis")

    if not similarity_search.questions or similarity_search.vectorizer is None:
        logger.warning("⚠️  No questions indexed for analysis")
        return {}

    try:
        # Vectorize the query and existing questions
        query_vector = similarity_search.vectorizer.transform([query])
        questions_vectors = similarity_search.vectorizer.transform(
            similarity_search.questions
        )

        # Calculate cosine similarity
        similarities = np.cosine_similarity(query_vector, questions_vectors).flatten()

        # Calculate statistics
        stats = {
            "mean": float(np.mean(similarities)),
            "std": float(np.std(similarities)),
            "min": float(np.min(similarities)),
            "max": float(np.max(similarities)),
            "median": float(np.median(similarities)),
            "percentile_25": float(np.percentile(similarities, 25)),
            "percentile_75": float(np.percentile(similarities, 75)),
            "above_threshold": int(np.sum(similarities >= similarity_search.threshold)),
            "total_questions": len(similarities),
        }

        logger.info(f"✅ Similarity analysis completed")
        return stats

    except Exception as e:
        logger.error(f"❌ Error analyzing similarity distribution: {e}")
        return {}


def batch_similarity_search(
    similarity_search: SimilaritySearch,
    queries: List[str],
) -> List[Optional[str]]:
    """Perform similarity search for multiple queries at once.

    Args:
        similarity_search: Similarity search instance
        queries: List of queries

    Returns:
        List of answers (None if no match found)
    """
    logger = setup_logger(name="similarity_analysis")

    results = []
    for query in queries:
        answer = similarity_search.search(query)
        results.append(answer)

    logger.info(f"✅ Batch search completed for {len(queries)} queries")
    return results


def main():
    """Main function demonstrating advanced similarity analysis."""
    logger = setup_logger(name="similarity_analysis")

    # Initialize components
    db_manager = DatabaseManager(Path("data/eventos.db"))
    similarity_search = SimilaritySearch(threshold=0.7)

    # Setup database
    with db_manager:
        db_manager.create_tables()
        db_manager.seed_sample_data()

    # Load similarity search
    with db_manager:
        qa_pairs = db_manager.get_all_qa_pairs()
        similarity_search.fit(qa_pairs)

    # Example 1: Find all similar questions
    print("\n" + "="*60)
    print("Example 1: Find All Similar Questions")
    print("="*60)
    query = "Quais eventos estão disponíveis?"
    similar = find_all_similar_questions(similarity_search, query, min_similarity=0.0)
    print(f"\nQuery: {query}")
    print(f"Found {len(similar)} similar questions:")
    for question, answer, score in similar[:5]:  # Show top 5
        print(f"  - Score: {score:.4f}")
        print(f"    Question: {question}")
        print(f"    Answer: {answer[:50]}...")

    # Example 2: Analyze similarity distribution
    print("\n" + "="*60)
    print("Example 2: Similarity Distribution Analysis")
    print("="*60)
    stats = analyze_similarity_distribution(similarity_search, query)
    print(f"\nQuery: {query}")
    print("Similarity Statistics:")
    print(f"  Mean: {stats['mean']:.4f}")
    print(f"  Std: {stats['std']:.4f}")
    print(f"  Min: {stats['min']:.4f}")
    print(f"  Max: {stats['max']:.4f}")
    print(f"  Median: {stats['median']:.4f}")
    print(f"  Questions above threshold: {stats['above_threshold']}/{stats['total_questions']}")

    # Example 3: Cluster similar questions
    print("\n" + "="*60)
    print("Example 3: Cluster Similar Questions")
    print("="*60)
    clusters = cluster_similar_questions(similarity_search, cluster_threshold=0.8)
    print(f"\nCreated {len(clusters)} clusters:")
    for cluster_id, pairs in clusters.items():
        print(f"\n{cluster_id}: {len(pairs)} questions")
        for question, answer in pairs[:2]:  # Show first 2
            print(f"  - {question[:50]}...")

    # Example 4: Batch similarity search
    print("\n" + "="*60)
    print("Example 4: Batch Similarity Search")
    print("="*60)
    queries = [
        "Quais eventos?",
        "Quando é o festival?",
        "Onde será a feira?",
    ]
    results = batch_similarity_search(similarity_search, queries)
    print("\nBatch search results:")
    for query, answer in zip(queries, results):
        print(f"\nQuery: {query}")
        print(f"Answer: {answer[:50] if answer else 'No match found'}...")

    logger.info("🎉 Similarity analysis examples completed!")


if __name__ == "__main__":
    main()
