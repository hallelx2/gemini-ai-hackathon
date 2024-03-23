import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def download_image(url, filepath):
  try:
    response = requests.get(url, stream=True)
    if response.status_code == 200:
      with open(filepath, 'wb') as f:
        for chunk in response.iter_content(1024):
          f.write(chunk)
      print(f"Downloaded image: {filepath}")
    else:
      print(f"Failed to download image: {url}")
  except Exception as e:
    print(f"Error downloading image: {e}")


def scrape_website(url, download_dir="images"):
  """Scrapes a website using Selenium with WebDriverManager, handles dynamic content,
  downloads images, and extracts body text.

  Args:
      url: The URL of the website to scrape.
      download_dir: The directory to save downloaded images (optional).

  Returns:
      A dictionary containing the scraped data:
          text: The extracted body text from the website.
          images: A list of downloaded image file paths.
  """
  try:
    # Set up driver using WebDriverManager
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = chrome_options)  # Open a Chrome browser instance using ChromeDriverManager

    driver.get(url)

    # Wait for page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "title")))


    # Extract title
    title = driver.title

    # Extract body text
    body_text = driver.find_element(By.TAG_NAME, "body").text

     # Create download directory if it doesn't exist
    if not os.path.exists(download_dir):
      os.makedirs(download_dir)

    # Extract and download images within body
    images = []
    for img in driver.find_elements(By.XPATH, ".//body//img"):  # XPath targeting body elements
      image_url = img.get_attribute("src")
      if image_url:
        filename = os.path.basename(image_url)  # Extract filename from URL
        filepath = os.path.join(download_dir, filename)
        # Download image using requests
        download_image(image_url, filepath)
        images.append(filepath)

    # Close the browser
    driver.quit()

    return {"text": body_text, 'images': images, 'title': title}
  except Exception as e:
    print(f"Error scraping website: {e}")
    return None


# Example usage
target_url = 'https://blog.hubspot.com/marketing/how-to-use-medium'
data = scrape_website(target_url)

if data:
  print("Extracted Body Text:")
  print(data["text"])
  print("\nDownloaded Images:")
  print(data["images"])
else:
  print("Failed to scrape website.")
