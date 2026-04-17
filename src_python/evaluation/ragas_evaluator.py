"""
RAGAS Evaluator Module
Evaluates RAG systems using RAGAS framework
"""

import os
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import pandas as pd

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from ..utils.logger import get_logger
from ..utils.config import load_config


logger = get_logger("ragas-evaluator")


@dataclass
class EvaluationResult:
    """Result of RAG evaluation."""
    dataset_name: str
    metrics: Dict[str, float]
    details: pd.DataFrame
    timestamp: str


class RAGASEvaluator:
    """
    Evaluator for RAG systems using RAGAS framework.
    """
    
    def __init__(self, config: Any):
        """
        Initialize RAGAS evaluator.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.evaluation_config = config.evaluation.ragas
        
        # Initialize OpenAI for RAGAS (RAGAS requires OpenAI for evaluation)
        self.llm = ChatOpenAI(
            model=self.evaluation_config.model,
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0
        )
        
        self.embeddings = OpenAIEmbeddings(
            model=self.evaluation_config.embeddingModel,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize metrics
        self.metrics = self._initialize_metrics()
        
        logger.info("RAGAS evaluator initialized", {
            "model": self.evaluation_config.model,
            "metrics": list(self.evaluation_config.metrics)
        })
    
    def _initialize_metrics(self):
        """
        Initialize RAGAS metrics.
        
        Returns:
            List of initialized metrics
        """
        available_metrics = {
            "faithfulness": faithfulness,
            "answer_relevancy": answer_relevancy,
            "context_precision": context_precision,
            "context_recall": context_recall
        }
        
        selected_metrics = []
        for metric_name in self.evaluation_config.metrics:
            if metric_name in available_metrics:
                metric = available_metrics[metric_name]
                selected_metrics.append(metric)
        
        return selected_metrics
    
    async def evaluate_rag_system(
        self,
        questions: List[str],
        answers: List[str],
        contexts: List[List[str]],
        ground_truths: Optional[List[str]] = None
    ) -> EvaluationResult:
        """
        Evaluate RAG system performance.
        
        Args:
            questions: List of questions
            answers: List of generated answers
            contexts: List of retrieved contexts for each question
            ground_truths: Optional list of ground truth answers
            
        Returns:
            EvaluationResult with metrics and details
        """
        try:
            from datasets import Dataset
            
            logger.info(f"Evaluating RAG system with {len(questions)} questions")
            
            # Create evaluation dataset
            data_dict = {
                "question": questions,
                "answer": answers,
                "contexts": contexts
            }
            
            if ground_truths:
                data_dict["ground_truth"] = ground_truths
            
            dataset = Dataset.from_dict(data_dict)
            
            # Run evaluation
            result = evaluate(
                dataset=dataset,
                metrics=self.metrics,
                llm=self.llm,
                embeddings=self.embeddings
            )
            
            # Convert to DataFrame for easier analysis
            df = result.to_pandas()
            
            # Calculate overall metrics
            metrics_summary = {}
            for metric_name in self.evaluation_config.metrics:
                if metric_name in df.columns:
                    metrics_summary[metric_name] = df[metric_name].mean()
            
            from datetime import datetime
            evaluation_result = EvaluationResult(
                dataset_name="rag_evaluation",
                metrics=metrics_summary,
                details=df,
                timestamp=datetime.now().isoformat()
            )
            
            logger.info("RAG evaluation completed", {
                "metrics": metrics_summary
            })
            
            return evaluation_result
            
        except Exception as error:
            logger.error("RAG evaluation failed", {"error": str(error)})
            raise
    
    async def evaluate_sample_questions(
        self,
        sample_size: int = 10
    ) -> EvaluationResult:
        """
        Evaluate with sample questions for testing.
        
        Args:
            sample_size: Number of sample questions to generate
            
        Returns:
            EvaluationResult
        """
        # Generate sample questions
        sample_questions = [
            "What is the purpose of this document?",
            "Summarize the key findings.",
            "What are the main conclusions?",
            "List the important metrics mentioned.",
            "Explain the methodology used."
        ] * (sample_size // 5 + 1)
        
        sample_questions = sample_questions[:sample_size]
        
        # Generate sample answers and contexts
        sample_answers = [
            "This document provides comprehensive analysis of the data pipeline system."
            for _ in range(sample_size)
        ]
        
        sample_contexts = [
            ["The data pipeline processes Excel and PDF files.",
             "It converts documents to RAG format.",
             "The system uses embedding for semantic search."]
            for _ in range(sample_size)
        ]
        
        return await self.evaluate_rag_system(
            questions=sample_questions,
            answers=sample_answers,
            contexts=sample_contexts
        )
    
    def save_evaluation_report(
        self,
        result: EvaluationResult,
        output_path: str
    ) -> None:
        """
        Save evaluation report to file.
        
        Args:
            result: Evaluation result
            output_path: Path to save report
        """
        try:
            # Save detailed results
            result.details.to_csv(output_path, index=False)
            
            # Save summary
            summary_path = output_path.replace('.csv', '_summary.json')
            import json
            with open(summary_path, 'w') as f:
                json.dump({
                    "dataset_name": result.dataset_name,
                    "metrics": result.metrics,
                    "timestamp": result.timestamp
                }, f, indent=2)
            
            logger.info(f"Evaluation report saved to {output_path}")
            
        except Exception as error:
            logger.error("Failed to save evaluation report", {"error": str(error)})
            raise
    
    async def run_benchmark_evaluation(self) -> Dict[str, Any]:
        """
        Run comprehensive benchmark evaluation.
        
        Returns:
            Benchmark results summary
        """
        logger.info("Starting benchmark evaluation")
        
        try:
            # Run sample evaluation
            result = await self.evaluate_sample_questions(sample_size=10)
            
            # Save results
            output_dir = "./data/evaluation_results"
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = result.timestamp.replace(":", "-")
            output_path = f"{output_dir}/ragas_evaluation_{timestamp}.csv"
            
            self.save_evaluation_report(result, output_path)
            
            return {
                "status": "completed",
                "metrics": result.metrics,
                "report_path": output_path,
                "timestamp": result.timestamp
            }
            
        except Exception as error:
            logger.error("Benchmark evaluation failed", {"error": str(error)})
            return {
                "status": "failed",
                "error": str(error)
            }


def create_ragas_evaluator(config_path: Optional[str] = None) -> RAGASEvaluator:
    """
    Factory function to create RAGAS evaluator.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        RAGASEvaluator instance
    """
    if config_path:
        # Load custom config
        import json
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        # Convert to Config object (simplified)
        from ..utils.config import Config
        config = Config.from_json(config_path)
    else:
        config = load_config()
    
    return RAGASEvaluator(config)


async def main():
    """
    Main entry point for RAGAS evaluation.
    """
    import sys
    
    evaluator = create_ragas_evaluator()
    result = await evaluator.run_benchmark_evaluation()
    
    print("RAGAS Benchmark Evaluation Results:")
    print(f"Status: {result['status']}")
    
    if result['status'] == 'completed':
        print(f"\nMetrics:")
        for metric_name, value in result['metrics'].items():
            print(f"  {metric_name}: {value:.4f}")
        print(f"\nReport saved to: {result['report_path']}")
        sys.exit(0)
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
