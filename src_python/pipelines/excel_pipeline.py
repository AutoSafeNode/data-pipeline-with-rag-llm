"""
Excel to RAG Pipeline
Processes Excel files and converts them to RAG-ready format.
"""

import asyncio
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from ..processors.excel_processor import ExcelProcessor
from ..processors.text_processor import TextProcessor
from ..rag.embeddings import EmbeddingGenerator
from ..rag.vector_store import VectorStore
from ..utils.logger import get_logger
from ..utils.config import PipelineConfig


logger = get_logger("excel-pipeline")


class ExcelToRAGPipeline:
    """
    Pipeline for converting Excel files to RAG format.
    """
    
    def __init__(self, config: PipelineConfig):
        """
        Initialize Excel pipeline.
        
        Args:
            config: Pipeline configuration
        """
        self.config = config
        self.excel_processor = ExcelProcessor(config)
        self.text_processor = TextProcessor(config)
        self.embedding_generator = EmbeddingGenerator(config)
        self.vector_store = VectorStore(config)
    
    async def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process single Excel file.
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            Processing result
        """
        try:
            logger.info(f"Processing Excel file: {file_path}")
            
            # Step 1: Read and extract data from Excel
            excel_data = await self.excel_processor.read_excel(file_path)
            
            # Step 2: Convert to chunks
            chunks = await self.excel_processor.convert_to_chunks(excel_data)
            
            # Step 3: Process and validate chunks
            processed_chunks = self.text_processor.process_chunks(chunks)
            
            # Step 4: Generate embeddings for chunks
            chunks_with_embeddings = await self.embedding_generator.generate_embeddings(
                processed_chunks
            )
            
            # Step 5: Store in vector store
            store_result = await self.vector_store.store(chunks_with_embeddings)
            
            logger.info("Excel file processed successfully", {
                "file_name": Path(file_path).name,
                "total_chunks": len(processed_chunks),
                "store_result": store_result
            })
            
            return {
                "success": True,
                "file_name": Path(file_path).name,
                "chunks": len(processed_chunks),
                "embeddings": len(chunks_with_embeddings),
                "vector_store_id": store_result["id"]
            }
        except Exception as error:
            logger.error(f"Error processing Excel file: {file_path}", {
                "error": str(error)
            })
            raise
    
    async def process_directory(self, input_dir: str) -> Dict[str, Any]:
        """
        Process all Excel files in directory.
        
        Args:
            input_dir: Directory containing Excel files
            
        Returns:
            Processing results summary
        """
        try:
            logger.info(f"Processing Excel files from directory: {input_dir}")
            
            input_path = Path(input_dir)
            if not input_path.exists():
                raise FileNotFoundError(f"Directory not found: {input_dir}")
            
            # Find Excel files
            excel_files = [
                f for f in input_path.iterdir()
                if f.is_file() and f.suffix in ['.xlsx', '.xls', '.xlsm']
            ]
            
            if not excel_files:
                logger.warning("No Excel files found in directory")
                return {"processed": 0, "results": []}
            
            logger.info(f"Found {len(excel_files)} Excel files to process")
            
            results = []
            for file in excel_files:
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
                "total": len(excel_files),
                "successful": successful,
                "failed": len(excel_files) - successful
            })
            
            return {
                "processed": len(excel_files),
                "successful": successful,
                "failed": len(excel_files) - successful,
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
            output_path = Path(self.config.output_dir) / f"excel-rag-{timestamp}.json"
            await self.save_to_file(result, str(output_path))
            
            return result
        except Exception as error:
            logger.error("Pipeline execution failed", {"error": str(error)})
            raise


async def main():
    """
    Main entry point for Excel pipeline.
    """
    import sys
    from ..utils.config import load_config
    
    config = load_config()
    pipeline_config = config.pipelines["excel"]
    
    pipeline = ExcelToRAGPipeline(pipeline_config)
    
    input_path = sys.argv[1] if len(sys.argv) > 1 else pipeline_config.input_dir
    
    try:
        result = await pipeline.run(input_path)
        logger.info("Excel pipeline completed successfully")
        sys.exit(0)
    except Exception as error:
        logger.error("Excel pipeline failed", {"error": str(error)})
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
