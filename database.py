import sqlite3


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