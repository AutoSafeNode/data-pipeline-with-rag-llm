"""
Text Processor Module
Handles text processing and normalization for RAG.
"""

import hashlib
from typing import Dict, List, Any

from ..utils.logger import get_logger


logger = get_logger("text-processor")


class TextProcessor:
    """
    Processor for text normalization and validation.
    """
    
    def __init__(self, config: Any):
        """
        Initialize text processor.
        
        Args:
            config: Configuration with min/max chunk sizes
        """
        self.min_chunk_size = getattr(config, 'min_chunk_size', 100)
        self.max_chunk_size = getattr(config, 'max_chunk_size', 2000)
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text content.
        
        Args:
            text: Text to normalize
            
        Returns:
            Normalized text
        """
        if not text:
            return ""
        
        # Multiple spaces to single space
        text = " ".join(text.split())
        # Multiple newlines to double newline
        text = "\n\n".join(text.split("\n\n"))
        # Tabs to spaces
        text = text.replace("\t", " ")
        
        return text.strip()
    
    def extract_key_info(self, text: str) -> Dict[str, Any]:
        """
        Extract key information from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentences and keywords
        """
        info = {
            "sentences": [],
            "keywords": []
        }
        
        # Extract sentences (simple version)
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        info["sentences"] = sentences
        
        # Extract potential keywords (capitalized words)
        words = text.split()
        info["keywords"] = [
            word for word in words
            if len(word) > 3 and word[0].isupper() and not word.islower()
        ]
        
        return info
    
    def validate_chunk(self, chunk: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate chunk quality.
        
        Args:
            chunk: Chunk to validate
            
        Returns:
            Validation result with valid flag and reason
        """
        if not chunk or not chunk.get("content"):
            return {"valid": False, "reason": "No content"}
        
        content = chunk["content"]
        
        if len(content) < self.min_chunk_size:
            return {"valid": False, "reason": "Chunk too small"}
        
        if len(content) > self.max_chunk_size:
            return {"valid": False, "reason": "Chunk too large"}
        
        # Check for meaningful content
        meaningful_chars = len([c for c in content if c.isalnum() or ord(c) > 127])
        if meaningful_chars < len(content) * 0.3:
            return {"valid": False, "reason": "Not enough meaningful content"}
        
        return {"valid": True}
    
    def enhance_chunk(self, chunk: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance chunk with additional metadata.
        
        Args:
            chunk: Chunk to enhance
            
        Returns:
            Enhanced chunk
        """
        info = self.extract_key_info(chunk["content"])
        
        enhanced = chunk.copy()
        enhanced["metadata"] = {
            **chunk.get("metadata", {}),
            "sentence_count": len(info["sentences"]),
            "keyword_count": len(info["keywords"]),
            "content_hash": self._generate_hash(chunk["content"])
        }
        
        return enhanced
    
    def _generate_hash(self, content: str) -> str:
        """
        Generate hash for content.
        
        Args:
            content: Content to hash
            
        Returns:
            Hex string hash
        """
        hash_obj = hashlib.md5(content.encode('utf-8'))
        return hash_obj.hexdigest()
    
    def process_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process and validate chunks.
        
        Args:
            chunks: Chunks to process
            
        Returns:
            List of valid chunks
        """
        valid_chunks = []
        
        for chunk in chunks:
            validation = self.validate_chunk(chunk)
            
            if validation["valid"]:
                enhanced = self.enhance_chunk(chunk)
                valid_chunks.append(enhanced)
            else:
                logger.warning("Invalid chunk skipped", {
                    "chunk_id": chunk.get("id"),
                    "reason": validation["reason"]
                })
        
        logger.info(f"Processed {len(chunks)} chunks, {len(valid_chunks)} valid")
        return valid_chunks
    
    def merge_small_chunks(
        self,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Merge small chunks.
        
        Args:
            chunks: Chunks to merge
            
        Returns:
            List of merged chunks
        """
        merged = []
        current_merged = None
        
        for chunk in chunks:
            if len(chunk["content"]) < self.min_chunk_size:
                if current_merged:
                    current_merged["content"] += "\n\n" + chunk["content"]
                    current_merged["metadata"]["merged_count"] = \
                        current_merged["metadata"].get("merged_count", 1) + 1
                else:
                    current_merged = chunk.copy()
                    current_merged["metadata"]["merged_count"] = 1
            else:
                if current_merged:
                    merged.append(current_merged)
                    current_merged = None
                merged.append(chunk)
        
        if current_merged:
            merged.append(current_merged)
        
        return merged
