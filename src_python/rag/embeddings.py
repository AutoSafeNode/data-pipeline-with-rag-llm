"""
Embedding Generator Module
Generates embeddings for text chunks using various models.
"""

import asyncio
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any

import numpy as np

from ..utils.logger import get_logger
from ..utils.config import RAGConfig


logger = get_logger("embeddings")


class EmbeddingGenerator:
    """
    Generator for text embeddings.
    """
    
    def __init__(self, config: RAGConfig):
        """
        Initialize embedding generator.
        
        Args:
            config: RAG configuration
        """
        self.config = config
        self.embedding_model = config.embedding_model
        self.cache_dir = Path(config.vector_store_path) / "cache"
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text chunk.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        try:
            # For now, return a simple hash-based embedding
            # In production, this would call an actual embedding API
            embedding = self._generate_simple_embedding(text)
            return embedding
            
        except Exception as error:
            logger.error("Error generating embedding", {"error": str(error)})
            raise
    
    async def generate_embeddings(
        self,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate embeddings for multiple chunks.
        
        Args:
            chunks: Chunks to embed
            
        Returns:
            Chunks with embeddings added
        """
        try:
            logger.info(f"Generating embeddings for {len(chunks)} chunks")
            
            chunks_with_embeddings = []
            
            for chunk in chunks:
                embedding = await self.generate_embedding(chunk["content"])
                
                chunk_with_embedding = chunk.copy()
                chunk_with_embedding["embedding"] = embedding
                chunk_with_embedding["metadata"] = {
                    **chunk.get("metadata", {}),
                    "embedding_model": self.embedding_model,
                    "embedding_dimension": len(embedding)
                }
                
                chunks_with_embeddings.append(chunk_with_embedding)
            
            logger.info(f"Generated embeddings for {len(chunks_with_embeddings)} chunks")
            return chunks_with_embeddings
            
        except Exception as error:
            logger.error("Error generating embeddings for chunks", {
                "error": str(error)
            })
            raise
    
    def _generate_simple_embedding(self, text: str) -> List[float]:
        """
        Simple hash-based embedding (placeholder for production).
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        dimension = 768  # Common embedding dimension
        embedding = [0.0] * dimension
        
        # Generate deterministic embedding based on text hash
        hash_value = int(hashlib.md5(text.encode('utf-8')).hexdigest(), 16)
        
        # Use hash to seed embedding
        for i in range(dimension):
            seed = (hash_value + i * 31) % 1000000
            embedding[i] = seed / 1000000.0
        
        # Normalize embedding
        magnitude = np.sqrt(np.sum(np.array(embedding) ** 2))
        if magnitude > 0:
            embedding = [val / magnitude for val in embedding]
        
        return embedding
    
    def calculate_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Similarity score
        """
        if len(embedding1) != len(embedding2):
            raise ValueError("Embedding dimensions must match")
        
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        magnitude1 = np.sqrt(sum(a * a for a in embedding1))
        magnitude2 = np.sqrt(sum(b * b for b in embedding2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    async def find_similar(
        self,
        query_embedding: List[float],
        chunks: List[Dict[str, Any]],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find most similar chunks.
        
        Args:
            query_embedding: Query embedding vector
            chunks: Chunks to search
            top_k: Number of top results to return
            
        Returns:
            List of similar chunks with similarity scores
        """
        similarities = []
        
        for chunk in chunks:
            similarity = self.calculate_similarity(
                query_embedding,
                chunk["embedding"]
            )
            similarities.append({
                "chunk": chunk,
                "similarity": similarity
            })
        
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:top_k]
    
    async def cache_embedding(
        self,
        text_hash: str,
        embedding: List[float]
    ) -> None:
        """
        Cache embedding to disk.
        
        Args:
            text_hash: Hash of text content
            embedding: Embedding vector
        """
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            cache_path = self.cache_dir / f"{text_hash}.json"
            
            with open(cache_path, 'w') as f:
                json.dump(embedding, f)
        except Exception as error:
            logger.warning("Failed to cache embedding", {"error": str(error)})
    
    async def load_cached_embedding(
        self,
        text_hash: str
    ) -> List[float]:
        """
        Load cached embedding from disk.
        
        Args:
            text_hash: Hash of text content
            
        Returns:
            Cached embedding or None
        """
        try:
            cache_path = self.cache_dir / f"{text_hash}.json"
            
            if cache_path.exists():
                with open(cache_path, 'r') as f:
                    return json.load(f)
            return None
        except Exception:
            return None
    
    async def batch_generate_with_cache(
        self,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Batch generate embeddings with caching.
        
        Args:
            chunks: Chunks to process
            
        Returns:
            Chunks with embeddings
        """
        results = []
        cache_hits = []
        cache_misses = []
        
        for chunk in chunks:
            text_hash = chunk["metadata"].get("content_hash", "")
            cached = await self.load_cached_embedding(text_hash)
            
            if cached:
                chunk_with_embedding = chunk.copy()
                chunk_with_embedding["embedding"] = cached
                chunk_with_embedding["metadata"] = {
                    **chunk.get("metadata", {}),
                    "embedding_model": self.embedding_model,
                    "embedding_dimension": len(cached),
                    "cached": True
                }
                results.append(chunk_with_embedding)
                cache_hits.append(chunk["id"])
            else:
                embedding = await self.generate_embedding(chunk["content"])
                await self.cache_embedding(text_hash, embedding)
                
                chunk_with_embedding = chunk.copy()
                chunk_with_embedding["embedding"] = embedding
                chunk_with_embedding["metadata"] = {
                    **chunk.get("metadata", {}),
                    "embedding_model": self.embedding_model,
                    "embedding_dimension": len(embedding),
                    "cached": False
                }
                results.append(chunk_with_embedding)
                cache_misses.append(chunk["id"])
        
        logger.info("Batch embedding generation complete", {
            "total": len(chunks),
            "cache_hits": len(cache_hits),
            "cache_misses": len(cache_misses)
        })
        
        return results
