from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


# URL kategoriju kartējums uz vienotām kategorijām
CATEGORY_MAP = {
    "politika": "Politika",
    "latvija": "Latvija",
    "pasaule": "Pasaule",
    "ekonomika": "Ekonomika",

    "sports": "Sports",
    "futbols": "Sports",
    "basketbols": "Sports",
    "hokejs": "Sports",
    "teniss": "Sports",
    "volejbols": "Sports",
    "florbols": "Sports",

    "kultura": "Kultūra",
    "izklaide": "Izklaide",
    "tehnologijas": "Tehnoloģijas",
    "auto": "Auto",
    "veseliba": "Veselība"
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

        if category_key in CATEGORY_MAP:
            return CATEGORY_MAP[category_key]

    # Rezerves variants: pārbauda visus URL fragmentus
    for part in parts:
        if part in CATEGORY_MAP:
            return CATEGORY_MAP[part]

    return None


# Mēģina iegūt kategoriju no HTML meta informācijas
def find_category_from_html(soup):
    meta = soup.find("meta", attrs={"property": "article:section"})
    if meta and meta.get("content"):
        category_key = meta["content"].strip().lower()

        if category_key in CATEGORY_MAP:
            return CATEGORY_MAP[category_key]

        return meta["content"].strip()

    meta = soup.find("meta", attrs={"name": "section"})
    if meta and meta.get("content"):
        category_key = meta["content"].strip().lower()

        if category_key in CATEGORY_MAP:
            return CATEGORY_MAP[category_key]

        return meta["content"].strip()

    return None


# Prasa lietotājam izvēlēties kategoriju
def ask_user_category():
    categories = sorted(set(CATEGORY_MAP.values()))

    print("\nIzvēlies kategoriju:")

    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")

    while True:
        choice = input("Ievadi kategorijas numuru: ")

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(categories):
                return categories[choice - 1]

        print("Nederīga izvēle. Mēģini vēlreiz.")


# Prasa apstiprināt automātiski noteikto kategoriju
def confirm_category(category):
    if category is None:
        print("\nKategoriju neizdevās automātiski noteikt.")
        return ask_user_category()

    while True:
        answer = input(f"\nNoteiktā kategorija ir '{category}'. Vai tā ir pareiza? (j/n): ").strip().lower()

        if answer in ["j", "ja", "jā", "y", "yes"]:
            return category

        if answer in ["n", "ne", "no"]:
            return ask_user_category()

        print("Lūdzu ievadi 'j' vai 'n'.")


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

        # Lietotājs apstiprina vai labo kategoriju
        category = confirm_category(category)

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