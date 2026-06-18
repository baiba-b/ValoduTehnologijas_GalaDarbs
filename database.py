import ast
import os
import sqlite3
import pandas as pd


# Izveido SQLite datubāzi un tabulu, ja tās vēl nav.
def init_db():
    conn = sqlite3.connect("raksti.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raksti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            vietne TEXT,
            kategorija TEXT,
            bert_rezultats TEXT,
            izveidots TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# Saglabā vienu rakstu datubāzē un atjauno CSV eksportu.
def save_article(url, vietne, kategorija, bert_rezultats=None):
    conn = sqlite3.connect("raksti.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO raksti (
            url,
            vietne,
            kategorija,
            bert_rezultats
        )
        VALUES (?, ?, ?, ?)
    """, (
        url,
        vietne,
        kategorija,
        bert_rezultats
    ))

    conn.commit()
    conn.close()

    export_to_csv()


# Eksportē visu datubāzi uz CSV, sadalot bert_rezultats vārdnīcu atsevišķās kolonnās.
def export_to_csv():
    os.makedirs("data/csv", exist_ok=True)

    conn = sqlite3.connect("raksti.db")

    df = pd.read_sql_query("SELECT * FROM raksti", conn)

    if "bert_rezultats" in df.columns:
        emociju_dati = df["bert_rezultats"].apply(
            lambda x: ast.literal_eval(x) if pd.notna(x) else {}
        )

        emociju_df = pd.json_normalize(emociju_dati)

        df = pd.concat(
            [df.drop(columns=["bert_rezultats"]), emociju_df],
            axis=1
        )

    df.to_csv(
        "data/csv/raksti.csv",
        index=False,
        encoding="utf-8-sig"
    )

    conn.close()

    print("CSV atjaunots: data/csv/raksti.csv")
