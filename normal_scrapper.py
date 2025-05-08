import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Solicitar URL al usuario
URL = input("Enter the website URL: ")
if not URL.startswith("http://") and not URL.startswith("https://"):
    URL = "http://" + URL

# Encabezados para simular un navegador
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Petición a la web
response = requests.get(URL, headers=HEADERS)
if response.status_code != 200:
    print(f"❌ Error: Unable to access {URL} (Status Code: {response.status_code})")
    exit()

# Parsear HTML
soup = BeautifulSoup(response.text, "html.parser")

# Guardar HTML
HTML_FILE = "extracted_html.html"
with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(soup.prettify())
print(f"✅ Extracted HTML saved as '{HTML_FILE}'")

# ----------------------
# EXTRAER Y GUARDAR CSS
# ----------------------

all_css = ""

# CSS inline en <style>
for style in soup.find_all("style"):
    all_css += style.get_text() + "\n"

# CSS externos
css_links = [link["href"] for link in soup.find_all("link", {"rel": "stylesheet"}) if "href" in link.attrs]

for css_link in css_links:
    full_url = urljoin(URL, css_link)
    try:
        css_response = requests.get(full_url, headers=HEADERS)
        if css_response.status_code == 200:
            all_css += f"\n/* CSS from {full_url} */\n" + css_response.text + "\n"
    except Exception as e:
        print(f"⚠ Error downloading CSS from {full_url}: {e}")

# Guardar CSS
CSS_FILE = "styles.css"
with open(CSS_FILE, "w", encoding="utf-8") as f:
    f.write(all_css)
print(f"✅ Extracted CSS saved as '{CSS_FILE}'")

# ----------------------
# EXTRAER Y GUARDAR JS
# ----------------------

all_js = ""

# JavaScript externos
js_links = [script["src"] for script in soup.find_all("script") if script.get("src")]

for js_link in js_links:
    full_url = urljoin(URL, js_link)
    try:
        js_response = requests.get(full_url, headers=HEADERS)
        if js_response.status_code == 200:
            all_js += f"\n// JavaScript from {full_url}\n" + js_response.text + "\n"
    except Exception as e:
        print(f"⚠ Error downloading JS from {full_url}: {e}")

# JavaScript inline
for script in soup.find_all("script"):
    if not script.get("src") and script.string:
        all_js += f"\n// Inline JS\n{script.string}\n"

# Guardar JS
JS_FILE = "scripts.js"
with open(JS_FILE, "w", encoding="utf-8") as f:
    f.write(all_js)
print(f"✅ Extracted JavaScript saved as '{JS_FILE}'")
