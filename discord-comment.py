import discord
import asyncio
import aiohttp
import requests
import time, json, os, sys, re

TOKEN = 'DISCORD-BOT-TOKEN'
client = discord.Client()

def timing():
    get = requests.get('https://indycarsso.blob.core.windows.net/racecontrol/timingscoring.json') # Request data from Indycar
    rawdata = get.text                                                          # Set text of GET reply as a variable
    top = rawdata.replace("jsonCallback(", "")                                  # Remove top line that is not JSON valid
    bottom = top.replace(");", "")                                              # Remove bottom line that is not JSON valid
    data = json.loads(bottom)                                                   # Load the formatted string as JSON
# LOCAL DEBUG
#   json_data = open("JSON FILE HERE", "r").read()
#   data = json.loads(json_data) 

#Setup Array Event Variables
    global eventFlag, session, newComment
    eventFlag  = data['timing_results']['heartbeat']['SessionStatus'] #Cold/In Progress
    session    = data['timing_results']['heartbeat']['SessionType'] #Q/P/R
    newComment = data['timing_results']['heartbeat']['Comment']

@client.event
async def indycar_comments():
    await client.wait_until_ready()
    print("Current servers:")
    for server in client.guilds:
        print(server.name)
    #channel = discord.utils.get(client.get_all_channels(), name='CHANNEL-NAME-HERE')
    channel = client.get_channel(1234567)
    listCount = None    #Setup variable
    oldComment = ""     #Setup variable
    commentLST = []     #Setup variable
    try:
        while True:
            timing()
            if eventFlag == "COLD":
                print("Event has not started, or is finished.") # Local notice only
                time.sleep(30)
            if oldComment != newComment:    # If the new comment does not match the old stored comment. . .
                if session == "Q" or session == "P" and re.search('entered the pits.|exited the pits.', newComment): # Ignore pit in/out comments during qual/practice
                    time.sleep(2)
                else:
                    if len(commentLST) < 5:
                        listCount = len(commentLST)
                        commentLST.append("["+time.strftime('%X')+"] " + newComment)
                        oldComment = newComment             # Set the new comment to be the old comment
                        print("listCount:", len(commentLST))
                        time.sleep(2)                       # 5 second wait before restarting loop
                    if len(commentLST) == 5:
                        commentSTR = "\n".join(commentLST)
                        print("Printing Comments\n")        # Local Print the comment string
                        msg = "```" + commentSTR + "```"
                        await channel.send(msg) # Send the comment to the Discord channel
                        oldComment = newComment             # Set the new comment to be the old comment
                        commentSTR = ""                     # Reset the comment string
                        commentLST = []                     # Reset the comment list
                        time.sleep(2)                       # 5 second before restarting loop
            else:                           # If the new comment *does* match the old stored comment. . .
                count = 0
                listCount = len(commentLST)
                while(count <= 5):   # Start a while timer
                    print("loop number: ", count+1)   # DEBUG: So we know where we are in the loop.
                    count += 1      # Increment the timer each time it runs
                    timing()        # Poll for new comments
                    if oldComment != newComment:    # If the new comment does not match the old stored comment. . .
                        if session == "Q" or session == "P" and re.search('entered the pits.|exited the pits.', newComment): # Ignore pit in/out comments during qual/practice
                            time.sleep(2)
                            break                       # Stop the timer, we don't care about pit in/out
                        else:
                            print("New Data, Break\n")
                            time.sleep(2)
                            break                       # Stop the timer, we have a new comment
                    if count == 5 and len(commentLST) in range (1,4):   # If we hit the time limit and have less than 5 new comments
                        print("5 second timeout, less than 5 comments!",commentLST,"\n")  # Local Print the comment list
                        commentSTR = "\n".join(commentLST)
                        msg = "```" + commentSTR + "```"
                        time.sleep(2)
                        await channel.send(msg)
                        oldComment = newComment
                        commentSTR = ""
                        commentLST = []
                        count = 0                           # Reset the timeout counter
                        break
                    elif count == 5 and len(commentLST) == 5: # If we hit the time limit and get 5 new comments
                        print("5 second timeout, 5 comments!",commentLST,"\n") # Local Print the comment list
                        commentSTR = "\n".join(commentLST)
                        msg = "```" + commentSTR + "```"
                        await channel.send(msg) # Send the comment to the Discord channel
                        oldComment = newComment
                        commentSTR = ""
                        commentLST = []
                        count = 0
                        break
                    elif count == 5 and len(commentLST) == 0: # If we hit the time limit and have ZERO comments (red flag situation)
                        print("Zero Comments\n",commentLST)   # Local Print the comment list
                        commentSTR = ""
                        commentLST = []
                        count = 0
                        break
                    else:                           # If the old comment still matches the new comment
                        print("Still Waiting, Comments Stored:",listCount,commentLST)
                        time.sleep(2)               # Keep the while loop running, but do not do anything.


    except KeyboardInterrupt:
        print("Ending Program\n")
        await client.close()
        quit()
    pass

#Start the whole thing
client.loop.create_task(indycar_comments())
client.run(TOKEN)
