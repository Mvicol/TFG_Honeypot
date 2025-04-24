import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# User input: Website URL
URL = input("Enter the website URL: ")
if not URL.startswith("http://") and not URL.startswith("https://"):
    URL = "http://" + URL

# Headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Request the webpage
response = requests.get(URL, headers=HEADERS)
if response.status_code != 200:
    print(f"❌ Error: Unable to access {URL} (Status Code: {response.status_code})")
    exit()

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Save the extracted HTML
HTML_FILE = "extracted_html.html"
with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(soup.prettify())
print(f"✅ Extracted HTML saved as '{HTML_FILE}'")

# Extract all CSS
all_css = ""

# Extract inline CSS from <style> tags
for style in soup.find_all("style"):
    all_css += style.get_text() + "\n"

# Extract and download external CSS files
css_links = [link["href"] for link in soup.find_all("link", {"rel": "stylesheet"}) if "href" in link.attrs]

for css_link in css_links:
    full_url = urljoin(URL, css_link)  # Convert relative links to absolute
    try:
        css_response = requests.get(full_url, headers=HEADERS)
        if css_response.status_code == 200:
            all_css += f"\n/* CSS from {full_url} */\n" + css_response.text + "\n"
    except Exception as e:
        print(f"⚠ Error downloading CSS from {full_url}: {e}")

# Save the extracted CSS
CSS_FILE = "styles.css"
with open(CSS_FILE, "w", encoding="utf-8") as f:
    f.write(all_css)
print(f"✅ Extracted CSS saved as '{CSS_FILE}'")