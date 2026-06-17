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

        return str(soup.body) if soup.body else "Body nav atrasts"

    except Exception as e:
        return f"Kļūda: {e}"


url1 = input("Pirmais URL: ")
url2 = input("Otrais URL: ")

teksts1 = get_body_html(url1)
teksts2 = get_body_html(url2)

print("\n=== Pirmais raksts ===")
print(teksts1)

print("\n=== Otrais raksts ===")
print(teksts2)