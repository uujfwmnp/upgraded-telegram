import requests
import json
import time, os, sys

def timing():
    #Setup Timing & Scoring
    tsGet = requests.get('https://scoring.imsa.com/scoring_data/RaceResults_JSONP.json')    # Request data from IMSA
    rawdata = tsGet.text                                                                    # Set text of GET reply as a variable
    top = rawdata.replace("jsonpRaceResults(", "")                                          # Remove top line that is not JSON valid
    bottom = top.replace(");", "")                                                          # Remove bottom line that is not JSON valid
    rawTS = json.loads(bottom)                                                              # Load the formatted string as JSON
    sessionGet = requests.get('https://scoring.imsa.com/scoring_data/SessionInfo_JSONP.json')
    rawdata = sessionGet.text
    top = rawdata.replace("jsonpSessionInfo(", "")
    bottom = top.replace(");", "")
    session = json.loads(bottom)

# LOCAL DEBUG
#    json_data = open("JSON FILE HERE", "r").read()
#    data = json.loads(json_data)

    #Setup Array Event Variables
    global eventName, eventFlag, eventTime, eventLeft, drivers

    eventName    = "Event Name:    " + session['T'] + " " + session['S']
    eventFlag    = "Status:        " + session['F']
    eventTime    = "Elapsed Time:  " + session['TT']
    eventLeft    = "Time Left:     " + session['TR']

    #Setup Array Driver Variables to purge junk data from the raw feed
    driversRaw = rawTS['B']
    drivers = []
    for i in range(0, len(driversRaw)):
        if (driversRaw[i]['C'] != ""):      # If the Class field is blank, this isn't a real driver.
            drivers.append (driversRaw[i])

    #Start the show!
def lapSpacing(length):
    switcher = {
        5: "               ",
        6: "              ",
        7: "             ",
        8: "            "
    }
    result = switcher.get(length, "  ")
    return result
def gapSpacing(length):
    switcher = {
        5: "        ",
        6: "       ",
        7: "      ",
        8: "     ",
        9: "  "
    }
    result = switcher.get(length, "  ")
    return result

def event():
    try:
        while True:
            timing()
            #Pretty Stuff Here
            if (sys.platform == "win32"):
                os.system('cls')
            else:
                os.system('clear')
            print("!! PRESS CONTROL-C TO END THE PROGRAM !!")
            print(eventName,"\n",
              eventFlag,"\n",
              eventTime,"\n",
              eventLeft,"\n",sep='')

            print ("Overall: ", "Class: ", "Driver: \t\t\t", "Num:\t", "Race Leader: ", "Class Leader:", "Gap to Class:" , "Last Lap:    ", "Car:")
            
            # Driver Variable Array
            for i in range(0, len(drivers)):
                overallPosition = drivers[i]['A']
#                classPosition = drivers[i]['PIC']
                carClass = drivers[i]['C']
                nameLen = len(drivers[i]['F'])
                if (nameLen >= 20):
                    driverName = drivers[i]['F']+" "
                elif (nameLen >= 16 and nameLen <= 19):
                    driverName = drivers[i]['F']+"\t"
                elif (nameLen == 15 or nameLen == 14):
                    driverName = drivers[i]['F']+"\t"
                elif (nameLen == 12 or nameLen == 13):
                    driverName = drivers[i]['F']+"\t\t"
                else:
                    driverName = drivers[i]['F'] + "\t\t"
                carNum = drivers[i]['N']
                carManuf = drivers[i]['V']
                bestLapTime = drivers[i]['BL']  + lapSpacing(len(drivers[i]['BL']))
                lastLapTime = drivers[i]['LL']
                diff2OLead  = drivers[i]['D']   + gapSpacing(len(drivers[i]['D']))
                diff2CLead  = drivers[i]['DIC'] + gapSpacing(len(drivers[i]['DIC']))
                classGap    = drivers[i]['GIC'] + gapSpacing(len(drivers[i]['GIC']))

                print (overallPosition, "\t ", carClass, "\t ", driverName, "\t", carNum, "\t", diff2OLead, diff2CLead, classGap, lastLapTime, "\t", carManuf)

            time.sleep(10)
            print("Refreshing. . .")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Ending Program\n")
        quit()
    pass

# Start the whole thing
event()