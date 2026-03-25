# -*- coding: utf-8 -*-
"""Configuration module for OpenAI Database Assistant."""

import os
from typing import Optional
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Configuration settings for the application."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")
    openai_model: str = Field(default="gpt-3.5-turbo", description="OpenAI model to use")
    openai_temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature for OpenAI responses")

    # Database Configuration
    database_path: Path = Field(default=Path("data/eventos.db"), description="Path to SQLite database")

    # Similarity Search Configuration
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="Similarity threshold for matching")

    # Assistant Configuration
    assistant_name: str = Field(default="Assistente de Eventos", description="Name of the assistant")
    assistant_system_prompt: str = Field(
        default="Você é um assistente útil especializado em eventos.",
        description="System prompt for the assistant",
    )

    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(default="logs/assistant.log", description="Path to log file")

    # Cache Configuration
    cache_enabled: bool = Field(default=True, description="Enable caching of responses")

    # Paths
    data_dir: Path = Field(default=Path("data"), description="Directory for data files")
    logs_dir: Path = Field(default=Path("logs"), description="Directory for log files")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()

    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "openai_api_key": "sk-...",
                "openai_model": "gpt-3.5-turbo",
                "database_path": "data/eventos.db",
            }
        }


# Global settings instance
settings = Settings()
