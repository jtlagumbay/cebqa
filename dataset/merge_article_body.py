# merges dataset/articles_202503120405_author_removed.csv with train, test, val.csv
import pandas as pd
from utils import *
import ast  # For safely evaluating strings as dictionaries

def extract_text(context_str):
    try:
        context_dict = ast.literal_eval(context_str)  # Safely convert string to dict
        return context_dict.get('text', '')  # Return 'text' value or empty string if not found
    except (ValueError, SyntaxError):
        return ''

articles = pd.read_csv(get_path(["dataset","articles_202503120405_author_removed_fixed.csv"]))
train = pd.read_csv(get_path(["dataset","train.csv"]))
val = pd.read_csv(get_path(["dataset","val.csv"]))
test = pd.read_csv(get_path(["dataset","test.csv"]))

articles_body_dict = dict(zip(articles['id'], articles['pseudonymized_body']))

train_new = train.copy()
train_new['article_body'] = train['article_id'].map(articles_body_dict).fillna('')
train_new['context'] = train["context"].apply(extract_text)
train_new['answer'] = train["answer"].apply(extract_text)

val_new = val.copy()
val_new['article_body'] = val['article_id'].map(articles_body_dict).fillna('')
val_new['context'] = val["context"].apply(extract_text)
val_new['answer'] = val["answer"].apply(extract_text)

test_new = test.copy()
test_new['article_body'] = test['article_id'].map(articles_body_dict).fillna('')
test_new['context'] = test["context"].apply(extract_text)
test_new['answer'] = test["answer"].apply(extract_text)

train_new.to_csv(get_path(["dataset", "train_removed-tag.csv"]), index=False)
val_new.to_csv(get_path(["dataset", "val_removed-tag.csv"]), index=False)
test_new.to_csv(get_path(["dataset", "test_removed-tag.csv"]), index=False)
