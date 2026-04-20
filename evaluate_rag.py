"""
RAG Evaluation Script
Run RAGAS evaluation and LangSmith tracing for RAG systems
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src_python.evaluation.ragas_evaluator import create_ragas_evaluator
from src_python.evaluation.langsmith_integration import create_langsmith_integration
from src_python.utils.logger import get_logger


logger = get_logger("evaluate-rag")


async def run_ragas_evaluation(
    config_path: Optional[str] = None,
    sample_size: int = 10
):
    """
    Run RAGAS evaluation.
    
    Args:
        config_path: Optional path to configuration file
        sample_size: Number of sample questions for evaluation
    """
    try:
        logger.info("Starting RAGAS evaluation")
        
        evaluator = create_ragas_evaluator(config_path)
        result = await evaluator.run_benchmark_evaluation()
        
        if result['status'] == 'completed':
            print("\n" + "="*60)
            print("🎯 RAGAS Evaluation Results")
            print("="*60)
            
            print(f"\n📊 Performance Metrics:")
            for metric_name, value in result['metrics'].items():
                print(f"  • {metric_name}: {value:.4f}")
            
            print(f"\n📁 Report saved to: {result['report_path']}")
            print(f"🕐 Timestamp: {result['timestamp']}")
            print("\n" + "="*60)
            
            return True
        else:
            print(f"❌ Evaluation failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as error:
        logger.error("RAGAS evaluation failed", {"error": str(error)})
        print(f"❌ Error: {str(error)}")
        return False


async def run_langsmith_test(
    config_path: Optional[str] = None
):
    """
    Run LangSmith integration test.
    
    Args:
        config_path: Optional path to configuration file
    """
    try:
        logger.info("Testing LangSmith integration")
        
        integration = create_langsmith_integration(config_path)
        
        # Test query tracing
        print("\n" + "="*60)
        print("🔗 LangSmith Integration Test")
        print("="*60)
        
        result = await integration.trace_rag_query(
            question="What is Data Scooper?",
            context=["Data Scooper is a RAG pipeline system."],
            answer="Data Scooper converts documents to RAG format.",
            metadata={"test": True, "version": "1.0"}
        )
        
        print(f"\n✅ Traced Query: {result['question']}")
        print(f"📝 Answer: {result['answer']}")
        print(f"📚 Context: {len(result['context'])} passages")
        
        # Get statistics
        stats = await integration.get_run_statistics()
        print(f"\n📊 LangSmith Statistics:")
        print(f"  • Total runs: {stats.get('total_runs', 0)}")
        print(f"  • Success rate: {stats.get('success_rate', 0):.2%}")
        print(f"  • Avg execution time: {stats.get('avg_execution_time', 0):.4f}s")
        
        print("\n" + "="*60)
        
        return True
        
    except Exception as error:
        logger.error("LangSmith test failed", {"error": str(error)})
        print(f"❌ Error: {str(error)}")
        return False


async def run_comprehensive_evaluation(
    config_path: Optional[str] = None,
    ragas_sample_size: int = 10
):
    """
    Run comprehensive evaluation with both RAGAS and LangSmith.
    
    Args:
        config_path: Optional path to configuration file
        ragas_sample_size: Sample size for RAGAS evaluation
    """
    print("\n" + "="*60)
    print("🚀 Data Scooper - Comprehensive RAG Evaluation")
    print("="*60)
    
    results = {
        "ragas": None,
        "langsmith": None
    }
    
    # Run RAGAS evaluation
    if os.getenv("OPENAI_API_KEY"):
        print("\n🔬 Running RAGAS Evaluation...")
        results["ragas"] = await run_ragas_evaluation(config_path, ragas_sample_size)
    else:
        print("⚠️  Skipping RAGAS evaluation (OPENAI_API_KEY not set)")
    
    # Run LangSmith test
    if os.getenv("LANGCHAIN_API_KEY"):
        print("\n🔗 Testing LangSmith Integration...")
        results["langsmith"] = await run_langsmith_test(config_path)
    else:
        print("⚠️  Skipping LangSmith test (LANGCHAIN_API_KEY not set)")
    
    # Summary
    print("\n" + "="*60)
    print("📋 Evaluation Summary")
    print("="*60)
    print(f"RAGAS Evaluation: {'✅ Completed' if results['ragas'] else '❌ Failed'}")
    print(f"LangSmith Test: {'✅ Completed' if results['langsmith'] else '❌ Failed'}")
    
    if all(results.values()):
        print("\n🎉 All evaluations completed successfully!")
        return 0
    else:
        print("\n⚠️  Some evaluations failed. Check logs for details.")
        return 1


def print_usage():
    """Print usage information."""
    print("""
Usage: python evaluate_rag.py [command] [options]

Commands:
  ragas           Run RAGAS evaluation only
  langsmith       Run LangSmith integration test only
  all             Run both evaluations (default)

Options:
  --config PATH   Path to custom configuration file
  --sample-size N Number of sample questions for RAGAS (default: 10)

Examples:
  python evaluate_rag.py ragas
  python evaluate_rag.py langsmith
  python evaluate_rag.py all --sample-size 20
  python evaluate_rag.py ragas --config custom_config.json

Environment Variables Required:
  - OPENAI_API_KEY: For RAGAS evaluation
  - LANGCHAIN_API_KEY: For LangSmith integration
    """)


async def main():
    """
    Main entry point.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run RAG evaluation and testing"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="all",
        choices=["ragas", "langsmith", "all"],
        help="Evaluation command to run"
    )
    parser.add_argument(
        "--config",
        help="Path to custom configuration file"
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=10,
        help="Number of sample questions for RAGAS evaluation"
    )
    
    args = parser.parse_args()
    
    # Check environment variables
    if args.command in ["ragas", "all"] and not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set")
        print("   RAGAS evaluation requires OpenAI API key")
    
    if args.command in ["langsmith", "all"] and not os.getenv("LANGCHAIN_API_KEY"):
        print("⚠️  Warning: LANGCHAIN_API_KEY environment variable not set")
        print("   LangSmith integration requires LangSmith API key")
    
    # Run evaluation
    if args.command == "ragas":
        success = await run_ragas_evaluation(args.config, args.sample_size)
        sys.exit(0 if success else 1)
    
    elif args.command == "langsmith":
        success = await run_langsmith_test(args.config)
        sys.exit(0 if success else 1)
    
    else:  # all
        exit_code = await run_comprehensive_evaluation(args.config, args.sample_size)
        sys.exit(exit_code)


if __name__ == "__main__":
    asyncio.run(main())
