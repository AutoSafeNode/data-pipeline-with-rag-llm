"""
Configuration Management Module
Handles loading and managing configuration from JSON files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class GeminiConfig:
    """Gemini API configuration."""
    api_key: str
    model: str = "gemini-pro"
    temperature: float = 0.3
    top_k: int = 40
    top_p: float = 0.95
    max_output_tokens: int = 2048


@dataclass
class PipelineConfig:
    """Pipeline configuration."""
    input_dir: str
    output_dir: str
    chunk_size: int
    chunk_overlap: int


@dataclass
class RAGConfig:
    """RAG configuration."""
    embedding_model: str = "text-embedding-004"
    vector_store_path: str = "./data/vectorstore"
    max_documents: int = 1000


@dataclass
class Config:
    """Main configuration class."""
    gemini: GeminiConfig
    pipelines: Dict[str, PipelineConfig]
    rag: RAGConfig
    
    @classmethod
    def from_json(cls, config_path: str) -> 'Config':
        """
        Load configuration from JSON file.
        
        Args:
            config_path: Path to configuration JSON file
            
        Returns:
            Config instance
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls(
            gemini=GeminiConfig(**data['gemini']),
            pipelines={
                name: PipelineConfig(**value)
                for name, value in data['pipelines'].items()
            },
            rag=RAGConfig(**data['rag'])
        )
    
    @classmethod
    def load_default(cls) -> 'Config':
        """
        Load default configuration from config/config.json.
        
        Returns:
            Config instance
        """
        config_path = Path(__file__).parent.parent.parent / "config" / "config.json"
        return cls.from_json(str(config_path))


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Load configuration from file.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        Config instance
    """
    if config_path:
        return Config.from_json(config_path)
    return Config.load_default()
