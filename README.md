# upgraded-telegram
Comment Bot &amp; Other Racing Stuff

### Requirements:
* Python 3
* Requests module (`pip install requests`)

#### Files:
* discord-comment.py
  - Comment bot for Discord. Doesn't fully work as of the initial commit. Crashes after completing the second loop. Some kind of async issue, I'm not able to figure it out.
* IMSA-timing.py
  - Timing & scoring for IMSA races.
* local-comment.py
  - Locally running comment script, prints to the screen.
* timing-scoring.php
  - T&S webpage script that runs on a varying page refresh timer, depending on session.
  - Includes color formatting for flags (red/yellow/green), push 2 pass, tire choices, lap times, and sector times.
  - Next major update will support IMS with stuff like no tow laps, speed averages, etc.
* timing-scoring.py
  - Locally running T&S script, prints to the screen.
  - Used switch-case statements to handle road/street qualifying text, and based on the length of JSON data, to insert the correct number of spaces to maintain formatting. Tabs have been almost entirely removed, and so there should only be display issues in the case of a very small screen width.
  - Next major update will support IMS with stuff like no tow laps, speed averages, etc.
  - Also need to get rid of tabs for formatting the driver column and driver names.
* old-timing.py
  - The original local T&S script, before the later attempts at polishing the output and making the code more readable.
* JSON-*.txt
  - Text files containing session data for practice/qual/race, for road/street/oval courses.
