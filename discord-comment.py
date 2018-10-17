import discord
import asyncio
import aiohttp
import requests
import time, json, os, sys, re

TOKEN = 'DISCORD-BOT-TOKEN'
client = discord.Client()

def timing():
	get = requests.get('http://racecontrol.indycar.com/xml/timingscoring.json') # Request data from Indycar
	rawdata = get.text															# Set text of GET reply as a variable
	top = rawdata.replace("jsonCallback(", "")									# Remove top line that is not JSON valid
	bottom = top.replace(");", "")												# Remove bottom line that is not JSON valid
	data = json.loads(bottom)													# Load the formatted string as JSON
# LOCAL DEBUG
#	json_data = open("JSON FILE HERE", "r").read()
#	data = json.loads(json_data) 

#Setup Array Event Variables
	global eventFlag, session, newComment
	eventFlag  = data['timing_results']['heartbeat']['SessionStatus'] #Cold/In Progress
	session    = data['timing_results']['heartbeat']['SessionType'] #Q/P/R
	newComment = data['timing_results']['heartbeat']['Comment']

@client.event
async def indycar_comments():
	await client.wait_until_ready()
	print("Current servers:")
	for server in client.servers:
		print(server.name)
	channel = discord.utils.get(client.get_all_channels(), name='CHANNEL-NAME-HERE')
	oldComment = ""
	commentLST = []
	try:
		while True:
			timing()
			if eventFlag == "COLD":
				print("Event has not started, or is finished.")	# Local notice only
				time.sleep(30)
			if session == "Q" or session == "P":
				if oldComment != newComment:	# If the new comment does not match the old stored comment. . .
					if re.search('entered the pits.|exited the pits.', newComment):	# Ignore pit in/out comments during qual/practice
						time.sleep(10)
					else:
						if len(commentLST) < 5:
							listCount = len(commentLST)
							commentLST.append("["+time.strftime('%X')+"] " + newComment)
							oldComment = newComment				# Set the new comment to be the old comment
							print(listCount)
							time.sleep(10)						# 10 second wait before restarting loop
						elif len(commentLST) == 5:
							commentSTR = "\n".join(commentLST)
							print("Printing Comments\n")		# Local Print the comment string
							msg = "```" + commentSTR + "```"
							await client.send_message(channel, msg)	# Send the comment to the Discord channel
							oldComment = newComment				# Set the new comment to be the old comment
							commentSTR = ""						# Reset the comment string
							commentLST = []						# Reset the comment list
							time.sleep(10)				# 10 second before restarting loop
				else:							# If the new comment *does* match the old stored comment. . .
					count = 0
					while(count < 5):	# Start a while timer
						print("loop number: %d" % (count + 1))
						count += 1		# Increment the timer each time it runs
						timing()		# Poll for new comments
						if oldComment != newComment:	# If the new comment does not match the old stored comment. . .
							if re.search('entered the pits.|exited the pits.', newComment):	# Ignore pit in/out comments during qual/practice
								time.sleep(2)
								break						# Stop the timer, we don't care about pit in/out
							else:
								print("New Data, Break\n")
								time.sleep(2)
								break						# Stop the timer, we have a new comment
						if count == 5 and len(commentLST) in range (1,4):	# If we hit the time limit and have less than 5 new comments
							print("5s & <= 4 Timeout!",commentLST)	# Local Print the comment list
							commentSTR = "\n".join(commentLST)
							msg = "```" + commentSTR + "```"
							time.sleep(2)
							await client.send_message(channel, msg)
							oldComment = newComment
							commentSTR = ""
							commentLST = []
							count = 0							# Reset the timeout counter
							break
						elif count == 5 and len(commentLST) == 5:	# If we hit the time limit and get 5 new comments
							print("5s & 5 comment Timeout!",commentLST)	# Local Print the comment list
							commentSTR = "\n".join(commentLST)
							msg = "```" + commentSTR + "```"
							await client.send_message(channel, msg)	# Send the comment to the Discord channel
							oldComment = newComment
							commentSTR = ""
							commentLST = []
							count = 0
							break
						elif count == 5 and len(commentLST) == 0:	# If we hit the time limit and have ZERO comments (red flag situation)
							print("Zero Comments",commentLST)	# Local Print the comment list
							commentSTR = ""
							commentLST = []
							count = 0
							break
						else:							# If the old comment still matches the new comment
							print("Still Waiting, Count:",listCount,"\n",commentLST)
							time.sleep(2)				# Keep the while loop running, but do not do anything.

			if session == "R":
				if oldComment != newComment:				# If the new comment does not match the old stored comment. . .
					if len(commentLST) <= 4:
						listCount = len(commentLST)
						commentLST.append("["+time.strftime('%X')+"] " + newComment)
						oldComment = newComment				# Set the new comment to be the old comment
						time.sleep(10)						# 10 second wait before restarting loop
					elif len(commentLST) == 5:
						commentSTR = "\n".join(commentLST)
						print("Printing Comments\n")		# Local Print the comment string
						msg = "```" + commentSTR + "```"
						await client.send_message(channel, msg)	# Send the comment to the Discord channel
						oldComment = newComment				# Set the new comment to be the old comment
						commentSTR = ""						# Reset the comment string
						commentLST = []						# Reset the comment list
						time.sleep(10)						# 10 second wait before restarting loop
				else:							# If the new comment *does* match the old stored comment. . .
#					time.sleep(10)
					count = 0
					while(count < 5):	# Start a while timer
						print("loop number: %d" % (count + 1))
						count += 1	# Increment the timer each time it runs
						timing()	# Poll for new comments
						if oldComment != newComment:	# If the new comment does not match the old stored comment. . .
							print("New Data, Break\n")
							time.sleep(2)
							break						# Stop the timer, we have a new comment
						if count == 5 and len(commentLST) in range (1,4):	# If we hit the time limit and have less than 5 new comments
							print("5s & <= 4 Timeout!",commentLST)	# Local Print the comment list
							commentSTR = "\n".join(commentLST)
							msg = "```" + commentSTR + "```"
							time.sleep(2)
							await client.send_message(channel, msg)
							oldComment = newComment
							commentSTR = ""
							commentLST = []
							count = 0							# Reset the timeout counter
							break
						elif count == 5 and len(commentLST) == 5:	# If we hit the time limit and get 5 new comments
							print("5s & 5 comment Timeout!",commentLST)	# Local Print the comment list
							commentSTR = "\n".join(commentLST)
							msg = "```" + commentSTR + "```"
							await client.send_message(channel, msg)	# Send the comment to the Discord channel
							oldComment = newComment
							commentSTR = ""
							commentLST = []
							count = 0
							break
						elif count == 5 and len(commentLST) == 0:	# If we hit the time limit and have ZERO comments (red flag situation)
							print("Zero Comments",commentLST)	# Local Print the comment list
							commentSTR = ""
							commentLST = []
							count = 0
							break
						else:							# If the old comment still matches the new comment
							print("Still Waiting, Count:",listCount,"\n",commentLST)
							time.sleep(2)				# Keep the while loop running, but do not do anything.


	except KeyboardInterrupt:
		print("Ending Program\n")
		quit()
	pass

#Start the whole thing
client.loop.create_task(indycar_comments())
client.run(TOKEN)
