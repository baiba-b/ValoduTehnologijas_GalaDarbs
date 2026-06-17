import requests
from bs4 import BeautifulSoup
import html
import re

# Iegūst HTML kodu no mājaslapas
def get_body_html(url):
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        return str(soup.body) if soup.body else "Body nav atrasts"

    except Exception as e:
        return f"Kļūda: {e}"


url1 = input("Pirmais URL: ")
url2 = input("Otrais URL: ")

teksts1 = get_body_html(url1)
teksts2 = get_body_html(url2)

from bs4 import BeautifulSoup
import html
import re


# Removes specific HTML elements from a webpage to get rid of needless content.
# For instance: header and footer blocks, menus, etc.
# Needs to be adapted for each website to get the best results.
def remove_html_elements(text):
    soup = BeautifulSoup(text, "html.parser")

    # Filtering by specific HTML elements
    for element in soup.find_all(["header", "footer", "button"]):
        element.decompose() # Removes an element from the tree

    # Filtering by HTML elements having specific attributes
    for element in soup.find_all(["div"], attrs={"class": re.compile(".*([Mm]enu|share|backlink).*")}):
        element.decompose()

    return str(soup)


# (1) Unescapes HTML entities.
# (2) Removes HTML tags while keeping the content.
# For instance: &amp; => &, <p>content</p> => content.
# This function is universal - it can be applied to any webpage from any website.
def convert_to_plaintext(text):
    text = html.unescape(text)                     # 1
    text = BeautifulSoup(text, "html.parser").text # 2
    return text


# Normalizes spaces and line breaks in the plain-text.
def normalize_white_spaces(text):
    text = re.sub("[ ]+", " ", text)
    text = re.sub("[ ]?\n+", "\n", text) # Try to comment out this line
    return text


# (1) Removal of needless HTML elements.
# (2) Unescaping HTML entities and removal of HTML tags.
# (3) Normalization of whitespaces in the plain-text.
def html_to_txt(html_txt):
    text = html_txt

    # with open(html_file, "r", encoding="utf-8") as input_file:
    #     text = input_file.read()

    text = remove_html_elements(text)   # 1
    text = convert_to_plaintext(text)   # 2
    text = normalize_white_spaces(text) # 3

    # with open(txt_file, "w", encoding="utf-8") as output_file:
    #     output_file.write(text)
    return text


teksts1= html_to_txt(teksts1)
teksts2 = html_to_txt(teksts2)



print("\n=== Pirmais raksts ===")
print(teksts1)

# print("\n=== Otrais raksts ===")
# print(teksts2)