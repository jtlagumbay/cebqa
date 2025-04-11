import pandas as pd
from utils import *

ARTICLES_TRAIN = get_path(["dataset","article_train.csv"])
ARTICLES_TEST = get_path(["dataset","article_test.csv"])
ARTICLES_VAL = get_path(["dataset","article_val.csv"])
MERGED = get_path(["dataset","merged.csv"])

# Load the CSV files
merged_df = pd.read_csv(MERGED)
article_train_df = pd.read_csv(ARTICLES_TRAIN)
article_test_df = pd.read_csv(ARTICLES_TEST)
article_val_df = pd.read_csv(ARTICLES_VAL)

# Filter rows based on 'article_id' in 'id' of train.csv and test.csv
merge_train_df = merged_df[merged_df['article_id'].isin(article_train_df['id'])]
merge_test_df = merged_df[merged_df['article_id'].isin(article_test_df['id'])]
merge_val_df = merged_df[merged_df['article_id'].isin(article_val_df['id'])]

# Save the results to new CSV files
merge_train_df.to_csv("cebquad_train_new.csv", index=False)
merge_test_df.to_csv("cebquad_test_new.csv", index=False)
merge_val_df.to_csv("cebquad_val_new.csv", index=False)