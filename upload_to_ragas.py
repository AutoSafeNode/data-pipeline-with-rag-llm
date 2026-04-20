"""
Upload ASPICE Dataset to RAGAS/HuggingFace
Convert and upload the ASPICE automotive certification dataset to RAGAS-compatible format
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Dict, List, Any


def convert_to_huggingface_format(
    dataset_path: str,
    output_path: str
):
    """Convert dataset to Hugging Face format for RAGAS."""
    print("🔄 Converting dataset to Hugging Face format")
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    # Convert to Hugging Face format
    hf_data = {
        "data": []
    }
    
    for item in dataset:
        hf_item = {
            "question": item["question"],
            "contexts": item["contexts"],
            "answer": item["answer"],
            "ground_truth": item.get("ground_truth", "")
        }
        hf_data["data"].append(hf_item)
    
    # Save as JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(hf_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Hugging Face format saved to {output_path}")
    print(f"📊 Total samples: {len(hf_data['data'])}")
    
    return hf_data


def create_ragas_upload_script(dataset_path: str):
    """Create RAGAS upload script."""
    print("📝 Creating RAGAS upload script")
    
    script_content = f'''#!/usr/bin/env python3
"""
Upload A's Dataset to RAGAS
Upload the generated dataset to RAGAS platform for evaluation
"""

from datasets import Dataset
import json

# Load dataset
with open("{dataset_path}", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create Hugging Face dataset
dataset_dict = {{
    "question": [],
    "contexts": [],
    "answer": [],
    "ground_truth": []
}}

for item in data["data"]:
    dataset_dict["question"].append(item["question"])
    dataset_dict["contexts"].append(item["contexts"])
    dataset_dict["answer"].append(item["answer"])
    dataset_dict["ground_truth"].append(item["ground_truth"])

# Create Dataset object
dataset = Dataset.from_dict(dataset_dict)

# Save to disk
dataset.save_to_disk("./as_ragas_hf_dataset")
print("✅ Dataset saved to ./as_ragas_hf_dataset")

# Optionally push to Hugging Face Hub
# dataset.push_to_hub("your-username/as-rag-dataset")
print("📤 To upload to Hugging Face Hub:")
print("   1. Create account at https://huggingface.co")
print("   2. Run: huggingface-cli login")
print("   3. Uncomment the push_to_hub line above")
print("   4. Replace 'your-username' with your Hugging Face username")
'''
    
    script_path = "upload_as_to_ragas.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"✅ Upload script created: {script_path}")
    print("   Run: python3 upload_as_to_ragas.py")
    
    return script_path


def main():
    """Main function to prepare dataset for RAGAS upload."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Upload A's dataset to RAGAS")
    parser.add_argument("--dataset", required=True,
                       help="Path to A's dataset JSON file")
    parser.add_argument("--output-dir", default="data/ragas_upload",
                       help="Output directory for RAGAS files")
    
    args = parser.parse_args()
    
    print("🚀 Preparing A's Dataset for RAGAS Upload")
    print("=" * 60)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Convert to Hugging Face format
    hf_output = f"{args.output_dir}/as_dataset_hf.json"
    convert_to_huggingface_format(args.dataset, hf_output)
    
    # Create upload script
    upload_script = create_ragas_upload_script(hf_output)
    
    print("\n" + "=" * 60)
    print("🎯 RAGAS Upload Preparation Complete!")
    print("=" * 60)
    
    print(f"\n📁 Generated Files:")
    print(f"   1. {hf_output} - Hugging Face format dataset")
    print(f"   2. {upload_script} - Upload script")
    
    print(f"\n📋 Next Steps:")
    print(f"   1. Install required packages:")
    print(f"      pip install datasets huggingface_hub")
    print(f"   2. Run the upload script:")
    print(f"      python3 {upload_script}")
    print(f"   3. Test with RAGAS:")
    print(f"      python3 test_ragas_with_as_dataset.py --samples 10")


if __name__ == "__main__":
    main()
