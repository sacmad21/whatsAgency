import os
import requests
from bs4 import BeautifulSoup

# Base URL for form submission
base_url = "https://lj.maharashtra.gov.in/1297/Reprints-of-the-Act"

# Directory to save downloaded PDFs
download_dir = "downloaded_pdfs/mhlawsite"
os.makedirs(download_dir, exist_ok=True)

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
}

def download_pdfs_from_page(soup):

    """Download all PDFs from the given page soup."""
    pdf_links = soup.find_all("a", href=lambda href: href and href.endswith(".pdf"))

    print("PDF Count:", len(pdf_links))
    for link in pdf_links:
        
        pdf_url = link['href']
        pdf_name = os.path.join(download_dir, os.path.basename(pdf_url))
        
        # Download the PDF
        pdf_response = requests.get(pdf_url, headers=headers)
        pdf_response.raise_for_status()
        
        # Save the PDF
        with open(pdf_name, "wb") as pdf_file:
            pdf_file.write(pdf_response.content)
        
        print(f"Downloaded: {pdf_name}")

def fetch_page(page_number):
    """Fetch content of a specific page by simulating the JavaScript call."""
    data = {
        "__EVENTTARGET": "ctl00$SitePH$Gridview1",
        "__EVENTARGUMENT": f"Page${page_number}",
    }
    
    response = requests.post(base_url, headers=headers, data=data)
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")

def download_all_pdfs():
    """Iterate over pages and download all PDFs."""
    page_number = 1
    
    while True:
        print(f"Processing page: {page_number}")
        try:
            # Fetch page content
            soup = fetch_page(page_number)
            
            print(soup.prettify())

            # Extract and download PDFs from the current page
            download_pdfs_from_page(soup)
            
            # Increment to the next page
            page_number += 1
        
        except Exception as e:
            print(f"No more pages to process or an error occurred: {e}")
            break
    
    print("All PDFs downloaded.")

# Start the process
download_all_pdfs()
