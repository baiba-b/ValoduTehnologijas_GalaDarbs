import csv
import os
import re

import html_ieguve_no_url
import html_apstrade

# rīks treniņa datu vākšanai

LABELS = {
    "1": "anger",
    "2": "disgust",
    "3": "fear",
    "4": "joy",
    "5": "neutral",
    "6": "sadness",
    "7": "surprise"
}


# Sadala tekstu teikumos un izmet pārāk īsos
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    cleaned = []

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) < 20:
            continue

        cleaned.append(sentence)

    return cleaned


# Parāda teikumu un liek lietotājam izvēlēties tā emociju no LABELS saraksta.
def ask_label(sentence):
    print("\nTeikums:")
    print(sentence)

    print("\nIzvēlies emociju:")
    for number, label in LABELS.items():
        print(f"{number}. {label}")

    while True:
        choice = input("Ievadi numuru: ").strip()

        if choice in LABELS:
            return LABELS[choice]

        print("Nederīga izvēle. Mēģini vēlreiz.")


# Pieraksta marķētos teikumus CSV failam
def save_labeled_sentences(rows, output_file):
    os.makedirs("data/csv", exist_ok=True)

    file_exists = os.path.exists(output_file)

    with open(output_file, "a", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "url",
                "site",
                "category",
                "sentence_id",
                "sentence",
                "manual_label"
            ]
        )

        if not file_exists:
            writer.writeheader()

        writer.writerows(rows)


# Iegūst rakstu, sadala teikumos, marķē katru un saglabā CSV
def main():
    url = input("Ievadi raksta URL: ").strip()

    raksts = html_ieguve_no_url.get_body_html(url)

    site = raksts["site"]
    category = raksts["category"]
    html = raksts["html"]

    text = html_apstrade.html_to_txt(html)

    sentences = split_sentences(text)

    print(f"\nAtrasti {len(sentences)} teikumi.")

    rows = []

    for index, sentence in enumerate(sentences, start=1):
        label = ask_label(sentence)

        rows.append({
            "url": url,
            "site": site,
            "category": category,
            "sentence_id": index,
            "sentence": sentence,
            "manual_label": label
        })

    output_file = "data/manual_emotion_labels.csv"
    save_labeled_sentences(rows, output_file)

    print(f"\nSaglabāts failā: {output_file}")


if __name__ == "__main__":
    main()