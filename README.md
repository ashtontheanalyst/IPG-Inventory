# IPG Inventory System
This inventory system is to be used by members of the Bush Combat Development Complex,
more specifically the Innovation Proving Ground team.


## Capabilities by NOV21
1. **[DONE]** Compare the inventory that is scanned in versus a master list of all items. From there
the application should show the end user what item(s) are missing and at what location.
2. **[DONE]** Rm.342 is priority for scanning items in/out, then we can expand to the OTA, OTA shed,
MCC, and MCC shed, etc.
3. Lofty goal is to have a notification system (most likely an email bot) that informs 
certain users when an item needs to be maintained, updated, patched, or etc.
4. **[DONE]** Ethan created an Army HR 2062 generator which would build out a HR when you scanned
in items. The HR could then be printed out and used for range clients. This needs to
be spruced up; mainly, the HR shouldn't list every line item one by one, but instead 
utilize the item amount category to save line space.


## Capabilities by DEC 15
1. **[DONE]** Admin rights in order to edit the CSV file with data (python anywhere), create an SOP on how
to do that
2. _(IN-PROG: M Baker)_ Updating the CSV file to include all items with QR codes and that are read into the system
3. "Maintenance" tab that shows the next effective date, highlights the row when it's past
due, then is able to be clicked on so that you can choose 'yes' or 'no' if maint was done, then
it'll update the next effective maintenance date. Turns yellow if you're 30 days out. Maybe if 
you click it as well it'll give you more details on what exctly it's talking about
4. Separate column to track who is the current holder of the object (this also needs to be
clickable to reset it)
5. Update the Info page to have more data on it like the effective maintenance date, who has the
item checked out to them, etc..
5. More filtering buttons/functionality in order to hndle the incrased features (QoS)
6. SOPs on how to do a lot of these tasks i.e. logging into python anywhere, pulling down/editing the CSV
master list, connecting the scanner to your phone, changing scanner settings, adding objects with stickers/codes
and etc, etc...


## Ideas
1. **[DONE]** Convert Ethan's Ruby on Rails application to a Python Flask application
2. **[DONE]** Fix the hosting problem by hosting the Flask application on pythonanywhere with a 
username/password
3. The main inventory page can save a temp csv with all of the items that have been scanned
so that we can have a button that says 'Build 2062' and then it builds it with the saved list
4. **[DONE]** Set the scanner to bluetooth mode, and make a separate page with the barcodes for configuring
the scanner/how to use it (help page)
5. _(IN-PROG)_ Log for when maintenance was completed
6. _(IN-PROG)_ Add a column with the maintenance date or window and then the cell per item can be clicked
to check off that mainentnance has been done (this is what would be logged), color code it
7. **[DONE]** Maybe another column that is like a "last seen" column, it checks to see when the item was
last scanned in, this is the true inventory
8. **[DONE]** Change the location and A-Z/Z-A buttons to be positional buttons to clear up the screen,
as you click them their value changes through a series
9. When you click 2062, a pop-up comes up and asks for a name or company so that it will put it on the
2062 as who the items are being checked out to
10. Idea 9 plays into this but a column with tracking who was the last person to scan out the item or
who is the current item holder. That cell should be clickable and when you click it you get the option
to enter the name of the new holder or reset it to basically say no one is holding it right now.
11. Maybe a help button to explain the different buttons or functionality of the site


## Progress Log
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

**11/14/25**
- Fixed home page return button

**11/17/25 Jeremy**
- Unconfirmed: 2062 generator complete to standard, he noticed the time was slow 20-30s per pdf gen

**11/17/25**
- Made the location and sort button toggle state btns (more concise for smaller screens)
- Created the "lastSeenBtn" which is a toggle on/off btn. The functionality will be that
when it's "on"/selected, it'll populate another column on the table showing the date/time of
when it was last scanned by the scanner.
- Made the same type of button that will show dates when things need to be maintained.
- Helper function in app.py made to read the CSV file based on different options/params.
- Scanning an item now logs the date that it happened in the CSV so that we can keep track
of the last time it was seen.
- Fixed bug where selecting the "Seen" or "Maint" button would reset the location back to
all of them instead of the current location the user had truly selected.

**11/18/25**
- Tried bringing in the 2062 generator but was not compatible with the pre-exisiting code/system,
need to figure out how to fix that and get it operational
- Pulled most recent code from main branch into the python anywhere, no bugs/issues in terms of 
functionality as of now
- Found a docx version of the 2062 so I have a pretty easy generator that runs right now, need to
get the actual formatting and details correct but it works!

**11/19/25**
- Completed the docx version of the 2062 generator that will create a header page and dynamic
pages as the item amount grows.
- Need to make the 2062 where items of the same name get put in one row instead of multiple,
then the serial numbers get listed in desc. and item quant reflects the amount of duplicates
- **NOTE:** We will not be doing docx to PDF convert because the module that runs it requires
microsoft word and pythonanywhere does not have that, so they'll have to be happy with a word doc
- Pythonanywhere is having issues with pulling from main, can't get the code to pull in and load

**11/20/25**
- Python anywhere has the correct code now, the issue was that it had local changes that it wanted
me to merge but that was not the desired behavior. Therefore I ran this command to wipe local changes
and pull purely what was on the github:
```sh
git reset --hard origin/main
git clean -fd
```
- 2062 generator is fully complete with all details and micro functions!

**11/21/25**
- The pythonanywhere site now requires a u/p to sign in, the default is test/test. In order to edit
the CSV file powering the pythonanywhere site you have to use my asmith@rellis.../password so it
is now fully secure
- BUG(FIXED): When the 'Seen' or 'Maint' is selected and you switch location or sort A-Z, the values in those
columns disappear, that is not desired behavior
- PROG: Michael Baker is working on finding the missing items, sticking with QR code, and inputting them
into the secondary CSV which will get appended when he's done
- Help and Info Pages look better, they have updated styling to match the home page
- Headbtns replaced with images instead of text
- 2062 gen btn now asks the user to specify who the document is for, then that person is listed as the recipient
on the doc
- Holder column was made, that tracks who the current holder of the object is. It can be manipulated if
you click on the cell of the objects row