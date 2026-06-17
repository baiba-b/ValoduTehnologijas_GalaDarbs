from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


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

        site = urlparse(url).netloc.replace("www.", "")

        return {
            "site": site,
            "html": str(soup.body) if soup.body else "Body nav atrasts"
        }

    except Exception as e:
        return {
            "site": None,
            "html": f"Kļūda: {e}"
        }