from utils import *
import re
def clean_text(text):
    text = text.replace('\xad', '')
    text = text.replace('\u00ad', '')
    text = text.replace('\N{SOFT HYPHEN}', '')
    # Replace non-breaking spaces with regular spaces
    text = text.replace('\xa0','')
    text = re.sub(r'(?<=[^\s\d])\.(?=[^\s\d])', '. ', text) 
    text = re.sub(r'(?<=[\d])\.(?=[\w])', '. ', text) 
    return text


articles = read_file(get_path(["data", "pseudonymized_articles-20241116-115334.json"]))

cleaned_articles = []

for article in articles:
    print("\n", article["body"])
    article["body"] = clean_text(article["body"])
    article["pseudonymized_body"] = clean_text(article["pseudonymized_body"])
    article["pseudonymized_title"] = clean_text(article["pseudonymized_title"])
    article["title"] = clean_text(article["title"])
    cleaned_articles.append(article)

write_file(get_path(["prompter", "cleaned-pseudonymized_articles-20241116-115334.json"]), cleaned_articles)