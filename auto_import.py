import html_ieguve_no_url
import html_apstrade
import emociju_analize
from database import init_db, save_article

URLS = [
    "https://www.lsm.lv/raksts/kas-notiek-latvija/raksti/17.06.2026-kas-notiek-latvija-aptauja-valsts-prezidenta-edgara-rinkevica-darbu-atzinigak-verte-jauniesi-un-augstu-ienakumu-sanemeji.a651894/",
    "https://www.lsm.lv/raksts/zinas/latvija/17.06.2026-veselibas-ministrija-uzdod-stradina-slimnicai-risinat-sastregumus-uznemsana.a651929/",
    "https://www.lsm.lv/raksts/sports/futbols/17.06.2026-pirmie-varti-un-punkts-pasaules-kausa-kongo-dr-futbolisti-parsteidz-portugali-un-spele-neizskirti.a651959/",
    "https://www.delfi.lv/sports/44523532/pasaules-kauss-futbola/120123173/anglijas-futbolisti-nospiez-horvatiju-un-uzvar-rezultativa-pasaules-kausa-cina",
    "https://www.delfi.lv/46713439/arzemes/120123152/dzivibas-atnemsana-vinam-ir-sports-longailendas-serijveida-slepkavam-piespriez-muza-ieslodzijumu",
    "https://www.delfi.lv/46713439/arzemes/120123161/pusaudzi-eiropas-savieniba-socialos-tiklus-verte-pozitivak-neka-vecaki-liecina-aptauja",
    "https://www.delfi.lv/46713439/arzemes/120123160/kostas-birojam-bijusi-diplomatiska-sazina-ar-kremli-pazino-es-amatpersona"
]


init_db()

# datubāzes populešana ar rakstiem no URL saraksta, iegūstot tekstu un analizējot emocijas, pēc tam saglabājot rezultātus datubāzē.
for url in URLS:
    print("\nApstrādā:", url)

    raksts = html_ieguve_no_url.get_body_html(url)

    site = raksts["site"]
    category = raksts["category"]
    html = raksts["html"]

    teksts = html_apstrade.html_to_txt(html)

    emocijas = emociju_analize.analizet_emocijas(teksts)

    save_article(
        url,
        site,
        category,
        str(emocijas),
        modelis=emociju_analize.NOKLUSETAIS_MODELIS
    )

    print("Saglabāts:", site, category)

print("\nVisi URL apstrādāti.")