from datasets import load_dataset, DatasetDict
from utils import *

CEBQUAD_CSV = get_path(["dataset","validated_202502041950.csv"])

def transform_row(row):
    return {
        "id": row["id"],
        "article_id": row["article_id"],
        "article_title": row["article_title"],
        "article_body": row["article_body"],
        "question": row["question"],
        "context": {
            "text": row["context"],
            "start": row["context_start"],
            "end": row["context_end"]
        },
        "answer": {
            "text": row["answer"],
            "start": row["answer_start"],
            "end": row["answer_end"]
        }
    }

# Load CSV file (assuming it's in the same directory)
dataset = load_dataset("csv", data_files=CEBQUAD_CSV)

# Split the dataset into train (70%) and temp (30%)
train_testvalid = dataset["train"].train_test_split(test_size=0.3, seed=42)

# Split temp (30%) into test (20%) and dev (10%)
test_valid = train_testvalid["test"].train_test_split(test_size=1/3, seed=42)

# Combine splits into DatasetDict
final_splits = {
    "train": train_testvalid["train"].map(transform_row),
    "test": test_valid["train"].map(transform_row),  # 20%
    "dev": test_valid["test"].map(transform_row)     # 10%
}

# Convert to DatasetDict
dataset = DatasetDict(final_splits)

# Print dataset sizes
print(dataset)
dataset.save_to_disk(get_path(["dataset", "cebquad"]))

