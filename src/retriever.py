# src/scraper_safe.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException, TimeoutException, StaleElementReferenceException
import time

def collect_first_articles(driver, max_articles=5):
    collected_texts = []

    for i in range(max_articles):
        try:
            # Re-fetch the list each loop to avoid stale elements
            articles = driver.find_elements(By.CSS_SELECTOR, "h3.contentRow-title a")
            if i >= len(articles):
                break
            target = articles[i]

            title = target.text

            # Open article in same tab
            try:
                target.click()
            except (StaleElementReferenceException, NoSuchWindowException):
                print(f"Skipping article {i+1}, could not click.")
                continue

            time.sleep(2)  # wait for page to load

            # Extract article content
            try:
                content = driver.find_element(By.CSS_SELECTOR, ".message-body").text
            except:
                content = driver.page_source  # fallback
            collected_texts.append(content)

            # Go back to search results
            try:
                driver.back()
                time.sleep(2)
            except NoSuchWindowException:
                print("Browser window closed unexpectedly.")
                break

        except Exception as e:
            print(f"Error with article {i+1}: {e}")

    return collected_texts

def scrape_first_conversations(query):
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.agricultureinformation.com/forums/forums/-/list")
        time.sleep(5)  # Wait for page to load

        # Click search
        try:
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.p-navgroup-link--search"))
            )
            search_button.click()
        except TimeoutException:
            print("Search button not found.")
            return []

        # Enter query
        try:
            search_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='keywords']"))
            )
            search_input.send_keys(query)
            search_input.send_keys(Keys.RETURN)
            time.sleep(2)
        except TimeoutException:
            print("Search input not found.")
            return []

        results = collect_first_articles(driver)
    except NoSuchWindowException:
        print("Browser closed unexpectedly during scraping.")
        results = []
    finally:
        try:
            driver.quit()
        except Exception:
            pass

    return results
