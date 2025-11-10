from flask import Flask, render_template, request, Response, jsonify
import pandas as pd
import csv


# Init app
app = Flask(__name__)

# Entire inventory CSV df
data = pd.read_csv('./data/Inventory.csv')
# df narrowed down to item name, serial, and location
items = data[['category_name','serial_number', 'location']]




# Home
@app.route("/")
def home():
    # Initially when hitting home page, load in the inventory at all locations
    items_html = render_table(items)
    return render_template('home.html', items_html=items_html)




# Route where the front-end requests a new table because a radio btn was pressed with a
# specific location (filters the table). We also have the sorting logic in here in case
# one of those btns is pressed
@app.route("/table")
def table():
    location = request.args.get("location")
    sortDirection = request.args.get("sortDirection")

    if location == "ALL":
        df = items
    else:
        df = items[items["location"] == location]

    if sortDirection == "A-Z":
        df = df.sort_values(by="category_name", ascending=True, na_position="last")
    elif sortDirection == "Z-A":
        df = df.sort_values(by="category_name", ascending=False, na_position="last")
    
    return Response(render_table(df), mimetype="text/html")


# This turns the dataframe passed in to an HTML table to be passed to front-end
def render_table(df):
    return df.to_html(index=False, table_id='itemTable', border=1)




# This is the scanner page
@app.route("/scan")
def scan():
    return render_template("scan.html")


# This matches the scanned value to the items information
@app.route("/getItem")
def getItem():
    scanVal = request.args.get("scanVal", "").strip()
    
    # Find the name of the item in the CSV based on the scanner value from the frontend
    with open("./data/Inventory.csv", newline="", encoding="utf-8") as csvfile:
        inventory = csv.DictReader(csvfile)

        for row in inventory:
            if row["object_code"] == scanVal:
                # This is where we change what all info we want to pull about the item
                return jsonify({"status": "ok", "itemName": row["category_name"], "itemSerial": row["serial_number"]})

    # If we don't find the item, return this...
    return jsonify({"status": "ok", "itemName": "Item name not found in DB", "itemSerial": "Item serial # not found in DB"})




# Run the App
if __name__ == '__main__':
    app.run(debug=True)