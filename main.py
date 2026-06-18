import html_ieguve_no_url
import html_apstrade
import emociju_analize
import vizualizacija
from database import init_db, save_article

init_db()

html_apstrade.load_stoplist("data/stoplist.txt")

url1 = input("Pirmais URL: ")
url2 = input("Otrais URL: ")

raksts1 = html_ieguve_no_url.get_body_html(url1)
raksts2 = html_ieguve_no_url.get_body_html(url2)

site1 = raksts1["site"]
site2 = raksts2["site"]

category1 = raksts1["category"]
category2 = raksts2["category"]

html1 = raksts1["html"]
html2 = raksts2["html"]

# HTML -> tīrs teksts
teksts1 = html_apstrade.html_to_txt(html1)
teksts2 = html_apstrade.html_to_txt(html2)

# Teksts -> emocijas
emocijas1 = emociju_analize.analizet_emocijas(teksts1)
emocijas2 = emociju_analize.analizet_emocijas(teksts2)

bert_rezultats1 = str(emocijas1)
bert_rezultats2 = str(emocijas2)

save_article(url1, site1, category1, bert_rezultats1)
save_article(url2, site2, category2, bert_rezultats2)

print("\n=== Pirmais raksts ===")
print("Vietne:", site1)
print("Kategorija:", category1)
print("Emocijas:")
for emocija, varbutiba in emocijas1.items():
    print(f"  {emocija}: {varbutiba:.2f}")

print("\n=== Otrais raksts ===")
print("Vietne:", site2)
print("Kategorija:", category2)
print("Emocijas:")
for emocija, varbutiba in emocijas2.items():
    print(f"  {emocija}: {varbutiba:.2f}")

vizualizacija.attelot_emociju_salidzinajumu(emocijas1, emocijas2, site1, site2)