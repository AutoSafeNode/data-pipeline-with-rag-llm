"""
Test ASPICE Dataset with RAGAS
Upload and evaluate the generated ASPICE automotive certification dataset using RAGAS framework
"""

import asyncio
import os
import json
from pathlib import Path
from typing import Dict, List, Any

from src_python.evaluation.ragas_evaluator import create_ragas_evaluator
from src_python.utils.logger import get_logger


logger = get_logger("ragas-aspice-test")


async def load_dataset(dataset_path: str) -> List[Dict[str, Any]]:
    """Load generated dataset from file."""
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    logger.info(f"Loaded {len(dataset)} samples from {dataset_path}")
    return dataset


async def prepare_for_ragas(dataset: List[Dict[str, Any]]) -> Dict[str, List]:
    """Prepare dataset for RAGAS evaluation."""
    questions = []
    answers = []
    contexts = []
    ground_truths = []
    
    for item in dataset:
        questions.append(item["question"])
        answers.append(item["answer"])
        contexts.append(item["contexts"])
        if "ground_truth" in item:
            ground_truths.append(item["ground_truth"])
    
    return {
        "questions": questions,
        "answers": answers,
        "contexts": contexts,
        "ground_truths": ground_truths if ground_truths else None
    }


async def evaluate_with_ragas(
    dataset_path: str,
    sample_size: int = 20
):
    """Evaluate A's dataset using RAGAS."""
    
    print("🏟️  Testing A's Dataset with RAGAS")
    print("=" * 60)
    
    # Load dataset
    print(f"📁 Loading dataset from {dataset_path}")
    dataset = await load_dataset(dataset_path)
    
    # Sample if needed
    if sample_size and len(dataset) > sample_size:
        print(f"📊 Sampling {sample_size} items from {len(dataset)} total samples")
        import random
        dataset = random.sample(dataset, sample_size)
    
    # Prepare for RAGAS
    print("🔧 Preparing data for RAGAS evaluation")
    ragas_data = await prepare_for_ragas(dataset)
    
    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set")
        print("   Please set your OpenAI API key in .env file")
        print("   RAGAS evaluation requires OpenAI API for metric calculation")
        return False
    
    # Initialize RAGAS evaluator
    print("🤖 Initializing RAGAS evaluator")
    try:
        evaluator = create_ragas_evaluator()
    except Exception as error:
        print(f"❌ Failed to initialize RAGAS evaluator: {error}")
        print("   Make sure OPENAI_API_KEY is properly set in .env file")
        return False
    
    # Run evaluation
    print(f"🎯 Evaluating {len(ragas_data['questions'])} samples")
    print("   This may take a few minutes...")
    
    try:
        result = await evaluator.evaluate_rag_system(
            questions=ragas_data["questions"],
            answers=ragas_data["answers"],
            contexts=ragas_data["contexts"],
            ground_truths=ragas_data["ground_truths"]
        )
        
        print("\n" + "=" * 60)
        print("🎯 RAGAS Evaluation Results")
        print("=" * 60)
        
        print(f"\n📊 Performance Metrics:")
        for metric_name, value in result.metrics.items():
            print(f"   • {metric_name}: {value:.4f}")
        
        # Calculate overall score
        if result.metrics:
            avg_score = sum(result.metrics.values()) / len(result.metrics)
            print(f"\n   🎯 Overall Average: {avg_score:.4f}")
        
        # Save results
        timestamp = result.timestamp.replace(":", "-")
        output_dir = "./data/evaluation_results"
        os.makedirs(output_dir, exist_ok=True)
        
        report_path = f"{output_dir}/as_ragas_evaluation_{timestamp}.csv"
        evaluator.save_evaluation_report(result, report_path)
        
        print(f"\n📁 Detailed report saved to: {report_path}")
        print(f"🕐 Evaluation completed at: {result.timestamp}")
        
        return True
        
    except Exception as error:
        print(f"❌ RAGAS evaluation failed: {error}")
        import traceback
        traceback.print_exc()
        return False


def show_dataset_preview(dataset_path: str, num_samples: int = 5):
    """Show preview of dataset content."""
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    print(f"\n📋 Dataset Preview ({num_samples} samples):")
    print("=" * 60)
    
    for i, item in enumerate(dataset[:num_samples]):
        print(f"\n{i+1}. Question: {item['question']}")
        print(f"   Category: {item['metadata']['category']}")
        print(f"   Answer: {item['answer'][:100]}...")
        print(f"   Ground Truth: {item['ground_truth']}")


def analyze_dataset_quality(dataset_path: str):
    """Analyze quality of generated dataset."""
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    print("\n📊 Dataset Quality Analysis:")
    print("=" * 60)
    
    # Category distribution
    categories = {}
    for item in dataset:
        cat = item['metadata']['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n📁 Category Distribution:")
    for cat, count in sorted(categories.items()):
        print(f"   • {cat}: {count} questions ({count/len(dataset)*100:.1f}%)")
    
    # Answer length distribution
    answer_lengths = [len(item['answer']) for item in dataset]
    print(f"\n📝 Answer Length Statistics:")
    print(f"   • Average: {sum(answer_lengths)/len(answer_lengths):.0f} characters")
    print(f"   • Min: {min(answer_lengths)} characters")
    print(f"   • Max: {max(answer_lengths)} characters")
    
    # Context count
    context_counts = [len(item['contexts']) for item in dataset]
    print(f"\n📚 Context Count Statistics:")
    print(f"   • Average: {sum(context_counts)/len(context_counts):.1f} contexts")
    print(f"   • Min: {min(context_counts)} contexts")
    print(f"   • Max: {max(context_counts)} contexts")


async def main():
    """Main function to test A's dataset with RAGAS."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test A's dataset with RAGAS")
    parser.add_argument("--dataset", default="data/evaluation_datasets", 
                       help="Directory containing dataset files")
    parser.add_argument("--samples", type=int, default=20,
                       help="Number of samples to evaluate (default: 20)")
    parser.add_argument("--preview", action="store_true",
                       help="Show dataset preview without evaluation")
    parser.add_argument("--analyze", action="store_true",
                       help="Analyze dataset quality without evaluation")
    
    args = parser.parse_args()
    
    # Find latest dataset file
    dataset_dir = Path(args.dataset)
    json_files = list(dataset_dir.glob("as_evaluation_dataset_*.json"))
    
    if not json_files:
        print(f"❌ No dataset files found in {args.dataset}")
        print("   Run generate_as_dataset.py first to create dataset")
        return
    
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    print(f"📁 Using dataset: {latest_file.name}")
    
    # Show preview if requested
    if args.preview:
        show_dataset_preview(str(latest_file))
        return
    
    # Analyze if requested
    if args.analyze:
        analyze_dataset_quality(str(latest_file))
        return
    
    # Run RAGAS evaluation
    success = await evaluate_with_ragas(str(latest_file), args.samples)
    
    if success:
        print("\n🎉 RAGAS evaluation completed successfully!")
        print("   Check the results and improve your RAG system based on metrics")
    else:
        print("\n⚠️  Evaluation failed. Please check the error messages above")
        print("   Make sure to set OPENAI_API_KEY in .env file")


if __name__ == "__main__":
    asyncio.run(main())
