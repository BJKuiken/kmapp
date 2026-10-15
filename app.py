from flask import Flask, request, render_template
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/km", methods=["POST"])
def save_km():
    data = request.json

    # Excel-bestand maken
    df = pd.DataFrame([data])
    filename = f"rit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join("exports", filename)

    # Zorg dat de map bestaat
    os.makedirs("exports", exist_ok=True)

    df.to_excel(filepath, index=False)

    return {"status": "ok", "file": filename}
