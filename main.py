"""
Data Scooper - Main Entry Point
Data pipeline for converting Excel/PDF to RAG and LLM integration.
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Any

from src_python.utils.logger import get_logger
from src_python.utils.config import load_config
from src_python.pipelines.excel_pipeline import ExcelToRAGPipeline
from src_python.pipelines.pdf_pipeline import PDFToRAGPipeline
from src_python.llm.gemini_client import GeminiApiClient


logger = get_logger("data-scooper")


class DataScooper:
    """
    Main data scooper class for coordinating pipelines.
    """
    
    def __init__(self, config: Any):
        """
        Initialize data scooper.
        
        Args:
            config: Configuration object
        """
        self.config = config
    
    async def process_excel(self, input_path: str) -> Dict[str, Any]:
        """
        Process Excel files to RAG.
        
        Args:
            input_path: Path to Excel file or directory
            
        Returns:
            Processing results
        """
        try:
            logger.info("Starting Excel to RAG pipeline")
            pipeline = ExcelToRAGPipeline(self.config.pipelines["excel"])
            result = await pipeline.run(input_path)
            logger.info("Excel pipeline completed", {"result": result})
            return result
        except Exception as error:
            logger.error("Excel pipeline failed", {"error": str(error)})
            raise
    
    async def process_pdf(self, input_path: str) -> Dict[str, Any]:
        """
        Process PDF files to RAG.
        
        Args:
            input_path: Path to PDF file or directory
            
        Returns:
            Processing results
        """
        try:
            logger.info("Starting PDF to RAG pipeline")
            pipeline = PDFToRAGPipeline(self.config.pipelines["pdf"])
            result = await pipeline.run(input_path)
            logger.info("PDF pipeline completed", {"result": result})
            return result
        except Exception as error:
            logger.error("PDF pipeline failed", {"error": str(error)})
            raise
    
    async def query_with_rag(
        self,
        query: str,
        rag_data: Dict[str, Any]
    ) -> str:
        """
        Query LLM with RAG context.
        
        Args:
            query: Query text
            rag_data: RAG context data
            
        Returns:
            LLM response
        """
        try:
            logger.info("Querying LLM with RAG context")
            client = GeminiApiClient(self.config.gemini)
            
            from src_python.llm.gemini_client import APIRequest
            
            api_request = APIRequest(
                system_instruction={
                    "parts": [{
                        "text": "You are a helpful assistant that answers questions based on the provided context."
                    }]
                },
                contents=[{
                    "parts": [{
                        "text": f"Context: {rag_data}\n\nQuestion: {query}"
                    }]
                }]
            )
            
            response = await client.generate_content(api_request)
            logger.info("LLM query completed")
            return response
        except Exception as error:
            logger.error("LLM query failed", {"error": str(error)})
            raise
    
    async def run_complete_pipeline(
        self,
        excel_path: str = None,
        pdf_path: str = None
    ) -> Dict[str, Any]:
        """
        Run complete pipeline.
        
        Args:
            excel_path: Optional Excel input path
            pdf_path: Optional PDF input path
            
        Returns:
            Combined results
        """
        try:
            logger.info("Starting complete data pipeline")
            
            results = {}
            
            if excel_path:
                results["excel"] = await self.process_excel(excel_path)
            
            if pdf_path:
                results["pdf"] = await self.process_pdf(pdf_path)
            
            logger.info("Complete pipeline finished", {"results": results})
            return results
        except Exception as error:
            logger.error("Complete pipeline failed", {"error": str(error)})
            raise


def print_usage():
    """Print usage information."""
    print("""
Usage: python main.py <command> [options]

Commands:
  excel <path>    Process Excel files to RAG
  pdf <path>      Process PDF files to RAG
  all <excel> <pdf>  Process both Excel and PDF files

Examples:
  python main.py excel ./data/input/excel
  python main.py pdf ./data/input/pdf
  python main.py all ./data/input/excel ./data/input/pdf
    """)


async def main():
    """
    Main entry point.
    """
    try:
        config = load_config()
        scooper = DataScooper(config)
        
        if len(sys.argv) < 2:
            print_usage()
            sys.exit(1)
        
        command = sys.argv[1]
        
        if command == "excel":
            input_path = sys.argv[2] if len(sys.argv) > 2 else config.pipelines["excel"].input_dir
            await scooper.process_excel(input_path)
            sys.exit(0)
        
        elif command == "pdf":
            input_path = sys.argv[2] if len(sys.argv) > 2 else config.pipelines["pdf"].input_dir
            await scooper.process_pdf(input_path)
            sys.exit(0)
        
        elif command == "all":
            excel_input = sys.argv[2] if len(sys.argv) > 2 else None
            pdf_input = sys.argv[3] if len(sys.argv) > 3 else None
            await scooper.run_complete_pipeline(excel_input, pdf_input)
            sys.exit(0)
        
        else:
            print_usage()
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        sys.exit(1)
    except Exception as error:
        logger.error("Pipeline execution failed", {"error": str(error)})
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
