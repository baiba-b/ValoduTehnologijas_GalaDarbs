import HTML_ieguve_no_url
import HTMLapstrade
import prieksapstrade
import EmocijuAnalize
import Vizualizacija
from database import init_db, save_article

init_db()


prieksapstrade.load_stoplist("data/stoplist.txt")

url1 = input("Pirmais URL: ")
url2 = input("Otrais URL: ")

raksts1 = HTML_ieguve_no_url.get_body_html(url1)
raksts2 = HTML_ieguve_no_url.get_body_html(url2)

site1 = raksts1["site"]
site2 = raksts2["site"]

category1 = raksts1["category"]
category2 = raksts2["category"]

html1 = raksts1["html"]
html2 = raksts2["html"]

# HTML -> tīrs teksts
teksts1 = HTMLapstrade.html_to_txt(html1)
teksts2 = HTMLapstrade.html_to_txt(html2)

# Teksts -> tekstvienības (tokeni)
# tekstvienibas1 = prieksapstrade.tokenize(teksts1)
# tekstvienibas2 = prieksapstrade.tokenize(teksts2)

# Teksts -> emocijas (BERT, izmanto tīro tekstu, nevis tekstvienības)
emocijas1 = EmocijuAnalize.analizet_emocijas(teksts1)
emocijas2 = EmocijuAnalize.analizet_emocijas(teksts2)

bert_rezultats1 = str(emocijas1)
bert_rezultats2 = str(emocijas2)

save_article(url1, site1, category1, str(emocijas1))
save_article(url2, site2, category2, str(emocijas2))

print("\n=== Pirmais raksts ===")
print("Vietne:", site1)
print("Kategorija:", category1)
# print(tekstvienibas1)
print("Emocijas:")
for emocija, varbutiba in emocijas1.items():
    print(f"  {emocija}: {varbutiba:.2f}")

print("\n=== Otrais raksts ===")
print("Vietne:", site2)
print("Kategorija:", category2)
# print(tekstvienibas2)
print("Emocijas:")
for emocija, varbutiba in emocijas2.items():
    print(f"  {emocija}: {varbutiba:.2f}")

#Šo var neņemt - izveido biežumsarakstu

from collections import Counter

# freq1 = Counter(tekstvienibas1)
# freq2 = Counter(tekstvienibas2)

# print("\nTop 20 tekstvienības 1. rakstā:")
# for token, count in freq1.most_common(20):
#     print(f"{token}: {count}")

# print("\nTop 20 tekstvienības 2. rakstā:")
# for token, count in freq2.most_common(20):
#     print(f"{token}: {count}")

Vizualizacija.attelot_emociju_salidzinajumu(emocijas1, emocijas2, site1, site2)