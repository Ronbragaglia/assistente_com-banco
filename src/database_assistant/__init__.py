# -*- coding: utf-8 -*-
"""OpenAI Database Assistant

Um assistente de IA com banco de dados SQLite e busca de similaridade
usando TF-IDF e cosine similarity.
"""

__version__ = "2.0.0"
__author__ = "Ronald Bragaglia"
__email__ = "ronald.bragaglia@example.com"

from .config import Settings
from .database import DatabaseManager
from .similarity import SimilaritySearch
from .assistant import OpenAIAssistant
from .cli import main

__all__ = [
    "Settings",
    "DatabaseManager",
    "SimilaritySearch",
    "OpenAIAssistant",
    "main",
]
