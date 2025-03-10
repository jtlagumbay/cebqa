from utils import *

dataset = get_dataset()

# Shuffle the "dev" split and select the first 300 rows
sampled_dev = dataset["dev"].shuffle(seed=42).select(range(300))
print(sampled_dev)

sampled = []
for data in sampled_dev:
    sampled.append({
        "id": data["id"],
        "article_id": data["article_id"],
        "question": data["question"],
        "context": data["context"]["text"],
        "answer": data["answer"]["text"],
    })

write_file(get_path(["cebquad_analysis", "sampled_300.json"]), sampled)