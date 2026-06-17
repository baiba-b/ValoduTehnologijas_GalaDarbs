import re
import regex
from collections import Counter

# Regulārā izteiksme tekstvienību (tokenu) sadalīšanai.
# Atpazīst vārdus, skaitļus un pieturzīmes.
token_re = regex.compile(r"\[\p{L}+\]|\p{L}+|\d+|\p{P}")

# Globāla stopvārdu kopa.
STOPLIST = set()


# Ielādē stopvārdus no faila.
def load_stoplist(filepath):
    global STOPLIST

    with open(filepath, encoding="utf-8") as file:
        for line in file:
            STOPLIST.add(line.strip().lower())

    print(f"Ielādēti {len(STOPLIST)} stopvārdi")


# Teksta normalizācija.
# pārvērš mazos burtos, noņem e-pastus, noņem URL adreses, aizvieto skaitļus ar vienotu vērtību "100".
def preprocess_text(text):
    text = str(text)

    # Ja teksts nav pilnībā ar lielajiem burtiem, tad pārvērš to mazajos burtos.
    if not text.isupper():
        text = text.lower()

    # Noņem e-pasta adreses
    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "",
        text
    )

    # Noņem URL adreses
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # Aizvieto visus skaitļus ar 100
    text = re.sub(r"\d+", "100", text)

    return text.strip()


# Sadala tekstu tekstvienībās (tokenos)
# un izmet stopvārdus un vienzīmes tokenus.
def tokenize(text):
    text = preprocess_text(text)

    tokens = token_re.findall(text)

    filtered_tokens = []

    for token in tokens:

        # Izmet stopvārdus
        if token.lower() in STOPLIST:
            continue

        # Izmet vienas rakstzīmes tokenus
        if len(token) <= 1:
            continue

        filtered_tokens.append(token)

    return filtered_tokens


# Izveido tekstvienību biežumsarakstu.
# Ja norādīts output_path, saglabā rezultātu failā.
def create_frequency_list(texts, output_path=None):
    token_counts = Counter()

    for text in texts:
        token_counts.update(tokenize(text))

    if output_path:
        with open(output_path, "w", encoding="utf-8") as file:
            for token, freq in token_counts.most_common():
                file.write(f"{freq}\t{token}\n")

    return token_counts


# Ielādē stopvārdus kā atsevišķu kopu.
def load_stoplist_set(stoplist_path):
    stoplist = set()

    with open(stoplist_path, encoding="utf-8") as file:
        for line in file:
            word = preprocess_text(line.strip())

            if word:
                stoplist.add(word)

    return stoplist


# Ielādē vārdnīcu no biežumsaraksta.
# Saglabā tikai tekstvienības, kuru biežums ir >= min_freq.
def load_whitelist(freq_path, min_freq=3):
    whitelist = set()

    with open(freq_path, encoding="utf-8") as file:
        for line in file:
            freq, token = line.strip().split("\t")

            if int(freq) >= min_freq:
                whitelist.add(token)

    return whitelist


# Filtrē tekstvienības:
# - izmet stopvārdus,
# - izmet pārāk īsus tokenus,
# - atstāj tikai whitelist vārdnīcas tokenus.
def normalize_tokens(tokens, stoplist=None, whitelist=None, min_len=2):
    filtered_tokens = []

    for token in tokens:

        if stoplist and token in stoplist:
            continue

        if len(token) < min_len:
            continue

        if whitelist and token not in whitelist:
            continue

        filtered_tokens.append(token)

    return filtered_tokens


# Pilna priekšapstrāde:
# tokenizācija + filtrēšana.
def tokenize_and_normalize(text, stoplist=None, whitelist=None):
    tokens = tokenize(text)
    return normalize_tokens(tokens, stoplist, whitelist)