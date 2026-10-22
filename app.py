from flask import Flask, request, send_from_directory
import sqlite3
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__)

DB_PATH = "km.db"

# -----------------------------
# DATABASE INITIALISATIE
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS ritten (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datum TEXT,
            begin INTEGER,
            eind INTEGER,
            van TEXT,
            via TEXT,
            naar TEXT,
            reden TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()  # database wordt automatisch aangemaakt bij start


# -----------------------------
# HOMEPAGE
# -----------------------------
@app.route("/")
def index():
    return send_from_directory("templates", "index.html")


# -----------------------------
# KM OPSLAAN
# -----------------------------
@app.route("/api/km", methods=["POST"])
def save_km():
    try:
        data = request.json
        print("Request ontvangen:", data)

        if not data:
            return {"status": "error", "message": "Geen JSON"}, 400

        # Opslaan in SQLite
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO ritten (datum, begin, eind, van, via, naar, reden)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("datum"),
            data.get("begin"),
            data.get("eind"),
            data.get("van"),
            data.get("via"),
            data.get("naar"),
            data.get("reden")
        ))
        conn.commit()
        conn.close()

        print("Rit opgeslagen in database.")

        return {"status": "ok"}

    except Exception as e:
        print("Fout:", str(e))
        return {"status": "error", "message": str(e)}, 500


# -----------------------------
# laatste km stand als start volgende keer
# -----------------------------


@app.route("/api/lastkm")
def last_km():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT eind FROM ritten ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()

    if row:
        return {"lastkm": row[0]}
    else:
        return {"lastkm": None}


# -----------------------------
# DATABASE DOWNLOADEN
# -----------------------------
@app.route("/download-db")
def download_db():
    db_path = "km.db"   # <-- correcte naam
    if not os.path.exists(db_path):
        return {"status": "error", "message": "Database bestaat niet"}, 404

    return send_from_directory(
        directory=".",
        path=db_path,
        as_attachment=True
    )


# -----------------------------
# LOKAAL TESTEN
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# -----------------------------
# overzicht paigna
# -----------------------------

@app.route("/overzicht")
def overzicht():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT datum, begin, eind, van, via, naar, reden FROM ritten ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    html = """
    <html>
    <head>
        <title>Overzicht ritten</title>
        <style>
            body { font-family: Arial; background: #CFA94A; padding: 20px; }
            h2 { text-align: center; }
            table { width: 100%; border-collapse: collapse; background: white; }
            th, td { padding: 12px; border: 1px solid #ccc; font-size: 16px; }
            th { background: #333; color: white; }
            .btn { margin-top: 20px; padding: 14px; background: #333; color: white; border: none; border-radius: 8px; font-size: 18px; width: 100%; }
        </style>
    </head>
    <body>
        <h2>Overzicht ritten</h2>
        <table>
            <tr>
                <th>Datum</th>
                <th>Begin</th>
                <th>Eind</th>
                <th>Van</th>
                <th>Via</th>
                <th>Naar</th>
                <th>Reden</th>
            </tr>
    """

    for r in rows:
        html += f"""
            <tr>
                <td>{r[0]}</td>
                <td>{r[1]}</td>
                <td>{r[2]}</td>
                <td>{r[3]}</td>
                <td>{r[4]}</td>
                <td>{r[5]}</td>
                <td>{r[6]}</td>
            </tr>
        """

    html += """
        </table>
        <button class="btn" onclick="window.location.href='/'">Terug naar invoer</button>
    </body>
    </html>
    """

    return html
