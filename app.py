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
