from splinter import Browser
from lxml import etree
#need to make sure that we have this up in el cloud
from account import getWiscUsername
from account import getWiscPassword
from pymongo import MongoClient
import math
import time
import sys
client = MongoClient()
db = client.schedule
#just me for now
#collection = db.hsar

# http://stackoverflow.com/questions/8255929/running-webdriver-chrome-with-selenium/8259152#8259152
browser = Browser('chrome')
scheduleToday = "https://acme.wisc.edu/tools/schedule/agent_view.php"
scheduleBase = "https://acme.wisc.edu/tools/schedule/agent_view.php?week="
loginStub = "&login="

weekStartNumber = 0
MAX_WEEKS = 16
login = "HSAR"



def grabWeek(login, table):
    # figure out how many rows we have to deal with
    times = table.find_by_css(".time")

    range = []
    range.append('date')
    for time in times:
        range.append(time.value)

    sun = []
    mon = []
    tues = []
    wed = []
    thur = []
    fri = []
    sat = []

    #dates = browser.find_by_css('th')
    dates = browser.find_link_by_partial_href('schedule.php?date=')
    #called remain bc pasted from below and i am a bad boy
    for remain in xrange(0,7):
        dateList = []
        for days in dates:
            dateList.append(days['href'])
        date = dateList[remain]
        day = date.split('=')
        finalDay = day[1]
        if remain == 0:
            sun.append(finalDay)
        if remain == 1:
            mon.append(finalDay)
        if(remain == 2):
            tues.append(finalDay)
        if(remain == 3):
            wed.append(finalDay)
        if(remain == 4):
            thur.append(finalDay)
        if(remain == 5):
            fri.append(finalDay)
        if(remain == 6):
            sat.append(finalDay)

    #fixed number of tables slot things. Its 8*range.length
    tableSlots = browser.find_by_css('td')
    totalCells = len(range) * 8
    #i=0 is dead
    for x in xrange(1, totalCells):
        remain = x%8
        index = math.floor(x/len(range))
        #don't need zero, already have that in the range
        try:
            if remain == 1:
                sun.append(tableSlots[x].value)
            if remain == 2:
                mon.append(tableSlots[x].value)
            if(remain == 3):
                tues.append(tableSlots[x].value)
            if(remain == 4):
                wed.append(tableSlots[x].value)
            if(remain == 5):
                thur.append(tableSlots[x].value)
            if(remain == 6):
                fri.append(tableSlots[x].value)
            if(remain == 7):
                sat.append(tableSlots[x].value)
        except:
            break
            browser.quit()
    
    week = []
    #week.append(sun).append(mon).append(tues).append(wed).append(thur).append(fri).append(sat)
    week.append(sun)
    week.append(mon)
    week.append(tues)
    week.append(wed)
    week.append(thur)
    week.append(fri)
    week.append(sat)
    #if update:
    insert(range, week, login)
    #else:
     #   insert(range, week, login)

def insert(range, week, login):
# this way hammers the DB with writes but takes less time for me to make it 
    collection = db.get_collection(login)
    for y in xrange(0,7):
        hoursWorked = 0
        for x in xrange(0, len(range)):
            if x == 0:
                collection.update({
                    range[x] : week[y][x]
                },{ range[x] : week[y][x]}, True )
            else:
                if week[y][x].strip():
                    result = collection.update_one({range[0] : week[y][0]}, {"$set" : {range[x] : week[y][x]}})
                    hoursWorked += 1
                else:
                    print "skipping "+week[y][0]+" time: "+range[x]
        result = collection.update_one({range[0] : week[y][0]}, {"$set" : {"hoursWorked" : hoursWorked/2}})



def getSchedule(login, weeks):
    for weekNumber in xrange(0, weeks):
        scheduleURL = scheduleBase + str(weekNumber) + loginStub + login
        #check to make sure that the something is on the schedule
        browser.visit(scheduleURL)
        if not browser.find_by_id('container').find_by_css('p'):
            table = browser.find_by_id("agent_view_table")
            grabWeek(login, table)


browser.visit(scheduleToday)
browser.find_by_id('j_username').fill(getWiscUsername())
browser.find_by_id('j_password').fill(getWiscPassword())
browser.find_by_css('.btn').click()

#query user for what they want to do

#command line args. 1 populates new schedule with (1, LOGIN)
# 2 updates, takes (2, LOGIN)

input = sys.argv[1]
login = sys.argv[2]

if input is "1":
    print "create new user @"+ login
    update = False
    getSchedule(login.lower, 20)

if input is "2":
    print 'checking for updates with ' + login
    getSchedule(login.lower, 2)



