import requests
import json
import re, time, os, sys

def timing():
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
    elif (event['trackType'] == "SC"):
        eventType = "Street Course"
    else:
        eventType = "Race Course"

    if ('overallTimeToGo' not in event.keys()):
        eventTime = "Elapsed Time:  " + event['elapsedTime']     # Qual/Race will show elapsed time
    else:
        eventTime = "Time Left:     " + event['overallTimeToGo'] # Practice will show time remaining. This may also occur during timed races, not sure

    #Setup Array Driver Variables
    drivers = data['timing_results']['Item']

    #Start the show!
    if (event['SessionType'] == "Q"):
        if (eventType != "Oval"): # Road/Street
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

def rsQual(qSession):
    switcher = {
        "Q1.I": "Session:       Qualifying Round 1 Group 1",
        "Q2.I": "Session:       Qualifying Round 1 Group 2",
        "Q3.I": "Session:       Qualifying Round 2 (Fast 12)",
        "Q4.I": "Session:       Qualifying Round 2 (Fast 6)"
    }
    result = switcher.get(qSession, "Session:       Qualifying")
    return result
def tires(tireType):
    switcher = {
        "P": "Black  ",
        "W": "Wet    ",
        "A": "Red    "
    }
    result = switcher.get(tireType, "Unknown")
    return result
def lapSpacing(length):
    switcher = {
        6: "     ",
        7: "    ",
        10: " "
    }
    result = switcher.get(length, "  ")
    return result
def gapSpacing(length):
    switcher = {
        5: "      ",
        6: "     ",
        7: "    ",
        8: "   ",
        9: "  ",
        10:" ",
    }
    result = switcher.get(length, "  ")
    return result
def p2pSpacing(length):
    switcher = {
        1: "     ",
        2: "    "
    }
    result = switcher.get(length, "   ")
    return result

try:
    while True:
        get = requests.get('https://indycarsso.blob.core.windows.net/racecontrol/timingscoring.json',timeout=10) # Request data from Indycar
        if (get.status_code == 404):    # If the JSON file is missing
            exit("T&S site reports a 404, closing script")
        else:
            rawdata = get.text                          # Set text of GET reply as a variable
            top = rawdata.replace("jsonCallback(", "")  # Remove top line that is not JSON valid
            bottom = top.replace(");", "")              # Remove bottom line that is not JSON valid
            data = json.loads(bottom)                   # Load the formatted string as JSON
        # LOCAL DEBUG
        #json_data = open("JSON-I-Practice.txt", "r").read() # LOCAL DEBUG
        #data = json.loads(json_data)                        # LOCAL DEBUG
        timing(data)
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
            if (eventType != "Oval"): # Road/Street
                print ("Position: ", "Driver: \t\t", "Car:\t", "Last Lap:  ", "Lead Gap:  ", "Gap Ahead: ", "Tire:  ", "P2P:  ", "Status:")
            else: #if (eventType == "Oval"):
                print ("Position: ", "Driver: \t\t", "Car:\t", "Last Lap:  ", "Lead Gap:  ", "Gap Ahead: ", "Status:")
        else:
            if (eventType != "Oval"): # Road/Street
                print ("Position: ", "Driver: \t\t", "Car:\t", "Last Lap:  ", "Best Lap:  ", "Tire:  ", "Status:")
            elif (event['trackType'] == "I" and  event['SessionType'] == "P"):
                print ("Position: ", "Driver: \t\t", "Car:\t", "Last Lap:  ", "Best Lap:  ", "Last Speed:", "Best Speed:", "Avg Speed: ", "NT Lap:    ", "NT Speed:  ", "NT Rank:", "Status:")
            else: #if (eventType == "Oval"):
                print ("Position: ", "Driver: \t\t", "Car:\t", "Last Lap:  ", "Best Lap:  ", "Status:")

        # Driver Variable Array
        for i in range(0, len(drivers)):
            position = drivers[i]['rank']
            if (len(drivers[i]['lastName']) >= 13):
                driverName = drivers[i]['lastName'] + "\t"
            if (len(drivers[i]['lastName']) >= 12):
                driverName = drivers[i]['lastName'] + " \t"
            elif (len(drivers[i]['lastName']) <= 4):
                driverName = drivers[i]['lastName'] + "\t\t\t"
            else:
                driverName = drivers[i]['lastName'] + "\t\t"
            carNum = drivers[i]['no']
            team = drivers[i]['team']
            bestLapTime = drivers[i]['bestLapTime'] + lapSpacing(len(drivers[i]['bestLapTime']))
            lastLapTime = drivers[i]['lastLapTime'] + lapSpacing(len(drivers[i]['lastLapTime']))
            diff2Lead = drivers[i]['diff'] + gapSpacing(len(drivers[i]['diff']))
            gapAhead = drivers[i]['gap'] + gapSpacing(len(drivers[i]['gap']))
            p2pRemain = drivers[i]['OverTake_Remain'] + p2pSpacing(len(drivers[i]['OverTake_Remain']))
            driverTire = tires(drivers[i]['Tire'])
            if (event['trackType'] == "I"):
                if ('AverageSpeed' not in drivers[i].keys()):
                    avgSpeed   = "00.0000" + gapSpacing(len("00.0000"))
                else:
                    avgSpeed   = drivers[i]['AverageSpeed'] + gapSpacing(len(drivers[i]['AverageSpeed']))
                if ('BestSpeed' not in drivers[i].keys()):
                    bestSpeed   = "00.0000" + gapSpacing(len("00.0000"))
                else:
                    bestSpeed   = drivers[i]['BestSpeed'] + gapSpacing(len(drivers[i]['BestSpeed']))
                if ('LastSpeed' not in drivers[i].keys()):
                    lastSpeed   = "00.0000" + gapSpacing(len("00.0000"))
                else:
                    lastSpeed   = drivers[i]['LastSpeed'] + gapSpacing(len(drivers[i]['LastSpeed']))
                if ('NTBestSpeed' not in drivers[i].keys()):
                    ntBestSpeed   = "000.000" + gapSpacing(len("-0.0001"))
                else:
                    ntBestSpeed   = drivers[i]['NTBestSpeed'] + gapSpacing(len(drivers[i]['NTBestSpeed']))
                if ('NTRank' not in drivers[i].keys()):
                    ntRank   = "0\t     "
                else:
                    ntRank     = drivers[i]['NTRank'] + "\t     "
                ntBestTime = drivers[i]['NTBestTime'] + gapSpacing(len(drivers[i]['NTBestTime']))
#Oval
            if (eventType == "Oval"):
                if (event['SessionType'] == "R"):
                    print (position, "\t  ", driverName, carNum, "\t", lastLapTime, diff2Lead, gapAhead, drivers[i]['status'])
                elif(event['trackType'] == "I" and event['SessionType'] == "P"):
                    print (position, "\t  ", driverName, carNum, "\t", lastLapTime, bestLapTime, lastSpeed, bestSpeed, avgSpeed, ntBestTime, ntBestSpeed, ntRank, drivers[i]['status'])
                elif(event['trackType'] == "I" and event['SessionType'] == "Q"):
                    print (position, "\t  ", driverName, carNum, "\t", lastLapTime, bestLapTime, avgSpeed, drivers[i]['status'])
                else: #(event['SessionType'] == "Q" or event['SessionType'] == "P")):
                    print (position, "\t  ", driverName, carNum, "\t", lastLapTime, bestLapTime, drivers[i]['status'])
#Road Course/Street Course
            else:
                if (event['SessionType'] == "R"): # This should cover all road/street course races
                    print (position, "\t  ", driverName, carNum, "\t", lastLapTime, diff2Lead, gapAhead, driverTire, p2pRemain, drivers[i]['status'])
                elif (event['SessionType'] == "Q"): # This should cover qual for all road/street courses
                    if (position == "7" and re.search(".I",event['preamble'])):
                        print ("--- TRANSFER CUT OFF ---")
                        print (position, "\t  ", driverName, carNum, "\t", lastLapTime, bestLapTime, driverTire, drivers[i]['status'])
                    else:
                        print (position, "\t  ", driverName, carNum, "\t", lastLapTime, bestLapTime, driverTire, drivers[i]['status'])
                else: #(event['SessionType'] == "P"):
                    print (position, "\t  ", driverName, carNum, "\t", lastLapTime, bestLapTime, driverTire, drivers[i]['status'])

        time.sleep(10)
        print("Refreshing. . .")
        time.sleep(1)
except KeyboardInterrupt:
    print("Ending Program\n")
    quit()
pass
