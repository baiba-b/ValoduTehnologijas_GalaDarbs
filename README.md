# ValoduTehnologijas_GalaDarbs
Gala darbs kursā "Valodu Tehnoloģiju pamati"

Uzstādīšana:
nepieciešams izpildīt sekojošās komandas termināli:
```
pip install requests beautifulsoup4 torch transformers matplotlib
```
testa datu ieguvei:
```
python auto_import.py
```
trenēšanai:
```
pip install datasets scikit-learn accelerate
```
palaišanas pirmajā reizē jāpalaiž:
```
python finetuned.py
python bertsalidzinajums.py
```
Tas izveidos mapes models/lvbert_final un models/bert_from_scratch_final. Bez tām main.py bus kļūda.

Šajā projektā tiek izmantots LV-BERT modelis.

Znotins, A., & Barzdins, G. (2020). LVBERT: Transformer-Based Model for Latvian Language Understanding [Conference paper]. Human Language Technologies - The Baltic Perspective, 328, 111–115.
