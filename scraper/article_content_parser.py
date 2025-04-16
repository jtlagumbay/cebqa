
import requests
import json

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils import *

FOLDER_PATH = "./scraper/"

def get_url_content(url):
    response = requests.get(url)
    html_content = response.content.decode("utf-8")
    parser = BeautifulSoup(html_content, "html.parser")

    return parser, html_content


def get_last_script_tag(url):
    parser, html = get_url_content(url)
    # Find the head section
    head = parser.find("head")
    # Find all script tags with type application/json in the head
    script_tags = parser.find_all("script", {"type": "application/ld+json"})
    
    if script_tags:
        # Get the last script tag
        last_script_tag = script_tags[-1]
        json_content = last_script_tag.string
        return json.loads(json_content) if json_content else None
    else:
        return None

def load_urls_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Assuming the JSON file has an array of URLs
        return data
    

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def scrape_articles():
    article_urls = read_file(get_path(["scraper", "superbalita-davao-article-links-20250411-130618.json"]))

    articles = []
    error_articles = []
    
    for article in article_urls:
        url = article['url']
        id = article['id']
        title = article['title']
        print(f"Processing {id}: {title}")

        data = get_last_script_tag(url)
        if data:
            try:
                article_body = data["articleBody"]
                    
                if article_body:
                    article["body"] = article_body
                    articles.append(article)
            except Exception as e:
                print(f"Error Processing {id}: {title}")
                error_articles.append(article)

    
    return articles, error_articles

timestamp = time.strftime("%Y%m%d-%H%M%S")
file_path = FOLDER_PATH + f"superbalita-davao-articles-{timestamp}.csv"
file_path_error = FOLDER_PATH + f"superbalita-davao-articles-error-{timestamp}.csv"

[articles, error_articles] = scrape_articles()
save_to_json(articles, file_path)
save_to_json(error_articles, file_path_error)
