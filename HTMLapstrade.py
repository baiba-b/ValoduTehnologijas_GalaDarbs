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


#kods ņemts no: https://colab.research.google.com/github/LUMII-AILab/NLP_Course/blob/main/notebooks/TextExtraction.ipynb#scrollTo=r6U6v5VezUNd
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

