import requests
import json
import time, os, sys, re

def timing():
	#Setup Timing & Scoring
	get = requests.get('http://racecontrol.indycar.com/xml/timingscoring.json') # Request data from Indycar
	rawdata = get.text															# Set text of GET reply as a variable
	top = rawdata.replace("jsonCallback(", "")									# Remove top line that is not JSON valid
	bottom = top.replace(");", "")												# Remove bottom line that is not JSON valid
	data = json.loads(bottom)													# Load the formatted string as JSON
# LOCAL DEBUG
#	json_data = open("JSON FILE HERE", "r").read()
#	data = json.loads(json_data)

	#Setup Array Event Variables
	global event, eventName, eventTrack, eventFlag, eventComment, eventType, eventTime, eventSession, eventLaps, drivers

	event = data['timing_results']['heartbeat']
	eventName    = "Event Name:    " + event['eventName']
	eventTrack   = "Track Name:    " + event['trackName']
	eventFlag    = "Status:        " + event['currentFlag']
	eventComment = "Comment:       " + event['Comment']

	if (event['trackType'] == "O"):
		eventType = "Oval"
	if (event['trackType'] == "RC"):
		eventType = "Road Course"
	if (event['trackType'] == "SC"):
		eventType = "Street Course"

	if ('overallTimeToGo' not in event.keys()):
		eventTime = "Elapsed Time:  " + event['elapsedTime']	# Qual/Race will show elapsed time
	else:
		eventTime = "Time Left:     " + event['overallTimeToGo']	# Practice will show time remaining. This may also occur during timed races, not sure

	#Setup Array Driver Variables
	drivers = data['timing_results']['Item']

	#Start the show!
	if (event['SessionType'] == "Q"):
		if (event['trackType'] == "RC" or event['trackType'] == "SC"):
			if (event['preamble'] == "Q1.I"):
				eventSession = "Session:       Qualifying Round 1 Group 1"
			if (event['preamble'] == "Q2.I"):
				eventSession = "Session:       Qualifying Round 1 Group 2"
			if (event['preamble'] == "Q3.I"):
				eventSession = "Session:       Qualifying Round 2 (Fast 12)"
			if (event['preamble'] == "Q4.I"):
				eventSession = "Session:       Qualifying Round 3 (Fast 6)"
			if (re.search('Q*.F|Q*.S|Q*.P',event['preamble'])):
				eventSession = "Session:       Qualifying" # This handles road/street qualifying sessions that do not follow the Qx.I format, such as MRTI events
		else:
			eventSession = "Session:       Qualifying"	# This handles qualifying sessions for oval tracks
	if (event['SessionType'] == "P"):
		eventSession = "Session:       Practice"
	if (event['SessionType'] == "R"):
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
					print ("Position: ", "Driver: \t\t", "Car:\t", "Last Lap:\t", "Diff to Lead:\t", "Gap Ahead:\t", "Tire:   ", "P2P:  ", "Status:")
				else: #if (eventType == "Oval"):
					print ("Position: ", "Driver: \t\t", "Car:\t", "Last Lap:  ", "Diff to Lead: ", "Gap Ahead: ", "Status:")

			if (event['SessionType'] == "Q" or event['SessionType'] == "P"):
				if (event['trackType'] == "RC" or event['trackType'] == "SC"):
					print ("Position: ", "Driver: \t\t", "Car:\t", "Last Lap: \t", "Best Lap: \t", "Tire: \t ", "Status:")					
				else: #if (eventType == "Oval"):
					print ("Position: ", "Driver: \t\t", "Car:\t", "Last Lap: ", "Best Lap: \t", "Status:")

			# Driver Variable Array
			for i in range(0, len(drivers)):
				position = drivers[i]['rank']
				driverName = drivers[i]['lastName']
				carNum = drivers[i]['no']
				team = drivers[i]['team']
				bestLapTime = drivers[i]['bestLapTime']
				lastLapTime = drivers[i]['lastLapTime']
				diff2Lead = drivers[i]['diff']
				gapAhead = drivers[i]['gap']
				if (len(drivers[i]['OverTake_Remain']) == 1):
					p2pRemain = drivers[i]['OverTake_Remain']+"     "
				if (len(drivers[i]['OverTake_Remain']) == 2):
					p2pRemain = drivers[i]['OverTake_Remain']+"    "
				if (len(drivers[i]['OverTake_Remain']) == 3):
					p2pRemain = drivers[i]['OverTake_Remain']+"   "
				if (drivers[i]['Tire'] == "P"):
					driverTire = "Black   "
				if (drivers[i]['Tire'] == "W"):
					driverTire = "Wet\t"
				if (drivers[i]['Tire'] == "A"):
					driverTire = "Red     "
				if (drivers[i]['Tire'] not in ("P","W","A")):	#Covers tire choices from alternate series, or if the tire choice is blank.
					driverTire = "Unknown "
#Oval Race
				if (event['SessionType'] == "R" and eventType == "Oval"):
					if (len(drivers[i]['lastName']) >= 12):
						print (position, "\t  ", driverName, "\t", carNum, "\t", lastLapTime, "   ", diff2Lead, "       ",  gapAhead, "    ", drivers[i]['status'])
					if (len(drivers[i]['lastName']) <= 3):
						print (position, "\t  ", driverName, "\t\t\t", carNum, "\t", lastLapTime, "   ", diff2Lead, "       ",  gapAhead, "    ", drivers[i]['status'])
					else:
						print (position, "\t  ", driverName, "\t\t", carNum, "\t", lastLapTime, "   ", diff2Lead, "       ",  gapAhead, "    ", drivers[i]['status'])
#RC/SC Race
				if (event['SessionType'] == "R" and eventType != "Oval"): # This should cover all road/street course races
					if (len(drivers[i]['lastName']) >= 12):
						print (position, "\t  ", driverName, "\t", carNum, "\t", lastLapTime, "\t", diff2Lead, "\t",  gapAhead, "\t", driverTire, p2pRemain, drivers[i]['status'])
					if (len(drivers[i]['lastName']) <= 3):
						print (position, "\t  ", driverName, "\t\t\t", carNum, "\t", lastLapTime, "\t", diff2Lead, "\t",  gapAhead, "\t", driverTire, p2pRemain, drivers[i]['status'])
					else:
						print (position, "\t  ", driverName, "\t\t", carNum, "\t", lastLapTime, "\t", diff2Lead, "\t",  gapAhead, "\t", driverTire, p2pRemain, drivers[i]['status'])
#Oval Q/P
				if (eventType == "Oval" and (event['SessionType'] == "Q" or event['SessionType'] == "P")):
					if (len(drivers[i]['lastName']) >= 12):
						print (position, "\t  ", driverName, "\t", carNum, "\t", lastLapTime, "  ", bestLapTime, "\t", drivers[i]['status'])
					if (len(drivers[i]['lastName']) <= 3):
						print (position, "\t  ", driverName, "\t\t\t", carNum, "\t", lastLapTime, "\t", bestLapTime, "\t", driverTire, drivers[i]['status'])
					else:
						print (position, "\t  ", driverName, "\t\t", carNum, "\t", lastLapTime, "  ", bestLapTime, "\t", drivers[i]['status'])
#RC/SC Q
				if (eventType != "Oval" and event['SessionType'] == "Q"): # This should cover qual for all road/street courses
					if (len(drivers[i]['lastName']) >= 12):
						if (position == "7"):
							print ("--- TRANSFER CUT OFF ---")
							print (position, "\t  ", driverName, "\t", carNum, "\t", lastLapTime, "\t", bestLapTime, "\t", driverTire, drivers[i]['status'])
						else:
							print (position, "\t  ", driverName, "\t\t", carNum, "\t", lastLapTime, "\t", bestLapTime, "\t", driverTire, drivers[i]['status'])
					if (len(drivers[i]['lastName']) <= 3):
						if (position == "7"):
							print ("--- TRANSFER CUT OFF ---")
							print (position, "\t  ", driverName, "\t\t\t", carNum, "\t", lastLapTime, "\t", bestLapTime, "\t", driverTire, drivers[i]['status'])
						else:
							print (position, "\t  ", driverName, "\t\t\t", carNum, "\t", lastLapTime, "\t", bestLapTime, "\t", driverTire, drivers[i]['status'])
					else:
						if (position == "7"):
							print ("--- TRANSFER CUT OFF ---")
							print (position, "\t  ", driverName, "\t\t", carNum, "\t", lastLapTime, "\t", bestLapTime, "\t", driverTire, drivers[i]['status'])
						else:
							print (position, "\t  ", driverName, "\t\t", carNum, "\t", lastLapTime, "\t", bestLapTime, "\t", driverTire, drivers[i]['status'])
#RC/SC P
				if (eventType != "Oval" and event['SessionType'] == "P"):
					if (len(drivers[i]['lastName']) >= 12):
						print (position, "\t  ", driverName, "\t", carNum, "\t", lastLapTime, "\t", bestLapTime, "\t", driverTire, drivers[i]['status'])
					if (len(drivers[i]['lastName']) <= 3):
						print (position, "\t  ", driverName, "\t\t\t", carNum, "\t", lastLapTime, "\t", bestLapTime, "\t", driverTire, drivers[i]['status'])
					else:
						print (position, "\t  ", driverName, "\t\t", carNum, "\t", lastLapTime, "\t", bestLapTime, "\t", driverTire, drivers[i]['status'])

			time.sleep(10)
			print("Refreshing. . .")
			time.sleep(1)
	except KeyboardInterrupt:
		print("Ending Program\n")
		quit()
	pass

# Start the whole thing
event()