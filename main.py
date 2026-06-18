import html_ieguve_no_url
import html_apstrade
import emociju_analize
import vizualizacija
from database import (
    init_db,
    save_article,
    videjas_emocijas_pa_vietnem,
    videjas_emocijas_pa_kategorijam,
    videjas_emocijas_visam_vietnem,
    videjas_emocijas_visam_kategorijam
)

MODELI = [
    ("AiLab-IMCS-UL/lvbert-emotions-ekman", "LVBERT (Ekman)"),
    ("models/lvbert_final", "LVBERT (fine-tuned)"),
    ("models/bert_from_scratch_final", "BERT (no nulles)")
]
EKMAN_MODELIS = MODELI[0][0]

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


# Palaiž visus MODELI vienam rakstam, saglabā katru DB un atgriež modeļa_nosaukums: emocijas
def analizet_ar_visiem_modeliem(url, vietne, kategorija, teksts):
    rezultati = {}

    for model_id, nosaukums in MODELI:
        emocijas = emociju_analize.analizet_emocijas(teksts, model_name=model_id)
        save_article(url, vietne, kategorija, str(emocijas), modelis=model_id)
        rezultati[nosaukums] = emocijas

    return rezultati


rezultati1 = analizet_ar_visiem_modeliem(url1, site1, category1, teksts1)
rezultati2 = analizet_ar_visiem_modeliem(url2, site2, category2, teksts2)

print("\n=== Pirmais raksts ===")
print("Vietne:", site1)
print("Kategorija:", category1)
for nosaukums, emocijas in rezultati1.items():
    print(f"\n{nosaukums}:")
    for emocija, varbutiba in emocijas.items():
        print(f"  {emocija}: {varbutiba:.2f}")

print("\n=== Otrais raksts ===")
print("Vietne:", site2)
print("Kategorija:", category2)
for nosaukums, emocijas in rezultati2.items():
    print(f"\n{nosaukums}:")
    for emocija, varbutiba in emocijas.items():
        print(f"  {emocija}: {varbutiba:.2f}")

# Vienam rakstam 3 modeļu salīdzinājums
vizualizacija.attelot_salidzinajumu(rezultati1, f"3 modeļu salīdzinājums - {site1}", "grafiks_modeli_1.png")
vizualizacija.attelot_salidzinajumu(rezultati2, f"3 modeļu salīdzinājums - {site2}", "grafiks_modeli_2.png")

# šiem tikai lvbert-emotions-ekman dati no datubāzes
if site1 != site2:
    vietnu_emocijas = videjas_emocijas_pa_vietnem([site1, site2], EKMAN_MODELIS)
    vizualizacija.attelot_salidzinajumu(vietnu_emocijas, "Vietņu salīdzinājums", "grafiks_vietnes.png")

if category1 != category2:
    kategoriju_emocijas = videjas_emocijas_pa_kategorijam([category1, category2], EKMAN_MODELIS)
    vizualizacija.attelot_salidzinajumu(kategoriju_emocijas, "Kategoriju salīdzinājums", "grafiks_kategorijas.png")

visu_vietnu_emocijas = videjas_emocijas_visam_vietnem(EKMAN_MODELIS)
vietnu_neutralitate = {vietne: emocijas["neutral"] for vietne, emocijas in visu_vietnu_emocijas.items()}
vizualizacija.attelot_neitralitates_rangu(vietnu_neutralitate, "Neitralākie portāli", "grafiks_neitralakie_portali.png")

visu_kategoriju_emocijas = videjas_emocijas_visam_kategorijam(EKMAN_MODELIS)
kategoriju_neutralitate = {kategorija: emocijas["neutral"] for kategorija, emocijas in visu_kategoriju_emocijas.items()}
vizualizacija.attelot_neitralitates_rangu(kategoriju_neutralitate, "Neitralākās kategorijas", "grafiks_neitralakas_kategorijas.png")
