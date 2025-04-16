import requests
import json

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service



# HOME_URL = "https://www.sunstar.com.ph/superbalita-cebu"
HOME_URL = "https://www.sunstar.com.ph/superbalita-davao"

def get_page_source(url):
    retry_limit = 5
    chrome_options = Options()
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-features=CookiesWithoutSameSiteMustBeSecure")

        # Use Service to manage ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    time.sleep(10)
    driver.get(url)
    iter = 0
    limit = 2
    while iter < limit:
        print(f"Iteration: {iter} ")
        try:
            time.sleep(3)
            driver.execute_script("window.scrollBy(0, 1000);")            
            read_more_btn = driver.find_element("css selector", ".arr--button.load-more-m_button__1mmf1.load-more-m_dark__3dfzb.load-more-m_default__2_k4V")
            read_more_btn.click()
            iter += 1
            retry_limit = 5
        except Exception as e:
            print("See more button not found. Retrying")
            driver.execute_script("window.scrollBy(0, 1000);")
        
        # Optionally, include a retry limit to avoid an infinite loop
            retry_limit -= 1
            if retry_limit == 0:
                print("Reached the retry limit. Exiting the loop.")
                break
            
            # Add another sleep to give time for more content to load
            time.sleep(3)

        
    articles = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="story-card-content"]')
    articles_info = []
    for idx, article in enumerate(articles, start = 1):
        try:
            url = article.find_element(By.CSS_SELECTOR, '[data-test-id="headline"] a').get_attribute("href")
            title = article.find_element(By.CSS_SELECTOR, '[data-test-id="headline"] h6').text
            author = article.find_element(By.CSS_SELECTOR, '[data-test-id="author-name"]').text
            date = article.find_element(By.CSS_SELECTOR, '[data-test-id="publish-time"] time').text

            # Append the article info to the list
            articles_info.append({
                "id": idx,
                "url": url,
                "title": title,
                "author": author,
                "date": date
            })
            print(f"Added {idx}. {title}")
        except Exception as e:
            print(f"Error extracting data from an article: {e}")

    return articles_info


# Main:

articles = get_page_source(HOME_URL)

timestamp = time.strftime("%Y%m%d-%H%M%S")
file_path = f"superbalita-davao-article-links-{timestamp}.csv"

with open(file_path, "w") as file:
    json.dump(articles, file, ensure_ascii=False, indent=4)
    print(f"{file_path} generated")


