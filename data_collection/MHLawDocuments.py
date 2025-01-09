import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the webpage containing the PDF links
base_url = 'https://lj.maharashtra.gov.in/1297/Reprints-of-the-Act'

# Directory to save downloaded PDFs
download_dir = 'downloaded_pdfs'
os.makedirs(download_dir, exist_ok=True)

# Headers to mimic a browser visit
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Send a GET request to the webpage
response = requests.get(base_url, headers=headers)
response.raise_for_status()  # Check for request errors

# Parse the webpage content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all anchor tags with href attributes ending in '.pdf'
pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))

print("PDF Links ::", len(pdf_links))

# Download each PDF
for link in pdf_links:
    pdf_url = urljoin(base_url, link['href'])
    pdf_name = os.path.join(download_dir, os.path.basename(pdf_url))

    # Download the PDF
    pdf_response = requests.get(pdf_url, headers=headers)
    pdf_response.raise_for_status()

    # Save the PDF to the specified directory
    with open(pdf_name, 'wb') as pdf_file:
        pdf_file.write(pdf_response.content)

    print(f'Downloaded: {pdf_name}')

print('All PDFs have been downloaded.')
