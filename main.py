import HTML_ieguve_no_url
import HTMLapstrade
import prieksapstrade

prieksapstrade.load_stoplist("data/stoplist.txt")

url1 = input("Pirmais URL: ")
url2 = input("Otrais URL: ")

raksts1 = HTML_ieguve_no_url.get_body_html(url1)
raksts2 = HTML_ieguve_no_url.get_body_html(url2)

site1 = raksts1["site"]
site2 = raksts2["site"]

html1 = raksts1["html"]
html2 = raksts2["html"]

# HTML -> tīrs teksts
teksts1 = HTMLapstrade.html_to_txt(html1)
teksts2 = HTMLapstrade.html_to_txt(html2)

# Teksts -> tekstvienības (tokeni)
tekstvienibas1 = prieksapstrade.tokenize(teksts1)
tekstvienibas2 = prieksapstrade.tokenize(teksts2)

print("\n=== Pirmais raksts ===")
print("Vietne:", site1)
print("Tekstvienības:")
print(tekstvienibas1)

print("\n=== Otrais raksts ===")
print("Vietne:", site2)
print("Tekstvienības:")
print(tekstvienibas2)

#Šo var neņemt - izveido biežumsarakstu

from collections import Counter

freq1 = Counter(tekstvienibas1)
freq2 = Counter(tekstvienibas2)

print("\nTop 20 tekstvienības 1. rakstā:")
for token, count in freq1.most_common(20):
    print(f"{token}: {count}")

print("\nTop 20 tekstvienības 2. rakstā:")
for token, count in freq2.most_common(20):
    print(f"{token}: {count}")