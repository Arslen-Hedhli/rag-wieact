# src/scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def collect_first_articles(driver, max_articles=5):
    collected_texts = []
    
    # Get the initial list of article elements
    articles = driver.find_elements(By.CSS_SELECTOR, "h3.contentRow-title a")
    articles = articles[:min(len(articles), max_articles)]
    
    for i in range(len(articles)):
        try:
            # Re-fetch the list each loop (elements get stale after navigation)
            articles = driver.find_elements(By.CSS_SELECTOR, "h3.contentRow-title a")
            target = articles[i]
            
            title = target.text
            
            # Click the article title
            target.click()
            time.sleep(2)  # wait for page to load
            
            # Extract article content
            try:
                content = driver.find_element(By.CSS_SELECTOR, ".message-body").text
            except:
                content = driver.page_source  # fallback if selector not found
            
            collected_texts.append(content)
            
            # Go back to search results
            driver.back()
            time.sleep(2)
        
        except Exception as e:
            print(f"Error with article {i+1}: {e}")
    
    return collected_texts

def scrape_first_conversations(query):
    driver = webdriver.Chrome()
    driver.get("https://www.agricultureinformation.com/forums/forums/-/list")
    time.sleep(5)  # Wait for the page to load

    # 1. Click the search icon to open the dropdown
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.p-navgroup-link--search"))
    )
    search_button.click()

    # 2. Wait for input field to appear and type text
    search_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='keywords']"))
    )
    search_input.send_keys(query)

    # 3. Press Enter or click the search button
    search_input.send_keys(Keys.RETURN)
    time.sleep(2) 


    results = collect_first_articles(driver)
    driver.quit()
    return results
