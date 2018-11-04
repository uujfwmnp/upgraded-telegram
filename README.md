# upgraded-telegram
Comment Bot &amp; Other Racing Stuff

* discord-comment.py
  - Comment bot for Discord. Doesn't fully work as of the initial commit. Crashes after completing the second loop. Some kind of async issue, I'm not able to figure it out.
* local-comment.py
  - Locally running comment script, prints to the screen.
* timing-scoring.py
  - Locally running T&S script, prints to the screen.
  - Used switch-case statements to handle road/street qualifying text, and based on the length of JSON data, to insert the correct number of spaces to maintain formatting. Tabs have been almost entirely removed, and so there should only be display issues in the case of a very small screen width.
  - Next major update will support IMS with stuff like no tow laps, speed averages, etc.
* old-timing.py
  - The original local T&S script, before the later attempts at polishing the output and making the code more readable.
