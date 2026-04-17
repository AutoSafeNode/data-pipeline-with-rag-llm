"""
PDF Data Processor Module
Handles reading and extracting data from PDF files.
"""

import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib

import PyPDF2
import pdfplumber

from ..utils.logger import get_logger
from ..utils.config import PipelineConfig


logger = get_logger("pdf-processor")


class PDFProcessor:
    """
    Processor for PDF files.
    """
    
    def __init__(self, config: PipelineConfig):
        """
        Initialize PDF processor.
        
        Args:
            config: Pipeline configuration
        """
        self.config = config
        self.chunk_size = config.chunk_size
        self.chunk_overlap = config.chunk_overlap
    
    async def read_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        Read PDF file and extract text.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            PDF data with text and metadata
            
        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: If reading fails
        """
        try:
            logger.info(f"Reading PDF file: {file_path}")
            
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Extract text using pdfplumber
            text = ""
            pages = 0
            metadata = {}
            
            with pdfplumber.open(file_path) as pdf:
                pages = len(pdf.pages)
                
                # Extract metadata
                if hasattr(pdf, 'metadata') and pdf.metadata:
                    metadata = {
                        "author": pdf.metadata.get('Author', ''),
                        "title": pdf.metadata.get('Title', ''),
                        "subject": pdf.metadata.get('Subject', ''),
                        "creator": pdf.metadata.get('Creator', '')
                    }
                
                # Extract text from all pages
                for page in pdf.pages:
                    text += page.extract_text() or ""
            
            result = {
                "text": text,
                "pages": pages,
                "metadata": metadata
            }
            
            logger.info("PDF file processed successfully", {
                "pages": pages,
                "text_length": len(text)
            })
            
            return result
            
        except Exception as error:
            logger.error("Error reading PDF file", {"error": str(error)})
            raise
    
    async def convert_to_chunks(
        self,
        pdf_data: Dict[str, Any],
        file_name: str
    ) -> List[Dict[str, Any]]:
        """
        Convert PDF text to chunks for RAG.
        
        Args:
            pdf_data: Extracted PDF data
            file_name: Name of PDF file
            
        Returns:
            List of text chunks
        """
        try:
            chunks = []
            text = pdf_data["text"]
            
            # Split into pages (approximately)
            page_texts = self._split_into_pages(text, pdf_data["pages"])
            
            chunk_index = 0
            current_page = 1
            current_chunk = ""
            
            for page_text in page_texts:
                paragraphs = page_text.split("\n\n")
                
                for paragraph in paragraphs:
                    if len(current_chunk + paragraph) > self.chunk_size:
                        if current_chunk:
                            chunks.append({
                                "id": f"{file_name}-page-{current_page}-chunk-{chunk_index}",
                                "source": file_name,
                                "content": current_chunk.strip(),
                                "metadata": {
                                    "type": "pdf",
                                    "page": current_page,
                                    "chunk_index": chunk_index,
                                    "length": len(current_chunk),
                                    **pdf_data["metadata"]
                                }
                            })
                            chunk_index += 1
                            
                            # Create overlap
                            sentences = current_chunk.split(". ")
                            overlap_sentences = sentences[-2:]
                            current_chunk = ". ".join(overlap_sentences) + ". " + paragraph
                        else:
                            current_chunk = paragraph
                    else:
                        current_chunk += ("\n\n" if current_chunk else "") + paragraph
                
                current_page += 1
                chunk_index = 0  # Reset chunk index for each page
            
            # Add final chunk
            if current_chunk:
                chunks.append({
                    "id": f"{file_name}-page-{current_page}-chunk-{chunk_index}",
                    "source": file_name,
                    "content": current_chunk.strip(),
                    "metadata": {
                        "type": "pdf",
                        "page": current_page,
                        "chunk_index": chunk_index,
                        "length": len(current_chunk),
                        **pdf_data["metadata"]
                    }
                })
            
            logger.info(f"Created {len(chunks)} text chunks from PDF")
            return chunks
            
        except Exception as error:
            logger.error("Error converting PDF to chunks", {"error": str(error)})
            raise
    
    def _split_into_pages(self, text: str, total_pages: int) -> List[str]:
        """
        Split text into pages.
        
        Args:
            text: Full text
            total_pages: Total number of pages
            
        Returns:
            List of page texts
        """
        # Split by approximate page length
        avg_chars_per_page = max(1, len(text) // total_pages)
        pages = []
        
        for i in range(0, len(text), avg_chars_per_page):
            pages.append(text[i:i + avg_chars_per_page])
        
        return pages
    
    def _extract_structured_data(self, text: str) -> Dict[str, List[str]]:
        """
        Extract structured data from PDF.
        
        Args:
            text: PDF text
            
        Returns:
            Structured data with headings and key points
        """
        structured_data = {
            "headings": [],
            "tables": [],
            "key_points": []
        }
        
        # Extract headings (lines in ALL CAPS or ending with :)
        lines = text.split("\n")
        structured_data["headings"] = [
            line for line in lines
            if line.strip() and (line.isupper() or line.strip().endswith(":"))
        ]
        
        # Extract key points (lines starting with bullets or numbers)
        structured_data["key_points"] = [
            line for line in lines
            if line.strip().startswith(("*", "-", "•")) or line.strip().match(r"^\d+\.")
        ]
        
        return structured_data
    
    async def process(self, file_path: str) -> Dict[str, Any]:
        """
        Process PDF file and return chunks ready for RAG.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Processed data with chunks
        """
        pdf_data = await self.read_pdf(file_path)
        chunks = await self.convert_to_chunks(pdf_data, Path(file_path).name)
        
        structured_data = self._extract_structured_data(pdf_data["text"])
        
        return {
            "source": Path(file_path).name,
            "type": "pdf",
            "chunks": chunks,
            "structured_data": structured_data,
            "metadata": {
                "pages": pdf_data["pages"],
                "total_chunks": len(chunks),
                **pdf_data["metadata"]
            }
        }
