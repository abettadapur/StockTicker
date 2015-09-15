echo %~dp0
pushd %~dp0
REM START "" /d "C:\folder" /b "p:\php\php.exe" file.php
CALL .\venv\Scripts\activate.bat
python cronjob.py
popd
PAUSE