@echo off

SET this_directory=%~dp0

cd %this_directory%

call venv\scripts\activate


powershell.exe "python examples/auto_tweet.py" >> "resources/temp/auto_tweet_log.txt"

call deactivate

::pause