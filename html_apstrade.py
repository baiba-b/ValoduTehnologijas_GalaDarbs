from bs4 import BeautifulSoup
import html
import re

# Globāla stopvārdu kopa
STOPLIST = set()


# Ielādē stopvārdus no faila
def load_stoplist(filepath):
    global STOPLIST

    with open(filepath, encoding="utf-8") as file:
        for line in file:
            STOPLIST.add(line.strip().lower())

    print(f"Ielādēti {len(STOPLIST)} stopvārdi")


# Noņem nevajadzīgus HTML elementus
def remove_html_elements(text):
    soup = BeautifulSoup(text, "html.parser")

    for element in soup.find_all(["header", "footer", "button", "nav", "aside"]):
        element.decompose()

    for element in soup.find_all(attrs={"class": re.compile(".*([Mm]enu|share|backlink|[Hh]eader|[Ff]ooter|breadcrumb|editor).*")}):
        element.decompose()

    return str(soup)


# kods ņemts no: https://colab.research.google.com/github/LUMII-AILab/NLP_Course/blob/main/notebooks/TextExtraction.ipynb#scrollTo=r6U6v5VezUNd
# Atkodē HTML entītijas un noņem HTML tagus
def convert_to_plaintext(text):
    text = html.unescape(text)
    text = BeautifulSoup(text, "html.parser").text
    return text


# Sakārto atstarpes un rindu pārtraukumus tīrajā tekstā
def normalize_white_spaces(text):
    text = re.sub("[ ]+", " ", text)
    text = re.sub("[ ]?\n+", "\n", text)
    return text


# HTML -> tīrs teksts
def html_to_txt(html_txt):
    text = html_txt
    text = remove_html_elements(text)
    text = convert_to_plaintext(text)
    text = normalize_white_spaces(text)
    return text
