import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Pēc noklusējuma izmantojam LVBERT, pielāgotu Ekman emociju klasifikācijai latviešu valodā.
# Vēlāk var pamēģināt citu (vai pašu apmācītu) BERT modeli,
NOKLUSETAIS_MODELIS = "AiLab-IMCS-UL/lvbert-emotions-ekman"
MAX_TOKENI = 480  # BERT limits ir 512, atstājam rezervi

_ieladetie_modeli = {}

# Ielādē tokenizatoru un modeli pēc nosaukuma (no Hugging Face hub).
# Ja modelis jau reiz ielādēts, atgriež to no keša.
def ieladet_modeli(model_name=NOKLUSETAIS_MODELIS):
    if model_name not in _ieladetie_modeli:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        model.eval()
        _ieladetie_modeli[model_name] = (tokenizer, model)

    return _ieladetie_modeli[model_name]


# Sadala garu tekstu vairākos gabalos pa teikumiem, lai katrs gabals ietilptu
# BERT 512 tokenu limitā. Nepieciešams, jo ziņu raksti parasti ir garāki par to.
def sadalit_teiku_gabalos(teksts, tokenizer, max_tokeni=MAX_TOKENI):
    teikumi = re.split(r"(?<=[.!?])\s+", teksts.strip())

    gabali = []
    dala = ""

    for teikums in teikumi:
        kandidats = (dala + " " + teikums).strip()
        tokenu_skaits = len(tokenizer.encode(kandidats, add_special_tokens=False))

        if tokenu_skaits > max_tokeni and dala:
            gabali.append(dala)
            dala = teikums
        else:
            dala = kandidats

    if dala:
        gabali.append(dala)

    return gabali


# Palaiž vienu teksta gabalu caur BERT modeli un atgriež katras emocijas
# varbūtību (0-1). Modelis ir multi-label, tāpēc izmanto sigmoid, nevis softmax.
def analizet_gabalu(teksts, tokenizer, model):
    inputs = tokenizer(teksts, return_tensors="pt", truncation=True, max_length=512)

    with torch.no_grad():
        outputs = model(**inputs)

    varbutibas = torch.sigmoid(outputs.logits)[0]
    id2label = model.config.id2label

    return {id2label[i]: varbutibas[i].item() for i in range(len(id2label))}


# Analizē visa raksta emocijas: sadala garumā gabalos, katru analizē atsevišķi
# un rezultātus vidējo, lai iegūtu emociju sadalījumu visam rakstam.
# Teksts šeit ir jau iztīrīts (piem. ar HTMLapstrade.html_to_txt), bet citādi
# nemainīts - BERT savam tokenizatoram pats vislabāk tiek galā ar dabīgu tekstu.
def analizet_emocijas(teksts, model_name=NOKLUSETAIS_MODELIS):
    tokenizer, model = ieladet_modeli(model_name)
    gabali = sadalit_teiku_gabalos(teksts, tokenizer)
    emocijas = model.config.id2label.values()

    if not gabali:
        return {emocija: 0.0 for emocija in emocijas}

    rezultati = [analizet_gabalu(gabals, tokenizer, model) for gabals in gabali]

    videjie = {}
    for emocija in emocijas:
        videjie[emocija] = sum(r[emocija] for r in rezultati) / len(rezultati)

    return videjie
