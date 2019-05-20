# JSON Key/Value Definitions
---
***Note: Not all keys will appear at all times. Some keys may have different values depending on the series. Keys are arranged alphabetically, but this is not how it appears in the JSON***
#### JSON setup
```
{
	"timing_results": {
		"heartbeat": {
		    "foo":bar",
		    "foo":bar"
		},
		"Item": [{
		        "foo":"bar",
		        "foo":"bar"
            }, {
		        "foo":"bar",
		        "foo":"bar"
		}]
	}
}
```
### Global `Heartbeat` Keys
| Key | Example Value | Definition | Notes |
| ------ | ------ | ------ | ------ |
|`Comment`|`Tony Kanaan #14 has entered the pits.`|Information passed to the teams and media from Race Control||
|`currentFlag`|`GREEN`|Green flag|Race/Qual/Practice underway|
|-|`YELLOW`|Yellow|Caution|
|-|`RED`|Red|Session halted|
|-|`CHECKERED`|Checkered|Session over|
|-|`UNFLAGGED`|Unflagged|Typically shown before a session starts|
|-|`COLD`|Cold|Typically shown well after a session is over and all cars are off the track|
|`dateTime`|`7/8/2018 1:57:17 PM`|The time the data was updated||
|`elapsedTime`|`15:13`|How long the session has been running|Qual/Race will show elapsed time, not always shown!|
|`EventID`|`3750`|Unsure||
|`eventName`|`Iowa Corn 300`|Name of the event||
|`greenTime`|`15:14`|Unsure|I assume it's the time (local) the track went green to start the race?|
|`lapNumber`|`46`|Total laps run up to this point|Only shown during races!|
|`overallTimeToGo`|`39:21`|Time left in the session|Practice sessions will show time remaining. This may also occur during timed races, not sure. Not always shown!|
|`preamble`|`R.1`|Explains the type of session|Different values for different session types. IndyCar sessions will always have `.I` at the end, Lights have `.L`|
|`Series`|`IndyCar`|What series is this?|Indy Lights, USF2000, and others also use this T&S system|
|`SessionStatus`|`IN PROGRESS`|In Progress|Cars are on track|
|-|`WARM`|Warm|Session is not yet underway, but crews/cars are on the pit lane|
|-|`COLD`|Cold|Session is over, crews/cars are no longer in the pits|
|`SessionType`|`R`|Race Session||
|-|`P`|Practice Session||
|-|`Q`|Qualifying Session||
|`timeOfMostRecent`|`0`|Unsure||
|`totalLaps`|`300`|Total laps in the race|Only shown during races!|
|`trackName`|`Iowa Speedway`|Name of the track||
|`trackLength`|`0.894`|Length of the track (in miles)||
|`trackType`|`O`|Type of track|Oval|
|-|`I`|-|Indy Speedway (Indy GP uses RC)|
|-|`RC`|-|Road Course|
|-|`SC`|-|Street Course|
|`yellowTime`|`1:13`|Unsure|I assume it's total time under yellow?|

### Global `Item` Keys
| Key | Example Value | Definition | Notes |
| ------ | ------ | ------ | ------ |
|`AverageSpeed`| `45.071`|Average speed over X number of laps (I think)|Really only useful for Indy qualifying|
|`bestLapTime`| `18.4824`|Best lap time||
|`bestLap`| `8`|Best lap number||
|`BestSpeed`| `174.133`|Best lap in miles per hour||
|`className`| `IndyCar`|Unsure.|More multi-class racing stuff?|
|`comment`| |Unsure.|I've never seen this used before|
|`deleted`| `0`|Unsure||
|`diff`| `0.0000`|Difference between driver and leader||
|`DriverID`| `326`|Unsure||
|`EntrantID`| `5`|Unsure.||
|`equipment`| `D/H/F`|What kind of gear does the driver have?|Dallara/Honda/Firestone|
|-| `D/C/F`|-|Dallara/Chevy/Firestone|
|`firstName`| `Scott`|Driver's first name||
|`flagStatus`| `Green`|Unsure.|I assume it will match up with `currentFlag`, perhaps with the addition of black flags and blue flags?|
|`gap`| `0.0000`|Difference between driver and next position ahead||
|`laps`| `16`|Laps completed||
|`lastLapTime`| `30.0539`|Last lap time||
|`lastName`| `Dixon`|Driver's last name||
|`LastSpeed`| `107.088`|Last lap in miles per hour||
|`lastPitLap`| `16`|The lap the driver pitted||
|`license`| `Veteran`|Veteran driver||
|-| `Rookie`|Rookie driver||
|`marker`| `7`|Unsure||
|`no`| `9`|Car number||
|`NTRank`| `0`|Driver's positon on the no-tow ranking|Only populates during Indy practice|
|`NTLap`| `0`|Lap number for driver's best no-tow lap|Only populates during Indy practice|
|`NTBestTime`| `-0.0001`|Best no-town lap time (in seconds)|Only populates during Indy practice|
|`oldRank`| `1`|Unsure|Perhaps the position they were last in on the previous lap?|
|`onTrack`| `False`|Is the driver on track?|No!|
|-| `True`|-|Yes!|
|`overallRank`| `1`|Unsure|Might be used for multi-class races?|
|`OverTake_Remain`| `200`|Amount of Overtake/Push To Pass remaining (in seconds)|Only active on road and street courses|
|`OverTake_Active`| `0`|Is Overtake/Push To Pass active?|Never seen this used, but I assume it's 0 for inactive|
|-| `1`|-|I assume it's 1 for active|
|`Passes`| `2`|Number of passes a driver has made|Only populates during a race|
|`pitStops`| `6`|Number of pit stops made||
|`resultID`|`5`|Unsure||
|`rank`| `1`|Driver position||
|`sincePitLap`| `0`|Laps since the last pit stop||
|`startPosition`| `6`|Driver's starting position||
|`status`| `In Pit`|Status of the driver (potentially more values than these)|Driver in pits|
|-| `Active`|-|Driver on track|
|-| `Contact`|-|Driver out of session due to contact|
|-| `Mechanical`|-|Driver out of session due to mechanical failure|
|`team`| `Chip Ganassi Racing Teams`|Team name||
|`TeamID`| `25`|Unsure.||
|`Tire`| `P`|Tire compound being used|P for Primary/Blacks|
|-| `O`|-|O for Option/Alternates/Reds|
|-| `W`|-|W for Wets|
|`totalEntrantPoints`| `393`|Season points||
|`totalDriverPoints`| `393`|Season points||
|`totalTime`| `19:02.5281`|Unsure.|Maybe total time on track?|
|||||

# Oval-Only `Item` Keys
| Key | Example Value | Definition | Notes |
| ------ | ------ | ------ | ------ |
|`preamble`|`P1.I`|Practice Session|The number changes to reflect the session, (1, 2, 3, etc.), or F for final `PF.I`|
|-|`Q1.1`|Qualifying|There is only one qualification session, so I'm making an assumption, I do not have the data.|
|-|`R.1`|Race||
|`trackType`|`O`|Type of track|Oval|
|||||

# Indy-Only `Item` Keys
| Key | Example Value | Definition | Notes |
| ------ | ------ | ------ | ------ |
|`Best_T1_SPD`| `241.637`|Best turn 1 trap speed||
|`Best_T2_SPD`| `239.637`|Best turn 2 trap speed||
|`Best_T3_SPD`| `239.805`|Best turn 3 trap speed||
|`Best_T4_SPD`| `237.365`|Best turn 4 trap speed||
|`lap1QualSpeed`| `230.800`|Lap time (in MPH) of qual lap 1|Only appears during qualification|
|`lap2QualSpeed`| `230.078`|Lap time (in MPH) of qual lap 2|Only appears during qualification|
|`lap3QualSpeed`| `229.798`|Lap time (in MPH) of qual lap 3|Only appears during qualification|
|`lap4QualSpeed`| `229.659`|Lap time (in MPH) of qual lap 4|Only appears during qualification|
|`lap1QualTime`| `38.9948`|Lap time (in seconds) of lap 1|Only appears during qualification|
|`lap2QualTime`| `39.1172`|Lap time (in seconds) of lap 2|Only appears during qualification|
|`lap3QualTime`| `39.1649`|Lap time (in seconds) of lap 3|Only appears during qualification|
|`lap4QualTime`| `39.1886`|Lap time (in seconds) of lap 4|Only appears during qualification|
|`lastWarmUpQualSpeed`| `222.320`|Lap time (in MPH) of last warmup lap|Only appears during qualification|
|`lastWarmUpQualTime`| `40.4822`|Lap time (in seconds) of the last warmup lap|Only appears during qualification|
|`NTBestTime`| `37.616`|Best no-town lap time (in seconds)|Only populates during Indy practice|
|`NTLap`| `10`|Lap number for driver's best no-tow lap|Only populates during Indy practice|
|`NTRank`| `1`|Driver's positon on the no-tow ranking|Only populates during Indy practice|
|`onBubble`| `False`|Is the driver on the 33rd position bubble?|No!|
|-| `True`|-|Yes!|
|`preamble`|`P1.I`|Practice Session|The number changes to reflect the session (1, 2, 3, etc.), or F for final `PF.I`|
|-|`I1.I`|Saturday Qualifying|Only seen this used once, I'm making an assumption.|
|-|`I2.I`|Bump Day, Race For Last, Last Row Shootout, etc.|Only seen this used once, I'm making an assumption.|
|-|`I3.I`|Fast 9 Shootout|Only seen this used once, I'm making an assumption.|
|-|`R.I`|Race|I'm making an assumption, I do not have the data.|
|`QStatus`| `Qualified - Pole Day - Group 1`|Did the driver qualify and when?|I don't have any more data for other status values|
|`T1`| `241.637`|Last turn 1 trap speed||
|`T2`| `239.637`|Last turn 1 trap speed||
|`T3`| `239.805`|Last turn 1 trap speed||
|`T4`| `237.365`|Last turn 1 trap speed||
|`totalQualTime`| `2:36.4655`|Total of all qualification laps on track during the attempt|Only appears during qualification|
|`trackType`|`I`|Type of track|Indy Speedway|
|||||


# Road/Street-Only `Item` Keys
| Key | Example Value | Definition | Notes |
| ------ | ------ | ------ | ------ |
|`Best_I1`| `29.1898`|Best sector 1 time (in seconds)||
|`Best_I2`| `19.7503`|Best sector 2 time (in seconds)||
|`Best_I3`| `12.6918`|Best sector 3 time (in seconds)|There could potentially be more than 3 sectors, but I've not seen it yet|
|`I1`| `29.1898`|Last sector 1 time (in seconds)||
|`I2`| `19.7503`|Last sector 2 time (in seconds)||
|`I3`| `12.6918`|Last sector 3 time (in seconds)|There could potentially be more than 3 sectors, but I've not seen it yet|
|`OverTake_Remain`| `200`|Amount of Overtake/Push To Pass remaining (in seconds)|Only active on road and street courses|
|`OverTake_Active`| `0`|Is Overtake/Push To Pass active?|Never seen this used, but I assume it's either 1 or 0|
|`preamble`|`P1.I`|Practice session|The number changes to reflect the session (1, 2, 3, etc.)|
|-|`Q1.I`|Qualifying Round 1, Group 1||
|-|`Q2.I`|Qualifying Round 1, Group 2||
|-|`Q3.I`|Qualifying Round 2|"Fast 12"|
|-|`Q4.I`|Qualifying Round 3|"Fast 6"|
|`Tire`| `P`|Tire compound being used|P for Primary/Blacks|
|-| `O`|-|O for Option/Alternates/Reds|
|-| `W`|-|W for Wets|
|`trackType`|`RC`|Type of track|Road Course|
|-|`SC`|Type of track|Street Course|
|||||
