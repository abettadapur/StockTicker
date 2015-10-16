PUSHD %~dp0
CALL .\venv\Scripts\activate.bat
python cronjob.py
POPD