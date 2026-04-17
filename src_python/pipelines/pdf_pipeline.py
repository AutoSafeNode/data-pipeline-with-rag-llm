"""
PDF to RAG Pipeline
Processes PDF files and converts them to RAG-ready format.
"""

import asyncio
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from ..processors.pdf_processor import PDFProcessor
from ..processors.text_processor import TextProcessor
from ..rag.embeddings import EmbeddingGenerator
from ..rag.vector_store import VectorStore
from ..utils.logger import get_logger
from ..utils.config import PipelineConfig


logger = get_logger("pdf-pipeline")


class PDFToRAGPipeline:
    """
    Pipeline for converting PDF files to RAG format.
    """
    
    def __init__(self, config: PipelineConfig):
        """
        Initialize PDF pipeline.
        
        Args:
            config: Pipeline configuration
        """
        self.config = config
        self.pdf_processor = PDFProcessor(config)
        self.text_processor = TextProcessor(config)
        self.embedding_generator = EmbeddingGenerator(config)
        self.vector_store = VectorStore(config)
    
    async def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process single PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Processing result
        """
        try:
            logger.info(f"Processing PDF file: {file_path}")
            
            # Step 1: Read and extract data from PDF
            pdf_data = await self.pdf_processor.read_pdf(file_path)
            
            # Step 2: Convert to chunks
            chunks = await self.pdf_processor.convert_to_chunks(
                pdf_data,
                Path(file_path).name
            )
            
            # Step 3: Process and validate chunks
            processed_chunks = self.text_processor.process_chunks(chunks)
            
            # Step 4: Generate embeddings for chunks
            chunks_with_embeddings = await self.embedding_generator.generate_embeddings(
                processed_chunks
            )
            
            # Step 5: Store in vector store
            store_result = await self.vector_store.store(chunks_with_embeddings)
            
            logger.info("PDF file processed successfully", {
                "file_name": Path(file_path).name,
                "pages": pdf_data["pages"],
                "total_chunks": len(processed_chunks),
                "store_result": store_result
            })
            
            return {
                "success": True,
                "file_name": Path(file_path).name,
                "pages": pdf_data["pages"],
                "chunks": len(processed_chunks),
                "embeddings": len(chunks_with_embeddings),
                "vector_store_id": store_result["id"],
                "structured_data": pdf_data.get("structured_data", {})
            }
        except Exception as error:
            logger.error(f"Error processing PDF file: {file_path}", {
                "error": str(error)
            })
            raise
    
    async def process_directory(self, input_dir: str) -> Dict[str, Any]:
        """
        Process all PDF files in directory.
        
        Args:
            input_dir: Directory containing PDF files
            
        Returns:
            Processing results summary
        """
        try:
            logger.info(f"Processing PDF files from directory: {input_dir}")
            
            input_path = Path(input_dir)
            if not input_path.exists():
                raise FileNotFoundError(f"Directory not found: {input_dir}")
            
            # Find PDF files
            pdf_files = [
                f for f in input_path.iterdir()
                if f.is_file() and f.suffix == '.pdf'
            ]
            
            if not pdf_files:
                logger.warning("No PDF files found in directory")
                return {"processed": 0, "results": []}
            
            logger.info(f"Found {len(pdf_files)} PDF files to process")
            
            results = []
            for file in pdf_files:
                try:
                    result = await self.process_file(str(file))
                    results.append(result)
                except Exception as error:
                    logger.error(f"Failed to process {file.name}", {
                        "error": str(error)
                    })
                    results.append({
                        "success": False,
                        "file_name": file.name,
                        "error": str(error)
                    })
            
            successful = sum(1 for r in results if r.get("success", False))
            
            logger.info("Directory processing complete", {
                "total": len(pdf_files),
                "successful": successful,
                "failed": len(pdf_files) - successful
            })
            
            return {
                "processed": len(pdf_files),
                "successful": successful,
                "failed": len(pdf_files) - successful,
                "results": results
            }
        except Exception as error:
            logger.error("Error processing directory", {"error": str(error)})
            raise
    
    async def save_to_file(self, data: Dict[str, Any], output_path: str) -> str:
        """
        Save processed data to file.
        
        Args:
            data: Data to save
            output_path: Output file path
            
        Returns:
            Path to saved file
        """
        try:
            import json
            
            output_file_path = Path(output_path)
            output_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Data saved to {output_path}")
            return str(output_path)
        except Exception as error:
            logger.error("Error saving data to file", {"error": str(error)})
            raise
    
    async def run(self, input_path: str) -> Dict[str, Any]:
        """
        Main execution method.
        
        Args:
            input_path: Input file or directory path
            
        Returns:
            Processing results
        """
        try:
            path = Path(input_path)
            
            if path.is_dir():
                result = await self.process_directory(input_path)
            else:
                result = await self.process_file(input_path)
            
            # Save results
            timestamp = datetime.now().isoformat().replace(":", "-")
            output_path = Path(self.config.output_dir) / f"pdf-rag-{timestamp}.json"
            await self.save_to_file(result, str(output_path))
            
            return result
        except Exception as error:
            logger.error("Pipeline execution failed", {"error": str(error)})
            raise


async def main():
    """
    Main entry point for PDF pipeline.
    """
    import sys
    from ..utils.config import load_config
    
    config = load_config()
    pipeline_config = config.pipelines["pdf"]
    
    pipeline = PDFToRAGPipeline(pipeline_config)
    
    input_path = sys.argv[1] if len(sys.argv) > 1 else pipeline_config.input_dir
    
    try:
        result = await pipeline.run(input_path)
        logger.info("PDF pipeline completed successfully")
        sys.exit(0)
    except Exception as error:
        logger.error("PDF pipeline failed", {"error": str(error)})
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
