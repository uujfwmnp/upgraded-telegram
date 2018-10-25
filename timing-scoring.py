import requests
import json
import time, os, sys

def rsQual(qSession):
    switcher = {
        "Q1.I": "Session:       Qualifying Round 1 Group 1",
        "Q2.I": "Session:       Qualifying Round 1 Group 2",
        "Q3.I": "Session:       Qualifying Round 2 (Fast 12)",
        "Q4.I": "Session:       Qualifying Round 2 (Fast 6)"
    }
    result = switcher.get(qSession, "Session:       Qualifying")
    return result
def tires(qSession):
    switcher = {
        "P": "Black  ",
        "W": "Wet    ",
        "A": "Red    "
    }
    result = switcher.get(qSession, "Unknown")
    return result

def timing():
    #Setup Timing & Scoring
    get = requests.get('http://racecontrol.indycar.com/xml/timingscoring.json') # Request data from Indycar
    rawdata = get.text                                                          # Set text of GET reply as a variable
    top = rawdata.replace("jsonCallback(", "")                                  # Remove top line that is not JSON valid
    bottom = top.replace(");", "")                                              # Remove bottom line that is not JSON valid
    data = json.loads(bottom)                                                   # Load the formatted string as JSON
# LOCAL DEBUG
#    json_data = open("JSON FILE HERE", "r").read()
#    data = json.loads(json_data)

    #Setup Array Event Variables
    global event, eventName, eventTrack, eventFlag, eventComment, eventType, eventTime, eventSession, eventLaps, drivers

    event = data['timing_results']['heartbeat']
    eventName    = "Event Name:    " + event['eventName']
    eventTrack   = "Track Name:    " + event['trackName']
    eventFlag    = "Status:        " + event['currentFlag']
    eventComment = "Comment:       " + event['Comment']

    if (event['trackType'] == "O" or event['trackType'] == "I"):
        eventType = "Oval"
    elif (event['trackType'] == "RC"):
        eventType = "Road Course"
    else:
        eventType = "Street Course"

    if ('overallTimeToGo' not in event.keys()):
        eventTime = "Elapsed Time:  " + event['elapsedTime']     # Qual/Race will show elapsed time
    else:
        eventTime = "Time Left:     " + event['overallTimeToGo'] # Practice will show time remaining. This may also occur during timed races, not sure

    #Setup Array Driver Variables
    drivers = data['timing_results']['Item']

    #Start the show!
    if (event['SessionType'] == "Q"):
        if (event['trackType'] == "RC" or event['trackType'] == "SC"):
            eventSession = rsQual(event['preamble'])
        else:
            eventSession = "Session:       Qualifying"     # This handles qualifying sessions for oval tracks
    elif (event['SessionType'] == "P"):
        eventSession = "Session:       Practice"
    else:
        eventSession = "Session:       Race"
        if ('totalLaps' not in event.keys()):
            eventLaps = "Lap:           " + event['lapNumber']
        else:
            eventLaps = "Lap:           " + event['lapNumber'] + " of " + event['totalLaps']

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
              eventTrack,"\n",
              eventSession,"\n",
              eventFlag,"\n",
              eventTime,"\n",
              eventComment,"\n",sep='')
            passTotal = 0
            if (event['SessionType'] == "R"):
                print(eventLaps)
                for i in range(0, len(drivers)):
                    passCount = drivers[i].get('Passes', 0)
                    passTotal += int(passCount)
                print("Total Passes: ",passTotal,"\n")
                if (event['trackType'] == "RC" or event['trackType'] == "SC"):
                    print ("Position: ", "Driver: \t\t", "Car:\t", "Last Lap:  ", "Diff to Lead: ", "Gap Ahead: ", "Tire:  ", "P2P:  ", "Status:")
                else: #if (eventType == "Oval"):
                    print ("Position: ", "Driver: \t\t", "Car:\t", "Last Lap:  ", "Diff to Lead: ", "Gap Ahead: ", "Status:")

            elif (event['SessionType'] == "Q" or event['SessionType'] == "P"):
                if (event['trackType'] == "RC" or event['trackType'] == "SC"):
                    print ("Position: ", "Driver: \t\t", "Car:\t", "Last Lap:  ", "Best Lap:  ", "Tire:  ", "Status:")                    
                else: #if (eventType == "Oval"):
                    print ("Position: ", "Driver: \t\t", "Car:\t", "Last Lap:  ", "Best Lap:  ", "Status:")

            # Driver Variable Array
            for i in range(0, len(drivers)):
                position = drivers[i]['rank']
                if (len(drivers[i]['lastName']) >= 12):
                    driverName = drivers[i]['lastName'] + "\t"
                elif (len(drivers[i]['lastName']) <= 4):
                    driverName = drivers[i]['lastName'] + "\t\t\t"
                else:
                    driverName = drivers[i]['lastName'] + "\t\t"
                carNum = drivers[i]['no']
                team = drivers[i]['team']
                #Best Lap Time + Spacing
                if (len(drivers[i]['bestLapTime']) == 7):
                    bestLapTime = drivers[i]['bestLapTime'] + "    "
                elif (len(drivers[i]['bestLapTime']) == 10):
                    bestLapTime = drivers[i]['bestLapTime'] + " "
                else:
                    bestLapTime = drivers[i]['bestLapTime'] + "  "
                #Last Lap Time + Spacing
                if (len(drivers[i]['lastLapTime']) == 7):
                    lastLapTime = drivers[i]['lastLapTime'] + "    "
                elif (len(drivers[i]['lastLapTime']) == 10):
                    lastLapTime = drivers[i]['lastLapTime'] + " "
                else:
                    lastLapTime = drivers[i]['lastLapTime'] + "  "
                #Distance to Leader Time + Spacing
                if (len(drivers[i]['diff']) == 6):
                    diff2Lead = drivers[i]['diff'] + "        "
                elif (len(drivers[i]['diff']) == 7):
                    diff2Lead = drivers[i]['diff'] + "       "
                elif (len(drivers[i]['diff']) == 9):
                    diff2Lead = drivers[i]['diff'] + "     "
                #Position Gap Time + Spacing
                if (len(drivers[i]['gap']) == 6):
                    gapAhead = drivers[i]['gap'] + "     "
                elif (len(drivers[i]['gap']) == 7):
                    gapAhead = drivers[i]['gap'] + "    "
                elif (len(drivers[i]['gap']) == 9):
                    gapAhead = drivers[i]['gap'] + "  "
                #Overtake + Spacing
                if (len(drivers[i]['OverTake_Remain']) == 1):
                    p2pRemain = drivers[i]['OverTake_Remain']+"     "
                elif (len(drivers[i]['OverTake_Remain']) == 2):
                    p2pRemain = drivers[i]['OverTake_Remain']+"    "
                else:
                    p2pRemain = drivers[i]['OverTake_Remain']+"   "
                driverTire = tires(drivers[i]['Tire'])
#Oval Race
                if (event['SessionType'] == "R" and eventType == "Oval"):
                    print (position, "\t  ", driverName, carNum, "\t", lastLapTime, diff2Lead, gapAhead, drivers[i]['status'])
#Oval Q/P
                elif (eventType == "Oval" and (event['SessionType'] == "Q" or event['SessionType'] == "P")):
                    print (position, "\t  ", driverName, carNum, "\t", lastLapTime, bestLapTime, drivers[i]['status'])
#RC/SC Race
                elif (event['SessionType'] == "R" and eventType != "Oval"): # This should cover all road/street course races
                    print (position, "\t  ", driverName, carNum, "\t", lastLapTime, diff2Lead, gapAhead, driverTire, p2pRemain, drivers[i]['status'])
#RC/SC Q
                elif (eventType != "Oval" and event['SessionType'] == "Q"): # This should cover qual for all road/street courses
                    if (position == "7" and event['preamble'] == "*.I"):
                        print ("--- TRANSFER CUT OFF ---")
                        print (position, "\t  ", driverName, carNum, "\t", lastLapTime, bestLapTime, driverTire, drivers[i]['status'])
                    else:
                        print (position, "\t  ", driverName, carNum, "\t", lastLapTime, bestLapTime, driverTire, drivers[i]['status'])
#RC/SC P
                elif (eventType != "Oval" and event['SessionType'] == "P"):
                    print (position, "\t  ", driverName, carNum, "\t", lastLapTime, bestLapTime, driverTire, drivers[i]['status'])
                        
            time.sleep(10)
            print("Refreshing. . .")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Ending Program\n")
        quit()
    pass

# Start the whole thing
event()
