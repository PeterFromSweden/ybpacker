set datetimef=%date:~-4%_%date:~3,2%_%date:~0,2%__%time:~0,2%_%time:~3,2%_%time:~6,2%
move expedition.txt expedition%datetimef%.txt
move /y boatids.txt boat-ids.txt
