from bs4 import BeautifulSoup
import html
import re

# Noņem nevajadzīgus HTML elementus (galvenes, kājenes, izvēlnes), lai paliktu tikai raksta teksts.
def remove_html_elements(text):
    soup = BeautifulSoup(text, "html.parser")

    # nav/aside parasti satur izvēlnes, robežceliņus (breadcrumbs) un sānjoslas - ne pašu rakstu
    for element in soup.find_all(["header", "footer", "button", "nav", "aside"]):
        element.decompose()

    # Nav restriktēts uz div, jo dažas vietnes (piem. apollo.lv) liek robežceliņus section tagā
    for element in soup.find_all(attrs={"class": re.compile(".*([Mm]enu|share|backlink|[Hh]eader|[Ff]ooter|breadcrumb|editor).*")}):
        element.decompose()

    return str(soup)


# kods ņemts no: https://colab.research.google.com/github/LUMII-AILab/NLP_Course/blob/main/notebooks/TextExtraction.ipynb#scrollTo=r6U6v5VezUNd
# Atkodē HTML entītijas un noņem HTML tagus, paturot saturu. Piem. &amp; => &, <p>saturs</p> => saturs.
def convert_to_plaintext(text):
    text = html.unescape(text)
    text = BeautifulSoup(text, "html.parser").text
    return text


# Sakārto atstarpes un rindu pārtraukumus tīrajā tekstā.
def normalize_white_spaces(text):
    text = re.sub("[ ]+", " ", text)
    text = re.sub("[ ]?\n+", "\n", text)
    return text


# Pilna HTML -> tīrs teksts plūsma: elementu noņemšana, atkodēšana, atstarpju sakārtošana.
def html_to_txt(html_txt):
    text = html_txt
    text = remove_html_elements(text)
    text = convert_to_plaintext(text)
    text = normalize_white_spaces(text)
    return text
