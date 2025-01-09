from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os 
import requests 
from urllib.parse import urlparse


# Path to ChromeDriver
driver_path = "/home/devzone/Downloads/chromedriver-linux64/"  # Update this path if necessary
download_dir = "downloaded_pdfs/mhlawsite"

# Initialize Service object
service = Service(driver_path)

# Initialize WebDriver with the Service object
# driver = webdriver.Chrome(service=service)
driver = webdriver.Firefox()

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
}


def download_pdf(pdf_url):

    o = urlparse(pdf_url)
    #print(o)

    pdf_name = os.path.join(download_dir, os.path.basename(pdf_url).replace('%20', '_'))
    
    # Download the PDF
    pdf_response = requests.get(pdf_url, headers=headers)
    pdf_response.raise_for_status()
    
    # Save the PDF
    with open(pdf_name, "wb") as pdf_file:
        pdf_file.write(pdf_response.content)
    
    print(f"Downloaded: {pdf_name}")


# Function to download PDFs from a webpage
def download_pdfs_from_page():
    """Find and print PDF links on the current page."""
    pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
    for link in pdf_links:
        pdf_url = link.get_attribute("href")
        
        download_pdf(pdf_url)
        
        print(f"Found PDF link: {pdf_url}")





# Function to navigate through paginated pages and download PDFs
def navigate_and_download():
    """Navigate through pages and download PDFs."""
    base_url = "https://lj.maharashtra.gov.in/1297/Reprints-of-the-Act"
    driver.get(base_url)
    page_number = 1

    while True:
        print(f"\nProcessing page: {page_number}\n====================================================================================")

        try:
            # Wait for the table to load
            time.sleep(3)  # Simple delay for demonstration (replace with WebDriverWait if necessary)

            # Download PDFs from the current page
            download_pdfs_from_page()

            # Find the link to the next page and click it
            try:
                next_page = driver.find_element(
                    By.XPATH, f"//a[contains(@href, 'Page${page_number + 1}')]"
                )
                next_page.click()
                page_number += 1
            except:
                print("No more pages available.")
                break

        except Exception as e:
            print(f"Error on page {page_number}: {e}")
            break

# Run the script
try:
    navigate_and_download()
finally:
    driver.quit()
