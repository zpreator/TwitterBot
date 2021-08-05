@echo off

SET this_directory=%~dp0

cd %this_directory%

call venv\scripts\activate

powershell.exe "python main.py"

call deactivate

::pause