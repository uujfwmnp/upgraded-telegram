import requests
import time, json, sys, os, re

if (sys.platform == "win32"):
	os.system('cls')
else:
	os.system('clear')
print("!! PRESS CONTROL-C TO END THE PROGRAM !!\n")

oldComment = ""
try:
	while True:
		get = requests.get('http://racecontrol.indycar.com/xml/timingscoring.json') # Request data from Indycar
		rawdata = get.text				# Set text of GET reply as a variable
		top = rawdata.replace("jsonCallback(", "")	# Remove top line that is not JSON valid
		bottom = top.replace(");", "")			# Remove bottom line that is not JSON valid
		data = json.loads(bottom)			# Load the formatted string as JSON
# LOCAL DEBUG
#		json_data = open("JSON FILE HERE", "r").read()
#		data = json.loads(json_data)

	#Setup Array Event Variables
		eventFlag  = data['timing_results']['heartbeat']['SessionStatus'] #Cold/In Progress
		session    = data['timing_results']['heartbeat']['SessionType'] #Q/P/R
		newComment = data['timing_results']['heartbeat']['Comment']

		if eventFlag == "COLD":
			print("Event is over.")
			time.sleep(30)
		if newComment == "":
			oldComment = newComment		# Set the new comment to be the old comment
			time.sleep(5)			# Ignore empty comments
		if session == "Q" or session == "P":
			if oldComment != newComment:	# If the new comment does not match the old stored comment. . .
				if re.search('entered the pits.|exited the pits.', newComment):	# Ignore pit in/out comments
					time.sleep(5)
				else:
					commentSTR = "["+time.strftime('%X')+"] " + newComment
					print(commentSTR)	# Print a the timestamp & comment. . .
					oldComment = newComment	# Set the new comment to be the old comment
					time.sleep(5)
			else:					# If the new comment *does* match the old stored comment. . .
				time.sleep(5)			# Keep the while loop running, but do not do anything.
		if session == "R":
			if oldComment != newComment:	# If the new comment does not match the old stored comment. . .
				commentSTR = "["+time.strftime('%X')+"] " + newComment
				print(commentSTR)		# Print a the timestamp & comment. . .
				oldComment = newComment		# Set the new comment to be the old comment
				time.sleep(5)
			else:					# If the new comment *does* match the old stored comment. . .
				time.sleep(5)			# Keep the while loop running, but do not do anything.

except KeyboardInterrupt:
	print("Ending Program\n")
	quit()
pass
