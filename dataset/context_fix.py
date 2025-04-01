from utils import *
import pandas as pd

val = pd.read_csv(get_path(["dataset", "val_removed-tag-fixed.csv"]))

# Add a new column for the context index
val['context_start_new'] = -1 
val['context_end_new'] = -1 
val['answer_start_new'] = -1 
val['answer_end_new'] = -1 

def find_text(article_body, text):
    # Create a regex pattern that handles variations in whitespace and quotes
    pattern = re.escape(text)
    pattern = pattern.replace('\\"', '["“”]')  # Handle both straight and curly quotes
    match = re.search(pattern, article_body)
    
    if match:
        return match.start()
    return -1

for idx, row in val.iterrows():
    context = str(row['context'])
    answer = str(row['answer'])
    article_body = str(row['article_body'])
    # print(row["id"])
    
    # Find the index of context in article_body
    context_index = article_body.find(context)
    
    if context_index == -1:
        print(f"Context\n{row['id']}")
    else:   
        val.at[idx, 'context_start'] = context_index
        val.at[idx, 'context_end'] = context_index + len(context)
        

    # Find the index of context in article_body
    answer_index = context.find(answer)
    
    if answer_index == -1:
        print(f"Answer\n{row['id']}")
    else:
        val.at[idx, 'answer_start'] = answer_index
        val.at[idx, 'answer_end'] = answer_index + len(answer)
    
    # if idx == 2500:
    #     break


# Save the modified DataFrame
# print(val)
val.to_csv(get_path(["dataset", "val_removed-tag-fixed.csv"]), index=False)

# 00228-013