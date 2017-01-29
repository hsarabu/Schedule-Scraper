Schedule Scrapper


This is a script designed to <em>import</em> schedule data from the DoIT Help Desk schedule. It'll push it into a local MongoDB database.

To use it, put your account credentials into account_SAMPLE.py and rename it to account.py. This is the only way to do it if you want to automate it.

To run, use the command line args. 

<code>
python scheduleScrapper.py [1,2] LOGIN
</code>

Options 1 adds a new user, adds 12 weeks of data. Option 2 simply updates data for exisitng user for the next 2 weeks. Practically, there is little difference between the 2 methods other than how many weeks it looks as it uses the Mongo findOneAndUpdate method