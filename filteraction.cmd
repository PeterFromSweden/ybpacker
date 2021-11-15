:: Script to be used from xgate mail
:: Use with F8-key in inbox, one mail at a time

:: cd to script folder
cd %~dp0

:: Strip any leading spaces
Set _time=%time: =0%

:: Create date-time string suitable for filename
set datetimef=%date:~-4%_%date:~3,2%_%date:~0,2%__%_time:~0,2%_%_time:~3,2%_%_time:~6,2%
move leaderboard.csv leaderboard%datetimef%.csv
move expedition.txt expedition%datetimef%.txt
move /y boatids.txt boat-ids.txt


