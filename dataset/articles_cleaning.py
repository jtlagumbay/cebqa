import pandas as pd
import re
from utils import *

# This removes the author tags at the end of the article. ex: "\ AVG"
# Load the CSV file
df = pd.read_csv(get_path(["dataset","articles_202503120405.csv"]))

# Function to clean the article_body
def clean_text(text):
    match = re.search(r'\. / .*$', text)
    if match:
        # print(match)
        trailing_text = match.group(0)  # Get the text after ". / "
        if len(trailing_text) > 7:  # Check if it reaches a certain length (e.g., 10 characters)
            print(match)
        #     # print("\n"+re.sub(r'\. / .*$', '.', text))
        #     raise Exception("here")
        # else: 
        # print(text)
        # print(re.sub(r'\. / .*$', '.', text))
        return re.sub(r'\. / .*$', '.', text)
     # Retain the period and remove text after '. / '
    return text

# Apply the function to the article_body column
df['body'] = df['body'].astype(str).apply(clean_text)
df['pseudonymized_body'] = df['pseudonymized_body'].astype(str).apply(clean_text)

# Save the cleaned CSV
df.to_csv("articles_202503120405_author_removed_1.csv", index=False)




# Load the CSV file
# df = pd.read_csv(get_path(["dataset","articles_202503120405_author_removed.csv"]))

# # Function to clean the article_body
# def clean_text(text):
#     ex = r"\. \(([A-Z]+)\)$"
#     match = re.search(ex, text)
#     if match:
#         print(match)
#         trailing_text = match.group(0)  # Get the text after ". / "
#         if len(trailing_text) > 7:  # Check if it reaches a certain length (e.g., 10 characters)
#             print(text)
#             raise Exception("here")
#         else: 
#             return re.sub(ex, '.', text)
#      # Retain the period and remove text after '. / '

# # Apply the function to the article_body column
# df['body'] = df['body'].astype(str).apply(clean_text)
# df['pseudonymized_body'] = df['pseudonymized_body'].astype(str).apply(clean_text)

# # Save the cleaned CSV
# # df.to_csv("articles_202503120405_author_removed.csv", index=False)
# # print(df)
# print("Processing complete. Cleaned data saved as cleaned_index.csv.")
