from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import requests
import time
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient, PartitionKey

# Azure Blob Storage configuration
BLOB_CONNECTION_STRING = "your_blob_connection_string"  # Replace with your Blob Storage connection string
CONTAINER_NAME = "documents"

# Azure Cosmos DB configuration
COSMOS_ENDPOINT = "your_cosmos_db_endpoint"  # Replace with your Cosmos DB endpoint
COSMOS_KEY = "your_cosmos_db_key"  # Replace with your Cosmos DB primary key
DATABASE_NAME = "DocumentDB"
CONTAINER_NAME_METADATA = "DocumentsMetadata"

# Path to ChromeDriver
driver_path = "/usr/local/bin/chromedriver"  # Update this path if necessary

# Initialize Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client(CONTAINER_NAME)
blob_container_client.create_container(exist_ok=True)

# Initialize Azure Cosmos DB
cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
cosmos_database = cosmos_client.create_database_if_not_exists(DATABASE_NAME)
cosmos_container = cosmos_database.create_container_if_not_exists(
    id=CONTAINER_NAME_METADATA,
    partition_key=PartitionKey(path="/actNo"),
)

# Initialize Selenium WebDriver
service = Service(driver_path)
driver  = webdriver.Chrome(service=service)


def upload_to_blob(file_path, blob_name):
    """Upload a file to Azure Blob Storage."""
    with open(file_path, "rb") as file_data:
        blob_container_client.upload_blob(name=blob_name, data=file_data, overwrite=True)
    blob_url = f"{blob_service_client.primary_endpoint}/{CONTAINER_NAME}/{blob_name}"
    print(f"Uploaded to Blob Storage: {blob_url}")
    return blob_url


def save_metadata_to_cosmos(metadata):
    """Save document metadata to Azure Cosmos DB."""
    cosmos_container.create_item(body=metadata)
    print(f"Saved metadata to Cosmos DB: {metadata}")



def download_and_process_pdfs():
    """Download PDF links, upload them to Blob Storage, and save metadata to Cosmos DB."""
    rows = driver.find_elements(By.XPATH, "//table[@id='ctl00_SitePH_Gridview1']/tbody/tr")

    # Skip the first row (header) and the last row (pagination)
    for i, row in enumerate(rows):
        if i == 0 or i == len(rows) - 1:
            continue  # Skip the first and last rows

        # Extract columns from the row
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) < 5:
            continue  # Skip rows with insufficient columns

        # Extract Act No, Act Year, and Short Title
        act_no = columns[1].text.strip()
        act_year = columns[2].text.strip()
        short_title = columns[3].text.strip().replace(" ", "_")

        # Extract PDF link
        try:
            pdf_link = columns[4].find_element(By.TAG_NAME, "a").get_attribute("href")
            if not pdf_link:
                continue
        except:
            print(f"No valid PDF link found in row {i}.")
            continue

        # Construct file name and download the PDF
        filename = f"{short_title}_{act_year}_{act_no}.pdf"
        file_path = os.path.join("/tmp", filename)
        response = requests.get(pdf_link)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {file_path}")

        # Upload to Azure Blob Storage
        blob_url = upload_to_blob(file_path, filename)

        # Save metadata to Cosmos DB
        metadata = {
            "id": filename,  # Cosmos DB requires a unique id
            "actNo": act_no,
            "actYear": act_year,
            "shortTitle": short_title,
            "url": blob_url,
        }
        save_metadata_to_cosmos(metadata)

        # Remove the local file after upload
        os.remove(file_path)


def navigate_and_download():
    """Navigate through pages and process PDFs."""
    base_url = "https://lj.maharashtra.gov.in/1297/Reprints-of-the-Act"
    driver.get(base_url)
    page_number = 1

    while True:
        print(f"Processing page: {page_number}")

        try:
            time.sleep(3)
            download_and_process_pdfs()

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

try:
    navigate_and_download()
finally:
    driver.quit()
