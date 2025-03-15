import os
import requests
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import time

# Base path where all country folders will be stored
BASE_SAVE_FOLDER = r"C:\Users\Admin\Documents\Cultural Analytics\resources\china_daily\missing_leaders"

# Path to the CSV file
CSV_PATH = r"C:\Users\Admin\Documents\Cultural Analytics\resources\missing_leaders.csv"

# Set up Chrome options
options = Options()
# options.add_argument("--headless")  # Uncomment to run in headless mode
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def download_page_images(save_folder):
    """Download images from the current page to the specified folder"""
    try:
        # Ensure the save folder exists
        os.makedirs(save_folder, exist_ok=True)

        # Wait for content to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'lft_art'))
        )
        time.sleep(2)  # Additional buffer for images to load

        # Parse page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        article_section = soup.find('div', class_='lft_art')

        if article_section:
            image_tags = article_section.find_all('img')
            print(f"Found {len(image_tags)} images on current page")

            for img_tag in image_tags:
                img_url = img_tag.get('src')
                if img_url:
                    full_url = urljoin(driver.current_url, img_url)
                    if not full_url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        continue

                    try:
                        img_data = requests.get(full_url, timeout=10).content
                        img_name = os.path.basename(full_url)
                        file_path = os.path.join(save_folder, img_name)

                        if not os.path.exists(file_path):
                            with open(file_path, 'wb') as f:
                                f.write(img_data)
                            print(f"Downloaded: {img_name}")
                        else:
                            print(f"Skipped duplicate: {img_name}")
                    except Exception as e:
                        print(f"Failed to download {full_url}: {e}")
    except Exception as e:
        print(f"Error processing page: {str(e)}")


def click_next_button():
    """Attempt to click the NEXT button"""
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="page rt"]//a[contains(text(), "NEXT")]'))
        )
        driver.execute_script("arguments[0].click();", next_button)
        return True
    except Exception as e:
        print("No more pages available or button not found")
        return False


def process_leader(country_code, leader_name):
    """Process all pages for a specific leader"""
    # Create query-friendly name
    leader_query = '+'.join(leader_name.lower().split())

    # Construct URL with proper encoding
    cond_params = {
        "publishedDateFrom": "2020-01-01",
        "publishedDateTo": "2025-01-01",
        "fullMust": leader_query,
        "sort": "dp",
        "duplication": "on"
    }
    encoded_cond = quote(json.dumps(cond_params))
    url = f"https://newssearch.chinadaily.com.cn/en/search?cond={encoded_cond}&language=en"

    # Create save path
    save_folder = os.path.join(BASE_SAVE_FOLDER, country_code, leader_name)

    print(f"\nProcessing {leader_name} ({country_code})")
    print(f"Search URL: {url}")
    print(f"Save folder: {save_folder}")

    try:
        driver.get(url)
        print("Page loaded - starting image download...")

        while True:
            download_page_images(save_folder)
            if not click_next_button():
                break
            print("Moving to next page...")
            time.sleep(3)  # Respectful delay between pages

    except Exception as e:
        print(f"Error processing {leader_name}: {str(e)}")


# Main execution
try:
    # Read and process CSV
    with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';')
        for row in csvreader:
            country_code = row['Country_Code']
            leaders = [name.strip() for name in row['De_Facto_Leader'].split(',')]

            for leader in leaders:
                if leader:  # Skip empty names
                    process_leader(country_code, leader)

finally:
    print("\nCompleted all downloads. Closing browser in 30 seconds...")
    time.sleep(30)
    driver.quit()