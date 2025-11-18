from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import csv
from pathlib import Path
import time


# Init app
app = Flask(__name__)

# Entire inventory CSV df
BASE_DIR = Path(__file__).resolve().parent
DATA_CSV = BASE_DIR / "data" / "Inventory.csv"




# Home
@app.route("/")
def home():
    return render_template('home.html')




# Scanner Help Page
@app.route("/scannerHelp")
def scannerHelp():
    return render_template('scannerHelp.html')




# Helper function for pulling from the CSV
def pullDataCSV(location=None, lastSeen=False, maint=False):
    items = []

    # Opens the CSV file with inventory data, goes row by row pulling out each
    # items specifics based on passed in arguments to this helper function
    with open(DATA_CSV, newline="", encoding="utf-8") as csvfile:
        csvinv = csv.DictReader(csvfile)
        for row in csvinv:
            if location is not None and row["location"] != location:
                continue

            # Every table to be displayed will have these three columns
            item = {
                "name": row["category_name"],
                "serial": row["serial_number"],
                "location": row["location"],
                "inventoried": row["inventoried"]
            }

            # These are our optional add ons that get button selected by the user
            if lastSeen:
                item["lastSeen"] = row.get("last_seen")
            
            if maint:
                item["maintenance"] = row.get("maintenance")

            # append each item to the items list
            items.append(item)

    return items


@app.route("/getTable")
def getTable():
    inventory = pullDataCSV()

    return jsonify({"status": "ok", "items": inventory})


@app.route("/getTableLastSeen")
def getTableLastSeen():
    location = request.args.get("location")
    inventory = pullDataCSV(location=location, lastSeen=True)

    return jsonify({"status": "ok", "items": inventory})


@app.route("/getTableMaintenance")
def getTableMaintenance():
    location = request.args.get("location")
    inventory = pullDataCSV(location=location, maint=True)

    return jsonify({"status": "ok", "items": inventory})


# Sort the table based on A-Z or Z-A
@app.route("/sortTable")
def sortTable():
    direction = request.args.get("direction")   # Get direction A:ascending or D:decending
    location = request.args.get("location")     # Pull the location for sorting

    # Use our helper function to pull inventory
    if location == "Location":
        inventory = pullDataCSV()
    else:
        inventory = pullDataCSV(location=location)

    # Sort the inv based on asc/desc
    if direction == "A":
        inventory = sorted(inventory, key=lambda x: x["name"])
    elif direction == "D":
        inventory = sorted(inventory, key=lambda x: x["name"], reverse=True)

    return jsonify({"status": "ok", "items": inventory})


# Filter the table based on location
@app.route("/filterTable")
def filterTable():
    location = request.args.get("location")

    if location == "Location":
        inventory = pullDataCSV()
    else:
        inventory = pullDataCSV(location=location)


    return jsonify({"status": "ok", "items": inventory})




# Marking an item present in the CSV based on scan from frontend
@app.route("/markPresent")
def markPresent():
    value = request.args.get("value")
    currentTimeFormatted = f"{time.localtime().tm_mon}/{time.localtime().tm_mday}/{time.localtime().tm_year}"

    # Make the CSV a pandas df, update the value that's been scanned in, write it to the CSV
    df = pd.read_csv(DATA_CSV, dtype=str)
    df.loc[df["object_code"] == value, "inventoried"] = "T"
    df.loc[df["object_code"] == value, "last_seen"] = currentTimeFormatted     # This is the last time the item was scanned in
    df.to_csv(DATA_CSV, index=False)

    # Read the newly updated CSV data to be passed to the frontend
    inventory = pullDataCSV(lastSeen=True)

    return jsonify({"status": "ok", "items": inventory})


# Resets the inventory column to all false values in the CSV
@app.route("/resetInvCol")
def resetInvCol():
    inventory = []

    # Make the CSV a pandas df, update all inventoried cells to FALSE, write it to the CSV
    df = pd.read_csv(DATA_CSV, dtype=str)
    df["inventoried"] = "F"
    df.to_csv(DATA_CSV, index=False)

    # Read the newly updated CSV data to be passed to the frontend, we put the params to true
    # just in case the user has those columns open, we don't want data just disappearing
    inventory = pullDataCSV(lastSeen=True, maint=True)

    return jsonify({"status": "ok", "items": inventory})




# This is the page where we can scan an item and get all its data/info
@app.route("/info")
def info():
    return render_template("info.html")

# Backend API for getting that info off the CSV, then sending to the frontend
@app.route("/getItemInfo")
def getItemInfo():
    value = request.args.get("value")

    item = []

    # This one can stay and not be in the helper function since it just pulls one item
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




# Generating the PDF
@app.route("/generatepdf")
def generate_pdf_route():
    return "hello"




# Run the App
if __name__ == '__main__':
    app.run(debug=True)