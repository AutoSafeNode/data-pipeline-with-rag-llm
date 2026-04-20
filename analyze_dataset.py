"""
Analyze A's Dataset Quality
Simple analysis without pandas dependency
"""

import json
import sys
from pathlib import Path


def analyze_dataset(dataset_path: str):
    """Analyze dataset quality without pandas."""
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    print("📊 A's Dataset Quality Analysis")
    print("=" * 60)
    
    # Basic statistics
    print(f"\n📈 Basic Statistics:")
    print(f"   Total samples: {len(dataset)}")
    
    # Category distribution
    categories = {}
    for item in dataset:
        cat = item['metadata']['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n📁 Category Distribution:")
    for cat, count in sorted(categories.items()):
        print(f"   • {cat}: {count} questions ({count/len(dataset)*100:.1f}%)")
    
    # Answer length statistics
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
    
    # Question length statistics
    question_lengths = [len(item['question']) for item in dataset]
    print(f"\n❓ Question Length Statistics:")
    print(f"   • Average: {sum(question_lengths)/len(question_lengths):.0f} characters")
    print(f"   • Min: {min(question_lengths)} characters")
    print(f"   • Max: {max(question_lengths)} characters")
    
    # Sample questions
    print(f"\n🔍 Sample Questions (first 3):")
    for i, item in enumerate(dataset[:3]):
        print(f"   {i+1}. {item['question']}")
        print(f"      Category: {item['metadata']['category']}")
        print(f"      Answer: {item['answer'][:80]}...")
        print(f"      Ground Truth: {item['ground_truth']}")
        print()
    
    print("✅ Dataset analysis completed!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        dataset_path = sys.argv[1]
    else:
        # Find latest dataset
        dataset_dir = Path("data/evaluation_datasets")
        json_files = list(dataset_dir.glob("as_evaluation_dataset_*.json"))
        if json_files:
            dataset_path = str(max(json_files, key=lambda x: x.stat().st_mtime))
        else:
            print("❌ No dataset files found")
            sys.exit(1)
    
    print(f"📁 Analyzing: {dataset_path}")
    analyze_dataset(dataset_path)
