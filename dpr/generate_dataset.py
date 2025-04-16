import random
from datasets import load_dataset, DatasetDict
from collections import defaultdict
import json
from utils import *

# Load your Hugging Face datasets (replace with actual dataset names or file paths)
articles_dataset = load_dataset("jhoannarica/superbalita_split")
qa_dataset = load_dataset("jhoannarica/cebquad_split")

def build_dpr_dataset(articles, qa, split):

    # Create lookup from article_id to article_body
    article_lookup = {row["id"]: row["pseudonymized_body"] for row in articles[split]}
    article_title = {row["id"]: row["pseudonymized_title"] for row in articles[split]}

    # Group questions by article_id
    qa_by_article = defaultdict(list)
    for row in qa[split]:
        qa_by_article[row["article_id"]].append({
            "question": row["question"],
            "answer": row["answer"]
        })

    # Prepare DPR-formatted data
    dpr_data = []

    all_article_ids = list(article_lookup.keys())

    for article_id, article_body in article_lookup.items():
        if article_id not in qa_by_article:
            continue  # skip if no questions for this article

        # Randomly pick one question-answer pair for the article
        qa_pair = random.choice(qa_by_article[article_id])

        # Select 5 negative contexts from other articles
        negative_ids = random.sample(
            [aid for aid in all_article_ids if aid != article_id],
            k=min(5, len(all_article_ids) - 1)
        )
        negative_ctxs = [
            {
                "article_id": neg_id,
                "title": article_title[neg_id],
                "text": article_lookup[neg_id]
            }
            for neg_id in negative_ids
        ]

        dpr_entry = {
            "question": qa_pair["question"],
            "answers": [qa_pair["answer"]],
            "positive_ctxs": [{
                "article_id": article_id,
                "title": article_title[article_id],
                "text": article_body
            }],
            "negative_ctxs": negative_ctxs
        }

        dpr_data.append(dpr_entry)

    return dpr_data

# Run for all splits and save as JSON
for split in ["train", "validation", "test"]:
# for split in ["train"]:
    dpr_dataset = build_dpr_dataset(articles_dataset, qa_dataset, split)
    write_file(get_path(["dpr", f"dpr_{split}.csv"]), dpr_dataset)
    # with open(f"dpr_{split}.json", "w", encoding="utf-8") as f:
    #     json.dump(dpr_dataset, f, ensure_ascii=False, indent=2)

print("DPR datasets created for train, validation, and test.")