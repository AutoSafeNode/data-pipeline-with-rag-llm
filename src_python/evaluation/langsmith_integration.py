"""
LangSmith Integration Module
Integrates with LangSmith for tracing and monitoring RAG systems
"""

import os
import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from functools import wraps

from langsmith import traceable, Client
from langchain.callbacks import LangChainTracer
from langchain.schema import BaseMessage, HumanMessage, AIMessage

from ..utils.logger import get_logger
from ..utils.config import load_config


logger = get_logger("langsmith-integration")


class LangSmithIntegration:
    """
    Integration with LangSmith for RAG system monitoring and debugging.
    """
    
    def __init__(self, config: Any):
        """
        Initialize LangSmith integration.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.langsmith_config = config.evaluation.langsmith
        
        # Initialize LangSmith client
        self.client = None
        
        if self.langsmith_config.enableTracing:
            self._initialize_langsmith()
        
        logger.info("LangSmith integration initialized", {
            "project_name": self.langsmith_config.projectName,
            "enabled": self.langsmith_config.enableTracing
        })
    
    def _initialize_langsmith(self):
        """Initialize LangSmith client and tracing."""
        try:
            # Set environment variables for LangSmith
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
            os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
            os.environ["LANGCHAIN_PROJECT"] = self.langsmith_config.projectName
            
            # Initialize client
            self.client = Client(
                api_url=os.environ["LANGCHAIN_ENDPOINT"],
                api_key=os.environ["LANGCHAIN_API_KEY"]
            )
            
            logger.info("LangSmith client initialized successfully")
            
        except Exception as error:
            logger.warning("Failed to initialize LangSmith client", {
                "error": str(error)
            })
            self.client = None
    
    @traceable(name="rag_query")
    async def trace_rag_query(
        self,
        question: str,
        context: List[str],
        answer: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Trace a RAG query with LangSmith.
        
        Args:
            question: User question
            context: Retrieved context passages
            answer: Generated answer
            metadata: Additional metadata
            
        Returns:
            Tracing result
        """
        if not self.client:
            logger.debug("LangSmith tracing disabled")
            return {
                "question": question,
                "context": context,
                "answer": answer,
                "metadata": metadata
            }
        
        try:
            # Create run in LangSmith
            run_data = {
                "question": question,
                "context": context,
                "answer": answer,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            logger.info("RAG query traced with LangSmith", {
                "question_length": len(question),
                "context_count": len(context),
                "answer_length": len(answer)
            })
            
            return run_data
            
        except Exception as error:
            logger.error("Failed to trace RAG query", {"error": str(error)})
            return {
                "question": question,
                "context": context,
                "answer": answer,
                "metadata": metadata,
                "error": str(error)
            }
    
    @traceable(name="document_processing")
    async def trace_document_processing(
        self,
        file_path: str,
        chunk_count: int,
        processing_time: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Trace document processing pipeline.
        
        Args:
            file_path: Path to processed document
            chunk_count: Number of chunks created
            processing_time: Time taken for processing
            metadata: Additional metadata
            
        Returns:
            Tracing result
        """
        if not self.client:
            logger.debug("LangSmith tracing disabled")
            return {
                "file_path": file_path,
                "chunk_count": chunk_count,
                "processing_time": processing_time
            }
        
        try:
            run_data = {
                "file_path": file_path,
                "chunk_count": chunk_count,
                "processing_time": processing_time,
                "chunks_per_second": chunk_count / processing_time if processing_time > 0 else 0,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            logger.info("Document processing traced", {
                "file_path": file_path,
                "chunk_count": chunk_count
            })
            
            return run_data
            
        except Exception as error:
            logger.error("Failed to trace document processing", {"error": str(error)})
            return {
                "file_path": file_path,
                "chunk_count": chunk_count,
                "processing_time": processing_time,
                "error": str(error)
            }
    
    def create_traceable_decorator(
        self,
        name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Callable:
        """
        Create a custom traceable decorator.
        
        Args:
            name: Name for the trace
            metadata: Default metadata for the trace
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                if not self.client:
                    return await func(*args, **kwargs)
                
                start_time = datetime.now()
                try:
                    result = await func(*args, **kwargs)
                    end_time = datetime.now()
                    
                    execution_time = (end_time - start_time).total_seconds()
                    
                    logger.info(f"Traced execution of {name}", {
                        "execution_time": execution_time,
                        "success": True
                    })
                    
                    return result
                    
                except Exception as error:
                    end_time = datetime.now()
                    execution_time = (end_time - start_time).total_seconds()
                    
                    logger.error(f"Traced execution of {name} failed", {
                        "execution_time": execution_time,
                        "error": str(error)
                    })
                    
                    raise
            
            return async_wrapper
        
        return decorator
    
    async def get_run_statistics(
        self,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get statistics about traced runs.
        
        Args:
            limit: Maximum number of runs to analyze
            
        Returns:
            Statistics dictionary
        """
        if not self.client:
            return {
                "status": "disabled",
                "message": "LangSmith tracing is not enabled"
            }
        
        try:
            # Get recent runs from the project
            runs = self.client.list_runs(
                project_name=self.langsmith_config.projectName,
                limit=limit
            )
            
            run_count = len(runs)
            
            # Calculate basic statistics
            execution_times = []
            error_count = 0
            
            for run in runs:
                if hasattr(run, 'end_time') and hasattr(run, 'start_time'):
                    if run.end_time and run.start_time:
                        execution_time = (run.end_time - run.start_time).total_seconds()
                        execution_times.append(execution_time)
                
                if hasattr(run, 'error') and run.error:
                    error_count += 1
            
            stats = {
                "status": "success",
                "total_runs": run_count,
                "error_count": error_count,
                "success_rate": (run_count - error_count) / run_count if run_count > 0 else 0,
                "avg_execution_time": sum(execution_times) / len(execution_times) if execution_times else 0,
                "project_name": self.langsmith_config.projectName
            }
            
            logger.info("LangSmith statistics retrieved", stats)
            return stats
            
        except Exception as error:
            logger.error("Failed to get LangSmith statistics", {"error": str(error)})
            return {
                "status": "error",
                "error": str(error)
            }
    
    async def create_feedback(
        self,
        run_id: str,
        score: float,
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create feedback for a specific run.
        
        Args:
            run_id: ID of the run to provide feedback for
            score: Score value (typically 0-1)
            comment: Optional comment
            
        Returns:
            Feedback result
        """
        if not self.client:
            return {
                "status": "disabled",
                "message": "LangSmith client is not initialized"
            }
        
        try:
            feedback = self.client.create_feedback(
                run_id=run_id,
                score=score,
                comment=comment
            )
            
            logger.info("Feedback created for run", {
                "run_id": run_id,
                "score": score
            })
            
            return {
                "status": "success",
                "feedback_id": feedback.id,
                "run_id": run_id,
                "score": score
            }
            
        except Exception as error:
            logger.error("Failed to create feedback", {"error": str(error)})
            return {
                "status": "error",
                "error": str(error)
            }


def create_langsmith_integration(config_path: Optional[str] = None) -> LangSmithIntegration:
    """
    Factory function to create LangSmith integration.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        LangSmithIntegration instance
    """
    if config_path:
        import json
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        from ..utils.config import Config
        config = Config.from_json(config_path)
    else:
        config = load_config()
    
    return LangSmithIntegration(config)


async def main():
    """
    Main entry point for LangSmith integration testing.
    """
    import sys
    
    integration = create_langsmith_integration()
    
    # Test RAG query tracing
    result = await integration.trace_rag_query(
        question="What is the purpose of this system?",
        context=["The system processes data for RAG applications."],
        answer="This is a data pipeline system for RAG.",
        metadata={"test": True}
    )
    
    print("LangSmith Integration Test:")
    print(f"Traced query: {result['question']}")
    
    # Get statistics
    stats = await integration.get_run_statistics()
    print(f"Statistics: {stats}")
    
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
