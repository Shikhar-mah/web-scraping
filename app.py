from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import os
import threading
import time
import subprocess

app = Flask(__name__)
CORS(app)

data_file = "commodities_clean.csv"
scrapper_file = "scrapper.py"


# -------------------------------------
# AUTO REFRESH TASK (Every 30 seconds)
# -------------------------------------
def auto_refresh():
    while True:
        try:
            print("Running scrapper.py...")
            subprocess.run(["python", scrapper_file], check=True)
            print("CSV updated successfully.")
        except Exception as e:
            print("Error running scrapper:", e)

        time.sleep(30)


refresh_thread = threading.Thread(target=auto_refresh, daemon=True)
refresh_thread.start()


# -------------------------------------
# LOAD DATA FUNCTION
# -------------------------------------
def load_data():
    if not os.path.exists(data_file):
        return []

    with open(data_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        cleaned = []
        for row in reader:
            # strip whitespace from all values
            cleaned_row = {k: v.strip() for k, v in row.items()}
            cleaned.append(cleaned_row)

        return cleaned


def clean_numeric(value):
    try:
        return float(value.replace(",", "").replace("%", ""))
    except:
        return value


# -------------------------------------
# API ENDPOINTS
# -------------------------------------

@app.route("/commodities", methods=["GET"])
def get_commodities():

    data = load_data()

    category = request.args.get("category")
    commodity = request.args.get("commodity")

    if category:
        data = [
            d for d in data
            if d["category"].strip().lower() == category.strip().lower()
        ]

    if commodity:
        data = [
            d for d in data
            if commodity.lower() in d["commodity"].lower()
        ]

    sort_by = request.args.get("sort_by")
    order = request.args.get("order", "asc")

    if sort_by and data and sort_by in data[0]:
        reverse = True if order == "desc" else False
        data.sort(
            key=lambda x: clean_numeric(x.get(sort_by, "")),
            reverse=reverse
        )

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    start = (page - 1) * limit
    end = start + limit

    return jsonify({
        "total_records": len(data),
        "page": page,
        "limit": limit,
        "data": data[start:end]
    })


@app.route("/categories", methods=["GET"])
def get_categories():
    data = load_data()

    categories = sorted(
        set(d["category"].strip() for d in data)
    )

    return jsonify(categories)


@app.route("/commodities/<string:name>", methods=["GET"])
def get_single(name):
    data = load_data()

    for item in data:
        if item["commodity"].lower() == name.lower():
            return jsonify(item)

    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(debug=False)
