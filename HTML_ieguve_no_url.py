from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


# URL kategoriju kartējums uz vienotām kategorijām
CATEGORY_MAP = {
    "politika": "Politika",
    "latvija": "Latvija",
    "pasaule": "Pasaule",
    "ekonomika": "Ekonomika",
    "bizness": "Ekonomika",
    "sports": "Sports",
    "kultura": "Kultūra",
    "kultūra": "Kultūra",
    "izklaide": "Izklaide",
    "tehnologijas": "Tehnoloģijas",
    "auto": "Auto",
    "veseliba": "Veselība",
    "veselība": "Veselība",
    "laika-zinas": "Laika ziņas",
    "kriminalzinas": "Kriminālziņas",
    "kriminālziņas": "Kriminālziņas",
    "viedokli": "Viedokļi",
    "viedokļi": "Viedokļi"
}


# Mēģina noteikt kategoriju no URL struktūras
def find_category_from_url(url):
    path = urlparse(url).path.lower()
    parts = [p for p in path.split("/") if p]

    print("URL daļas:", parts)

    if len(parts) >= 2 and parts[0] == "raksts":

        # LSM ziņu sadaļā izmanto trešo URL daļu
        if len(parts) >= 3 and parts[1] == "zinas":
            category_key = parts[2]
        else:
            category_key = parts[1]

        category_map = {
            "sports": "Sports",
            "futbols": "Sports",
            "zinas": "Ziņas",
            "latvija": "Latvija",
            "pasaule": "Pasaule",
            "ekonomika": "Ekonomika",
            "kultura": "Kultūra",
            "kultūra": "Kultūra",
            "dzive--stils": "Dzīvesstils",
            "dzive-stils": "Dzīvesstils",
            "tehnologijas": "Tehnoloģijas"
        }

        if category_key in category_map:
            return category_map[category_key]

    return None


# Mēģina iegūt kategoriju no HTML meta informācijas
def find_category_from_html(soup):

    meta = soup.find("meta", attrs={"property": "article:section"})
    if meta and meta.get("content"):
        return meta["content"]

    meta = soup.find("meta", attrs={"name": "section"})
    if meta and meta.get("content"):
        return meta["content"]

    return None


# Prasa lietotājam izvēlēties kategoriju
def ask_user_category():
    categories = sorted(set(CATEGORY_MAP.values()))

    print("\nKategoriju neizdevās automātiski noteikt.")
    print("Izvēlies kategoriju:")

    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")

    while True:
        choice = input("Ievadi kategorijas numuru: ")

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(categories):
                return categories[choice - 1]

        print("Nederīga izvēle. Mēģini vēlreiz.")


# Iegūst HTML kodu un kategoriju no mājaslapas
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

        site = urlparse(url).netloc.replace("www.", "")

        # Vispirms mēģina noteikt kategoriju no HTML
        category = find_category_from_html(soup)

        # Ja neizdodas, mēģina no URL
        if category is None:
            category = find_category_from_url(url)

        # Ja joprojām neizdodas, jautā lietotājam
        if category is None:
            category = ask_user_category()

        return {
            "site": site,
            "category": category,
            "html": str(soup.body) if soup.body else "Body nav atrasts"
        }

    except Exception as e:
        return {
            "site": None,
            "category": None,
            "html": f"Kļūda: {e}"
        }