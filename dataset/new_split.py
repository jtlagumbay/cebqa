import pandas as pd
from utils import *

csv_files = ["train_removed-tag.csv", "val_removed-tag.csv", "test_removed-tag.csv"]
csv_path = [get_path(["dataset", file]) for file in csv_files]
articles = pd.read_csv(get_path(["dataset","articles_202503120405_author_removed_fixed.csv"]))
articles_body_dict = dict(zip(articles['id'], articles['pseudonymized_body']))

df = pd.concat([pd.read_csv(f) for f in csv_path], ignore_index=True).sort_values(by="id")
df['article_body'] = df['article_id'].map(articles_body_dict).fillna('')

df.to_csv("merged.csv", index=False)

print(df)