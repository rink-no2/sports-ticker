import json
import requests
import datetime
from datetime import timedelta
from tkinter import *
import time

### This function is for MLB and give out status
### and bases status

def mlbStatus(outs, base_one, base_two, base_thr):
    xstatus = ""
    if outs == 1:
        xstatus = str(outs) + " out: "
    else:
        xstatus = str(outs) + " outs: "
    if not base_one and not base_two and not base_thr:
        xstatus = xstatus + "Bases Empty"
    if base_one and not base_two and not base_thr:
        xstatus = xstatus + "Runner on 1st"
    if not base_one and base_two and not base_thr:
        xstatus = xstatus + "Runner on 2nd"
    if not base_one and not base_two and base_thr:
        xstatus = xstatus + "Runner on 3rd"
    if base_one and base_two and not base_thr:
        xstatus = xstatus + "Runners on 1st and 2nd"
    if base_one and not base_two and base_thr:
        xstatus = xstatus + "Runners on 1st and 3rd"
    if not base_one and base_two and base_thr:
        xstatus = xstatus + "Runners on 2nd and 3rd"
    if base_one and base_two and base_thr:
        xstatus = xstatus + "Bases Loaded"
    return xstatus

### A Dictionary for cities with two teams in a league
### Changed to an external file. Better to manage that way.

specialDict = eval(open("DupNicknames.txt").read())

### URL/APIs to go grab JSON endpoints

url = ["http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
       ,"http://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard"
       ,"http://site.api.espn.com/apis/site/v2/sports/soccer/usa.1/scoreboard"
       ,"http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
      ]

### Set up initial window

root = Tk()
mytext = Label(root,
               text='Sports\nTicker',
               width=25,
               height=10,
               bg="orange",
               font=("Times New Roman",64))
mytext.pack()
root.update()
time.sleep(2)

### Main Loop

for sport in url:

### If it's before 11am local time, print yesterday's score
### After 11am, print today's upcoming games/scores
    
    tod = datetime.datetime.now()
    yest = datetime.datetime.now() - timedelta(days=1)
    if int(tod.strftime('%H')) < 11:
        sport = sport + '?dates=' + yest.strftime('%Y%m%d')
    else:
        sport = sport + '?dates=' + tod.strftime('%Y%m%d')

### Get the JSON and read it in 

    response = requests.get(sport)
    todos = json.loads(response.text)
    
    league = todos["leagues"][0]["abbreviation"]   #read in the league
    for i in range(0,len(todos["events"])):
        away_team = todos["events"][i]["competitions"][0]["competitors"][1]["team"]["location"]
        away_nick = todos["events"][i]["competitions"][0]["competitors"][1]["team"]["name"]
        away_score = todos["events"][i]["competitions"][0]["competitors"][1]["score"]
        home_team = todos["events"][i]["competitions"][0]["competitors"][0]["team"]["location"]
        home_nick = todos["events"][i]["competitions"][0]["competitors"][0]["team"]["name"]
        home_score = todos["events"][i]["competitions"][0]["competitors"][0]["score"]
        status = todos["events"][i]["status"]["type"]["detail"]

###  Gets the in-inning status for MLB. Passes to the function above
        
        if "Top" in status or "Bottom" in status:
            outs = todos["events"][i]["competitions"][0]["situation"]["outs"]
            base_one = todos["events"][i]["competitions"][0]["situation"]["onFirst"]
            base_two = todos["events"][i]["competitions"][0]["situation"]["onSecond"]
            base_thr = todos["events"][i]["competitions"][0]["situation"]["onThird"]
            xStat = mlbStatus(outs, base_one, base_two, base_thr)

###  Check the dictionary for two-team per sport cities
            
        if league+away_nick in specialDict:
            away_team = specialDict[league+away_nick]
        if league+home_nick in specialDict:
            home_team = specialDict[league+home_nick]

###  Print score
###  If the status contains an "at" game has yet to start
###  First elif deals with MLB and prints in-inning status
            
        if " at " in status:
            status = status[status.find(" at ")+4:]
            pstring = league+"\n" + away_team + "\n" + "at " + \
                      home_team + "\n" + status
        elif "Top" in status or "Bottom" in status:
            pstring = league+"\n" + \
                      away_team + "  " + away_score + "\n" + \
                      home_team + "  " + home_score + "\n" + \
                      status + "\n" + xStat
        else:
            pstring = league+"\n" + \
                      away_team + "  " + away_score + "\n" + \
                      home_team + "  " + home_score + "\n" + \
                      status
        mytext.config(text=pstring
                      ,bg="#D41244")
        mytext.pack()
        root.update()
        time.sleep(2)
    
