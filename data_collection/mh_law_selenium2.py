from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import requests
import time

# Path to ChromeDriver
driver_path = "/usr/local/bin/chromedriver"  # Update this path if necessary

# Initialize Service object
service = Service(driver_path)

# Initialize WebDriver with the Service object
driver = webdriver.Firefox()

# Directory to save downloaded PDFs
download_dir = "downloaded_pdfs/mhlawsite"

os.makedirs(download_dir, exist_ok=True)

def download_and_rename_pdfs(pageCount):
    """Find and download PDF links, renaming them with ShortTitle_ActYear_ActNo.pdf."""
    
    # Find the rows in the table
    rows = driver.find_elements(By.XPATH, "//table[@id='SitePH_Gridview1']/tbody/tr")
    
    rowCount = -1  
    
    print("Rows ::", len(rows))

    
    for row in rows:
        rowCount = rowCount + 1

        if rowCount == 0  or rowCount == 11 :
            continue

       
        # Extract the necessary details from columns
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) < 5:
            continue  # Skip if the row does not have enough columns

        act_no = columns[1].text.strip()  # Act No
        
        # This indicates its first row.
        if act_no == "SR.NO" :
            continue

        act_year = columns[2].text.strip()  # Act Year


        short_title = columns[3].text.strip().replace(" ", "_")  # Short Title (replace spaces with underscores)


        print("File data::", act_no, act_year, short_title)



        # Find the PDF link in the last column
        pdf_link = columns[5].find_element(By.TAG_NAME, "a").get_attribute("href")
        if not pdf_link:
            continue

        # Construct the filename
        filename = f"{short_title}_ACT{act_no}.pdf"
        filepath = os.path.join(download_dir, filename)

        # Download the PDF
        response = requests.get(pdf_link)
        with open(filepath, "wb") as file:
            file.write(response.content)

        print("File:", (rowCount + ((pageCount-1)*10)), " -> " , filename) 
        print(f"Downloaded and saved as: {filepath}")




def navigate_and_download():
    """Navigate through pages and download renamed PDFs."""
    base_url = "https://lj.maharashtra.gov.in/1297/Reprints-of-the-Act"
    driver.get(base_url)
    page_number = 1

    while True:
        print(f"\nProcessing page: {page_number}\n=====================================================================")

        try:
            # Wait for the table to load
            time.sleep(3)  # Simple delay for demonstration (replace with WebDriverWait if necessary)

            # Download and rename PDFs from the current page
            download_and_rename_pdfs(page_number)


            # Find the link to the next page and click it
            try:
                print(">>>>> Click Page No ::", page_number  )    
                page_number += 1
                next_page = driver.find_element(
                    By.XPATH, f"//a[contains(@href, 'Page${page_number}')]"
                )

                next_page.click()
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
