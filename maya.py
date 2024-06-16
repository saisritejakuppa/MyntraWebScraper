import os
import json
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Function to download image or video given a URL using wget
def download_media(url, directory, index, video = False):
    if video:
        filename = f"{index}.mp4"  # Naming convention: {index}.mp4 for videos
    else:
        filename = f"{index}.jpg"  # Naming convention: {index}.jpg for images

    filepath = os.path.join(directory, filename)

    # Use wget command to download the media (image or video)
    try:
        if video:
            cmd = f'wget {url}-1500k -O {filepath}'
            print('-------------------')
            print(cmd)
            os.system(cmd)
        else:
            subprocess.run(['wget', '-q', '-O', filepath, url], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {url}: {e}")
        return None

    return filename

# Function to scrape product details and media (images/videos) using Selenium
def scrape_product_details(product_id):
    # Set up Selenium Chrome driver
    options = Options()
    options.add_argument("--headless")  # Uncomment this line to run headless
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the product page
    url = f"https://www.manyavar.com/en-in/kurta-pajama/{product_id}.html"
    driver.get(url)
    time.sleep(3)  # Allow time for the page to load

    # Extract product details
    product_details = {}

    # Get product description
    description_element = driver.find_element("css selector", '#collapsible-details-null')
    product_details['description'] = description_element.text.strip()

    # Get product features
    features = {}
    feature_elements = driver.find_elements("css selector", '.accordion__body .attribute-values')
    print(f"Found {len(feature_elements)} feature elements.")  # Debug statement
    for element in feature_elements:

        text = element.text.split(": ")
        print(element.text)
        if len(text) == 2:
            key = text[0].strip()
            value = text[1].strip()
            features[key] = value
            print(f"Feature - {key}: {value}")  # Debug statement
        else:
            print(f"Unexpected feature format: {element.text}")  # Debug statement
    product_details['features'] = features

    # Get image and video URLs
    media_elements = driver.find_elements("css selector", 'div.gallery-inner div[data-pos-id] img, div.gallery-inner video')
    media_urls = []
    vid_urls = []
    for element in media_elements:
        if element.tag_name == 'img':
            media_urls.append(element.get_attribute('src'))
        elif element.tag_name == 'video':
            poster_url = element.get_attribute('poster')
            vid_urls.append(poster_url)

    # Download media (images and videos)
    media_directory = f"data/{product_id}/{product_id}_images"
    os.makedirs(media_directory, exist_ok=True)
    downloaded_media = []

    for index, media_url in enumerate(media_urls, start=1):
        media_filename = download_media(media_url, media_directory, index)
        downloaded_media.append(media_filename)

    # Store media filenames in product_details
    product_details['media_urls'] = downloaded_media

    # Close the Selenium driver
    driver.quit()

    # Write product details to a JSON file
    output_filename = f"data/{product_id}/{product_id}_details.json"
    with open(output_filename, 'w') as json_file:
        json.dump(product_details, json_file, indent=4)

    print(f"Scraping and downloading for {product_id} completed.")

# Example usage:
if __name__ == "__main__":
    for i in range(113704,113704 + 100, 1):
        product_id = f"UC{i}"
        scrape_product_details(product_id)
        break
