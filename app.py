from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import csv
from pathlib import Path
import time
from gen2062 import *


# Init app
app = Flask(__name__)

# Entire inventory CSV df
BASE_DIR = Path(__file__).resolve().parent
DATA_CSV = BASE_DIR / "data" / "Inventory.csv"

# 2062 Template and Dir
TEMPLATE_PATH = BASE_DIR / "docs" / "base2062.docx"
OUTPUT_DIR = BASE_DIR / "docs" / "filled"




# Home
@app.route("/")
def home():
    return render_template('home.html')




# Scanner Help Page
@app.route("/scannerHelp")
def scannerHelp():
    return render_template('scannerHelp.html')




# Helper function for pulling from the CSV
def pullDataCSV(location=None, lastSeen=False, maint=False, holder=False):
    items = []

    # Opens the CSV file with inventory data, goes row by row pulling out each
    # items specifics based on passed in arguments to this helper function
    with open(DATA_CSV, newline="", encoding="utf-8") as csvfile:
        csvinv = csv.DictReader(csvfile)
        for row in csvinv:
            if location is not None and location != "Location" and row["location"] != location:
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

            if holder:
                item["holder"] = row.get("holder")

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


@app.route("/getTableHolder")
def getTableHolder():
    location = request.args.get("location")
    inventory = pullDataCSV(location=location, holder=True)

    return jsonify({"status": "ok", "items": inventory})


# Sort the table based on A-Z or Z-A
@app.route("/sortTable")
def sortTable():
    direction = request.args.get("direction")   # Get direction A:ascending or D:decending
    location = request.args.get("location")     # Pull the location for sorting
    maint = request.args.get("maint")
    seen = request.args.get("seen")

    # Use our helper function to pull inventory
    if location == "Location":
        inventory = pullDataCSV(lastSeen=seen, maint=maint)
    else:
        inventory = pullDataCSV(location=location, lastSeen=seen, maint=maint)

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
    maint = request.args.get("maint")
    seen = request.args.get("seen")

    if location == "Location":
        inventory = pullDataCSV(lastSeen=seen, maint=maint)
    else:
        inventory = pullDataCSV(location=location, lastSeen=seen, maint=maint)


    return jsonify({"status": "ok", "items": inventory})




# Marking an item present in the CSV based on scan from frontend
@app.route("/markPresent")
def markPresent():
    value = request.args.get("value")
    location = request.args.get("location")
    seen = request.args.get("seen")
    maint = request.args.get("maint")
    
    currentTimeFormatted = f"{time.localtime().tm_mon}/{time.localtime().tm_mday}/{time.localtime().tm_year}"

    # Make the CSV a pandas df, update the value that's been scanned in, write it to the CSV
    df = pd.read_csv(DATA_CSV, dtype=str)
    df.loc[df["object_code"] == value, "inventoried"] = "T"
    df.loc[df["object_code"] == value, "last_seen"] = currentTimeFormatted     # This is the last time the item was scanned in
    df.to_csv(DATA_CSV, index=False)

    # Read the newly updated CSV data to be passed to the frontend
    if location == "Location" or location is None:
        inventory = pullDataCSV(lastSeen=seen, maint=maint)
    else:
        inventory = pullDataCSV(location=location, lastSeen=seen, maint=maint)

    return jsonify({"status": "ok", "items": inventory})




# Changes the holder of an item based on what's passed in from the frontend
@app.route("/changeHolder")
def changeHolder():
    name = request.args.get("name")
    item = request.args.get("item")
    serial = request.args.get("serial")
    location = request.args.get("location")
    seen = request.args.get("seen")
    maint = request.args.get("maint")

    df = pd.read_csv(DATA_CSV, dtype=str)
    df.loc[(df["category_name"] == item) & (df["serial_number"] == serial), "holder"] = name
    df.to_csv(DATA_CSV, index=False)

    if location == "Location" or location is None:
        inventory = pullDataCSV(lastSeen=seen, maint=maint, holder=True)
    else:
        inventory = pullDataCSV(location=location, lastSeen=seen, maint=maint, holder=True)

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
    inventory = pullDataCSV()

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




# Sending the PDF once generated
@app.route("/get2062")
def get2062():
    # Let the gen2062.py file handle all the docx creation, then send it to the frontend for download
    client = request.args.get("client")
    path = generate2062docx(client=client)

    return send_file(
        path,
        as_attachment=True,
        download_name=f"Generated2062.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )




# Run the App
if __name__ == '__main__':
    app.run(debug=True)