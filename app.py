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
# LOKAAL TESTEN
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
