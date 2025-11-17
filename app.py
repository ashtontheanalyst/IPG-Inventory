from flask import Flask, render_template, request, jsonify, redirect, send_file
import pandas as pd
import csv
from pdfgeneration import *
from pathlib import Path


# Init app
app = Flask(__name__)

CSV_PATH = "./data/Inventory.csv"
PDF_TMP_DIR = Path("./tmp")
PDF_TMP_DIR.mkdir(exist_ok=True)

# Entire inventory CSV df
BASE_DIR = Path(__file__).resolve().parent
DATA_CSV = BASE_DIR / "data" / "Inventory.csv"

# inventory
inventory = []

# Home
@app.route("/")
def home():
    return render_template('home.html')

# Scanner Help Page
@app.route("/scannerHelp")
def scannerHelp():
    return render_template('scannerHelp.html')

@app.route("/getTable")
def getTable():
    inventory = []

    # Pulls the data from the csv file, updates the global inventory array as an array of dicts with each
    # item row, then sends it to the front end to make it a table
    with open(DATA_CSV, newline="", encoding="utf-8") as csvfile:
        csvinv = csv.DictReader(csvfile)
        for row in csvinv:
            inventory.append({
                "name": row["category_name"],
                "serial": row["serial_number"],
                "code": row["object_code"],
                "location": row["location"],
                "inventoried": row["inventoried"]
            })

    return jsonify({"status": "ok", "items": inventory})

# Sort the table based on A-Z or Z-A
@app.route("/sortTable")
def sortTable():
    direction = request.args.get("direction")   # Get direction A:ascending or D:decending
    location = request.args.get("location")     # Pull the location for sorting

    inventory = []  # Clear

    if location == "ALL":
        with open(DATA_CSV, newline="", encoding="utf-8") as csvfile:
            csvinv = csv.DictReader(csvfile)
            for row in csvinv:
                inventory.append({
                    "name": row["category_name"],
                    "serial": row["serial_number"],
                    "code": row["object_code"],
                    "location": row["location"],
                    "inventoried": row["inventoried"]
                })
    else:
        with open(DATA_CSV, newline="", encoding="utf-8") as csvfile:
            csvinv = csv.DictReader(csvfile)
            for row in csvinv:
                if row["location"] == location: # This is the line change for location
                    inventory.append({
                        "name": row["category_name"],
                        "serial": row["serial_number"],
                        "code": row["object_code"],
                        "location": row["location"],
                        "inventoried": row["inventoried"]
                    })

    if direction == "A":
        inventory = sorted(inventory, key=lambda x: x["name"])
    elif direction == "D":
        inventory = sorted(inventory, key=lambda x: x["name"], reverse=True)

    return jsonify({"status": "ok", "items": inventory})

# Filter the table based on location
@app.route("/filterTable")
def filterTable():
    location = request.args.get("location")

    inventory = []  # Clear

    if location != "ALL":
        with open(DATA_CSV, newline="", encoding="utf-8") as csvfile:
            csvinv = csv.DictReader(csvfile)
            for row in csvinv:
                if row["location"] == location:
                    inventory.append({
                        "name": row["category_name"],
                        "serial": row["serial_number"],
                        "code": row["object_code"],
                        "location": row["location"],
                        "inventoried": row["inventoried"]
                    })
    else:
        # Default table with items at all locations
        return redirect("/getTable")


    return jsonify({"status": "ok", "items": inventory})

# Marking an item present in the CSV based on scan from frontend
@app.route("/markPresent")
def markPresent():
    inventory = []
    value = request.args.get("value")

    # Make the CSV a pandas df, update the value that's been scanned in, write it to the CSV
    df = pd.read_csv(DATA_CSV, dtype=str)
    df.loc[df["object_code"] == value, "inventoried"] = "T"
    df.to_csv(DATA_CSV, index=False)

    # Read the newly updated CSV data to be passed to the frontend
    with open(DATA_CSV, newline="", encoding="utf-8") as csvfile:
        csvinv = csv.DictReader(csvfile)
        for row in csvinv:
            inventory.append({
                "name": row["category_name"],
                "serial": row["serial_number"],
                "code": row["object_code"],
                "location": row["location"],
                "inventoried": row["inventoried"]
            })

    return jsonify({"status": "ok", "items": inventory})

# Resets the inventory column to all false values in the CSV
@app.route("/resetInvCol")
def resetInvCol():
    inventory = []

    # Make the CSV a pandas df, update all inventoried cells to FALSE, write it to the CSV
    df = pd.read_csv(DATA_CSV, dtype=str)
    df["inventoried"] = "F"
    df.to_csv(DATA_CSV, index=False)

    # Read the newly updated CSV data to be passed to the frontend
    with open(DATA_CSV, newline="", encoding="utf-8") as csvfile:
        csvinv = csv.DictReader(csvfile)
        for row in csvinv:
            inventory.append({
                "name": row["category_name"],
                "serial": row["serial_number"],
                "code": row["object_code"],
                "location": row["location"],
                "inventoried": row["inventoried"]
            })

    return jsonify({"status": "ok", "items": inventory})

@app.route("/generatepdf")
def generate_pdf_route():
    project_name = request.args.get("project_name")
    if not project_name:
        return jsonify({"status": "error", "message": "Project name required"}), 400

    final_pdf = generate_pdf(project_name)
    if final_pdf.exists():
        return send_file(final_pdf, as_attachment=True, mimetype='application/pdf')
    else:
        return jsonify({"status": "error", "message": "Error generating PDF"}), 500

# This is the page where we can scan an item and get all its data/info
@app.route("/info")
def info():
    return render_template("info.html")

# Backend API for getting that info off the CSV, then sending to the frontend
@app.route("/getItemInfo")
def getItemInfo():
    value = request.args.get("value")

    item = []

    with open(DATA_CSV, newline="", encoding="utf-8") as csvfile:
        csvinv = csv.DictReader(csvfile)
        for row in csvinv:
            if row["object_code"] == value:
                item.append({
                    "name": row["category_name"],
                    "serial": row["serial_number"],
                    "code": row["object_code"],
                    "location": row["location"],
                    "inventoried": row["inventoried"]
                })

    return jsonify({"status": "ok", "item": item})




# Run the App
if __name__ == '__main__':
    app.run(debug=True)