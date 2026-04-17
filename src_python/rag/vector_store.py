"""
Vector Store Module
Manages storage and retrieval of document embeddings.
"""

import json
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

import numpy as np

from ..utils.logger import get_logger
from ..utils.config import RAGConfig


logger = get_logger("vector-store")


class VectorStore:
    """
    Store for document embeddings with search capabilities.
    """
    
    def __init__(self, config: RAGConfig):
        """
        Initialize vector store.
        
        Args:
            config: RAG configuration
        """
        self.config = config
        self.store_path = Path(config.vector_store_path) / "vectors"
        self.index_path = Path(config.vector_store_path) / "index.json"
        self.max_documents = config.max_documents
        self.index: Dict[str, Dict[str, Any]] = {}
    
    async def initialize(self) -> None:
        """
        Initialize vector store.
        """
        try:
            self.store_path.mkdir(parents=True, exist_ok=True)
            await self.load_index()
            logger.info("Vector store initialized")
        except Exception as error:
            logger.error("Error initializing vector store", {"error": str(error)})
            raise
    
    async def store(
        self,
        chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Store document chunks with embeddings.
        
        Args:
            chunks: Chunks with embeddings to store
            
        Returns:
            Storage result with document ID
        """
        try:
            await self.initialize()
            
            document_id = f"doc-{datetime.now().timestamp()}-{uuid.uuid4().hex[:8]}"
            doc_path = self.store_path / f"{document_id}.json"
            
            document = {
                "id": document_id,
                "chunks": [
                    {
                        "id": chunk["id"],
                        "content": chunk["content"],
                        "embedding": chunk["embedding"],
                        "metadata": chunk.get("metadata", {})
                    }
                    for chunk in chunks
                ],
                "timestamp": datetime.now().isoformat(),
                "chunk_count": len(chunks)
            }
            
            # Save document to disk
            with open(doc_path, 'w', encoding='utf-8') as f:
                json.dump(document, f, ensure_ascii=False, indent=2)
            
            # Update index
            self.index[document_id] = {
                "id": document_id,
                "path": str(doc_path),
                "timestamp": document["timestamp"],
                "chunk_count": document["chunk_count"],
                "source": chunks[0].get("source", "") if chunks else ""
            }
            
            await self.save_index()
            
            logger.info("Document stored successfully", {
                "document_id": document_id,
                "chunk_count": chunks
            })
            
            return {"id": document_id, "chunk_count": len(chunks)}
            
        except Exception as error:
            logger.error("Error storing document", {"error": str(error)})
            raise
    
    async def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filters: Optional filters for search
            
        Returns:
            List of similar chunks with similarity scores
        """
        try:
            await self.initialize()
            
            results = []
            document_ids = list(self.index.keys())
            
            for doc_id in document_ids:
                doc = await self.load_document(doc_id)
                if not doc:
                    continue
                
                for chunk in doc["chunks"]:
                    # Apply filters
                    if filters:
                        if "type" in filters and chunk["metadata"].get("type") != filters["type"]:
                            continue
                        if "source" in filters and chunk["metadata"].get("source") != filters["source"]:
                            continue
                    
                    # Calculate similarity
                    similarity = self._calculate_cosine_similarity(
                        query_embedding,
                        chunk["embedding"]
                    )
                    
                    results.append({
                        "document_id": doc_id,
                        "chunk_id": chunk["id"],
                        "content": chunk["content"],
                        "metadata": chunk["metadata"],
                        "similarity": similarity
                    })
            
            # Sort by similarity and return top K
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:top_k]
            
        except Exception as error:
            logger.error("Error searching vector store", {"error": str(error)})
            raise
    
    async def load_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Load document from disk.
        
        Args:
            document_id: Document ID to load
            
        Returns:
            Document data or None if not found
        """
        try:
            doc_info = self.index.get(document_id)
            if not doc_info:
                logger.warning(f"Document not found in index: {document_id}")
                return None
            
            with open(doc_info["path"], 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as error:
            logger.error("Error loading document", {
                "document_id": document_id,
                "error": str(error)
            })
            return None
    
    async def delete_document(self, document_id: str) -> bool:
        """
        Delete document from store.
        
        Args:
            document_id: Document ID to delete
            
        Returns:
            True if deleted successfully
        """
        try:
            doc_info = self.index.get(document_id)
            if not doc_info:
                logger.warning(f"Document not found: {document_id}")
                return False
            
            # Delete file
            Path(doc_info["path"]).unlink()
            
            # Remove from index
            del self.index[document_id]
            await self.save_index()
            
            logger.info(f"Document deleted: {document_id}")
            return True
            
        except Exception as error:
            logger.error("Error deleting document", {
                "document_id": document_id,
                "error": str(error)
            })
            raise
    
    async def save_index(self) -> None:
        """
        Save index to disk.
        """
        try:
            with open(self.index_path, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, ensure_ascii=False, indent=2)
        except Exception as error:
            logger.error("Error saving index", {"error": str(error)})
            raise
    
    async def load_index(self) -> None:
        """
        Load index from disk.
        """
        try:
            if self.index_path.exists():
                with open(self.index_path, 'r', encoding='utf-8') as f:
                    self.index = json.load(f)
                logger.info(f"Loaded {len(self.index)} documents from index")
            else:
                # Index doesn't exist yet, create empty index
                self.index = {}
                await self.save_index()
        except Exception:
            self.index = {}
            await self.save_index()
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get store statistics.
        
        Returns:
            Statistics dictionary
        """
        await self.initialize()
        
        document_ids = list(self.index.keys())
        total_chunks = sum(
            self.index[doc_id]["chunk_count"]
            for doc_id in document_ids
        )
        
        return {
            "total_documents": len(document_ids),
            "total_chunks": total_chunks,
            "max_documents": self.max_documents,
            "available_space": self.max_documents - len(document_ids)
        }
    
    async def clear(self) -> None:
        """
        Clear all documents from store.
        """
        try:
            document_ids = list(self.index.keys())
            
            for doc_id in document_ids:
                await self.delete_document(doc_id)
            
            logger.info("Vector store cleared")
        except Exception as error:
            logger.error("Error clearing vector store", {"error": str(error)})
            raise
    
    def _calculate_cosine_similarity(
        self,
        vec1: List[float],
        vec2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Similarity score
        """
        if len(vec1) != len(vec2):
            raise ValueError("Vector dimensions must match")
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = np.sqrt(sum(a * a for a in vec1))
        magnitude2 = np.sqrt(sum(b * b for b in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    async def export(self, output_path: str) -> str:
        """
        Export vector store data.
        
        Args:
            output_path: Path to export data
            
        Returns:
            Path to exported data
        """
        try:
            stats = await self.get_stats()
            export_data = {
                "stats": stats,
                "index": self.index,
                "exported_at": datetime.now().isoformat()
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Vector store exported to {output_path}")
            return output_path
        except Exception as error:
            logger.error("Error exporting vector store", {"error": str(error)})
            raise
