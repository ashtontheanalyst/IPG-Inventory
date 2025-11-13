# IPG Inventory System
This inventory system is to be used by members of the Bush Combat Development Complex,
more specifically the Innovation Proving Ground team.


## Capabilities
1. Compare the inventory that is scanned in versus a master list of all items. From there
the application should show the end user what item(s) are missing and at what location.
2. Rm.342 is priority for scanning items in/out, then we can expand to the OTA, OTA shed,
MCC, and MCC shed, etc.
3. Lofty goal is to have a notification system (most likely an email bot) that informs 
certain users when an item needs to be maintained, updated, patched, or etc.
4. Ethan created an Army HR 2062 generator which would build out a HR when you scanned
in items. The HR could then be printed out and used for range clients. This needs to
be spruced up; mainly, the HR shouldn't list every line item one by one, but instead 
utilize the item amount category to save line space.


## Progress
**11/7/25:**
- Ashton (lead), Avery, Brian, and Rosa (main client) fleshed out application capabilities 
as seen in the above section
- Created the [github](https://github.com/ashtontheanalyst/IPG-Inventory), configured
VS Code on RE-3, fresh python install and associated packages... set-up env
- Created a basic app that brings in the csv file as a dataframe, then displays the item
names and serial numbers on the home screen in a table
- The app will show the inventory as a table, can filter it based on items at a location, 
and then on top of that sort A-Z or Z-A

**11/10/25:**
- Tristan got the app running on python anywhere!
- Created a scan page that dynamically updates a table on page with scanned items and their
associated name/serial number. Can add more info if needed.
- Functionality being built in for 2062 creation and inventory check

**11/12/25:**
- Main inventory page will now be used to check if an item has been scanned or not. The fix
was just adding another column with 1 or 0 for if it's been scanned or not.
- Idea #3 created, working on it
- Idea #4 created
- Deleted the scan page, the home page is the main now
- Scanner can now be used in bluetooth or usb dongle 2.4 mode
- Updated the styling from 0 to a lot

**11/13/25**
- Scanner button lights up green (animated) whenever you scan an item in successfully so the
end user is sure it did something
- Scanned in items row in the table's background color gets changed to green in order to show
it's been scanned also
- Scanner is now in python anywhere under asmith@rellis email
- On Safari/Iphones, the scanner input wasn't working (our first bug yay), the button would
light up green but the row of the item's background wouldn't change or show that it had been
scanned. The issue was the the scannerInput element had to get some styling changes so that
Safari wouldn't siable it as "insecure"


## Ideas
1. Convert Ethan's Ruby on Rails application to a Python Flask application
2. Fix the hosting problem by hosting the Flask application on pythonanywhere with a 
username/password
3. The main inventory page can save a temp csv with all of the items that have been scanned
so that we can have a button that says 'Build 2062' and then it builds it with the saved list
4. Set the scanner to bluetooth mode, and make a separate page with the barcodes for configuring
the scanner/how to use it (help page)
