import ast
import os
import sqlite3
import pandas as pd


# Izveido SQLite datubāzi un tabulu
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
            modelis TEXT,
            izveidots TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("PRAGMA table_info(raksti)")
    columns = [row[1] for row in cursor.fetchall()]

    if "modelis" not in columns:
        cursor.execute("ALTER TABLE raksti ADD COLUMN modelis TEXT")

    conn.commit()
    conn.close()


# Saglabā vienu rakstu db, atjauno CSV eksportu
def save_article(url, vietne, kategorija, bert_rezultats=None, modelis=None):
    conn = sqlite3.connect("raksti.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO raksti (
            url,
            vietne,
            kategorija,
            bert_rezultats,
            modelis
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        url,
        vietne,
        kategorija,
        bert_rezultats,
        modelis
    ))

    conn.commit()
    conn.close()

    export_to_csv()


# Eksportē visu datubāzi uz CSV
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


# Ielādē visas dotā modeļa rindas 
def _ieladet_emociju_df(modelis):
    conn = sqlite3.connect("raksti.db")
    df = pd.read_sql_query("SELECT * FROM raksti WHERE modelis = ?", conn, params=(modelis,))
    conn.close()

    emociju_dati = df["bert_rezultats"].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) else {}
    )

    return pd.concat([df.drop(columns=["bert_rezultats"]), pd.json_normalize(emociju_dati)], axis=1)


# Vidējās emocijas dotajām vietnēm (tikai dotā modeļa rindas).
def videjas_emocijas_pa_vietnem(vietnes, modelis):
    df = _ieladet_emociju_df(modelis)
    df = df[df["vietne"].isin(vietnes)]

    emociju_kolonnas = [c for c in df.columns if c not in ["id", "url", "vietne", "kategorija", "modelis", "izveidots"]]

    return df.groupby("vietne", dropna=False)[emociju_kolonnas].mean().to_dict(orient="index")


# Vidējās emocijas dotajām kategorijām (tikai dotā modeļa rindas).
def videjas_emocijas_pa_kategorijam(kategorijas, modelis):
    df = _ieladet_emociju_df(modelis)
    df = df[df["kategorija"].isin(kategorijas)]

    emociju_kolonnas = [c for c in df.columns if c not in ["id", "url", "vietne", "kategorija", "modelis", "izveidots"]]

    return df.groupby("kategorija", dropna=False)[emociju_kolonnas].mean().to_dict(orient="index")


# Vidējās emocijas visām DB esošajām vietnēm (tikai dotā modeļa rindas).
def videjas_emocijas_visam_vietnem(modelis):
    df = _ieladet_emociju_df(modelis)
    emociju_kolonnas = [c for c in df.columns if c not in ["id", "url", "vietne", "kategorija", "modelis", "izveidots"]]

    return df.groupby("vietne", dropna=False)[emociju_kolonnas].mean().to_dict(orient="index")


# Vidējās emocijas visām DB esošajām kategorijām (tikai dotā modeļa rindas).
def videjas_emocijas_visam_kategorijam(modelis):
    df = _ieladet_emociju_df(modelis)
    emociju_kolonnas = [c for c in df.columns if c not in ["id", "url", "vietne", "kategorija", "modelis", "izveidots"]]

    return df.groupby("kategorija", dropna=False)[emociju_kolonnas].mean().to_dict(orient="index")
