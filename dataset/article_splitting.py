from datasets import load_dataset, DatasetDict
from utils import *
import pandas as pd 
from sklearn.model_selection import train_test_split

ARTICLES_CSV = get_path(["dataset","articles_202503120405_author_removed_fixed.csv"])

df = pd.read_csv(ARTICLES_CSV)
df = df.drop(columns=["title", "body", "updated_on", "updated_by", "assigned_to"]) 
print(df.head())


# Split into 70% training, 20% testing, 10% validation
train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42)  # 30% split for test and validation
val_df, test_df = train_test_split(temp_df, test_size=0.6667, random_state=42)  # 20% for test and 10% for validation


train_df.sort_values(by="id").to_csv("article_train.csv", index=False)
val_df.sort_values(by="id").to_csv("article_val.csv", index=False)
test_df.sort_values(by="id").to_csv("article_test.csv", index=False)

# Check the sizes of the splits
print(f"Train: {len(train_df)} | Test: {len(test_df)} | Validation: {len(val_df)}")




