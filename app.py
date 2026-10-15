from flask import Flask, request, send_from_directory
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

@app.route("/api/km", methods=["POST"])
def save_km():
    try:
        print("Request ontvangen:", request.json)

        data = request.json
        if not data:
            print("Geen JSON ontvangen!")
            return {"status": "error", "message": "Geen JSON"}, 400

        df = pd.DataFrame([data])
        filename = f"rit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join("exports", filename)

        os.makedirs("exports", exist_ok=True)
        df.to_excel(filepath, index=False)

        print("Excel opgeslagen:", filepath)
        return {"status": "ok", "file": filename}

    except Exception as e:
        print("Fout in save_km:", str(e))
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
