import unicodedata
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


# Katra kanoniskā kategorija ar visiem zināmajiem sinonīmiem/URL apzīmējumiem,
# ko dažādi portāli izmanto tai pašai tēmai (piem. LSM "arzemes", citur "ārvalstis").
# Ja parādās jauns portāls ar citu apzīmējumu, vienkārši pievieno to attiecīgajā sarakstā.
KATEGORIJU_SINONIMI = {
    "Latvija": ["latvija"],
    "Pasaule": ["pasaule", "arzemes", "ārzemes", "arvalstis", "ārvalstis", "starptautiska"],
    "Politika": ["politika"],
    "Ekonomika": ["ekonomika", "bizness", "finanses"],
    "Sports": ["sports", "futbols", "basketbols", "hokejs", "teniss", "volejbols", "florbols"],
    "Kultūra": ["kultura"],
    "Izklaide": ["izklaide"],
    "Tehnoloģijas": ["tehnologijas", "it"],
    "Auto": ["auto"],
    "Veselība": ["veseliba"],
    "Kriminālziņas": ["kriminalzinas", "noziegumi"],
    "Laika ziņas": ["laika-zinas", "laikazinas"],
    "Viedokļi": ["viedokli"]
}


# Pārvērš tekstu mazajos burtos un noņem diakritiskās zīmes, lai "Ārzemes",
# "arzemes" un "ārvalstis" varētu salīdzināt vienādi neatkarīgi no pieraksta.
def normalize_text(text):
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c))


# Plakana uzmeklēšanas vārdnīca: normalizēts sinonīms -> kanoniskā kategorija.
# Tiek uzbūvēta vienreiz no KATEGORIJU_SINONIMI, lai sinonīmus nevajadzētu uzturēt divviet.
CATEGORY_MAP = {
    normalize_text(sinonims): kategorija
    for kategorija, sinonimi in KATEGORIJU_SINONIMI.items()
    for sinonims in sinonimi
}


# Mēģina noteikt kategoriju no URL struktūras
def find_category_from_url(url):
    path = urlparse(url).path.lower()
    parts = [p for p in path.split("/") if p]

    print(f"URL daļas ({url}):", parts)

    if len(parts) >= 2 and parts[0] == "raksts":

        # LSM ziņu sadaļā izmanto trešo URL daļu
        if len(parts) >= 3 and parts[1] == "zinas":
            category_key = parts[2]
        else:
            category_key = parts[1]

        category_key = normalize_text(category_key)

        if category_key in CATEGORY_MAP:
            return CATEGORY_MAP[category_key]

    # Rezerves variants: pārbauda visus URL fragmentus
    for part in parts:
        if normalize_text(part) in CATEGORY_MAP:
            return CATEGORY_MAP[normalize_text(part)]

    return None


# Mēģina iegūt kategoriju no HTML meta informācijas
def find_category_from_html(soup):
    meta = soup.find("meta", attrs={"property": "article:section"})
    if meta and meta.get("content"):
        category_key = normalize_text(meta["content"])

        if category_key in CATEGORY_MAP:
            return CATEGORY_MAP[category_key]

        return meta["content"].strip()

    meta = soup.find("meta", attrs={"name": "section"})
    if meta and meta.get("content"):
        category_key = normalize_text(meta["content"])

        if category_key in CATEGORY_MAP:
            return CATEGORY_MAP[category_key]

        return meta["content"].strip()

    return None


# Prasa lietotājam izvēlēties kategoriju
def ask_user_category(url):
    categories = sorted(set(CATEGORY_MAP.values()))

    print(f"\nIzvēlies kategoriju rakstam: {url}")

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
def confirm_category(category, url):
    if category is None:
        print(f"\nKategoriju neizdevās automātiski noteikt rakstam: {url}")
        return ask_user_category(url)

    while True:
        answer = input(f"\nRakstam {url}\nnoteiktā kategorija ir '{category}'. Vai tā ir pareiza? (j/n): ").strip().lower()

        if answer in ["j", "ja", "jā", "y", "yes"]:
            return category

        if answer in ["n", "ne", "no"]:
            return ask_user_category(url)

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
        category = confirm_category(category, url)

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