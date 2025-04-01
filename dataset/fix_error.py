import pandas as pd
from utils import *

# Load both CSV files
new_df = pd.read_csv(get_path(["dataset", "articles_202503120405_author_removed.csv"]))
original_df = pd.read_csv(get_path(["dataset", "articles_202503120405.csv"]))

# Create a dictionary from the original CSV for quick lookup
# original_body_dict = original_df.set_index('id')['body'].to_dict()
# original_pseudo_body_dict = original_df.set_index('id')['pseudonymized_body'].to_dict()


# # Replace 'article_id' with your actual ID column name if different

# # Fill blank article_body in new_df
# new_df['body'] = new_df.apply(
#     lambda row: original_body_dict.get(row['id'], row['body']) 
#     if pd.isna(row['body']) or row['body'] == '' 
#     else row['body'],
#     axis=1
# )
# new_df['pseudonymized_body'] = new_df.apply(
#     lambda row: original_pseudo_body_dict.get(row['id'], row['pseudonymized_body']) 
#     if pd.isna(row['pseudonymized_body']) or row['pseudonymized_body'] == '' 
#     else row['pseudonymized_body'],
#     axis=1
# )

# # Save the updated new CSV

for index, row in new_df.iterrows():
    print(row["body"])
    if pd.isna(row['body']) or row['body'] == '':
        original_body = original_df.iloc[index]['body']
        new_df.at[index, 'body'] = original_body

    if pd.isna(row['pseudonymized_body']) or row['pseudonymized_body'] == '':
        original_pseudonymized_body = original_df.iloc[index]['pseudonymized_body']
        new_df.at[index, 'pseudonymized_body'] = original_pseudonymized_body

new_df.to_csv('"articles_202503120405_author_removed_fixed.csv', index=False)