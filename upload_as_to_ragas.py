#!/usr/bin/env python3
"""
Upload A's Dataset to RAGAS
Upload the generated dataset to RAGAS platform for evaluation
"""

from datasets import Dataset
import json

# Load dataset
with open("data/ragas_upload/as_dataset_hf.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create Hugging Face dataset
dataset_dict = {
    "question": [],
    "contexts": [],
    "answer": [],
    "ground_truth": []
}

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
