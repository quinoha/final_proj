

@echo off
echo =========================================
echo WORKALONE: AI Fitness Session Manager
echo =========================================
echo.
echo [1/3] Creating virtual environment (venv)...
python -m venv venv

echo.
echo [2/3] Activating venv and installing dependencies... (This may take a minute)
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [3/3] Setup complete! Starting the program...
echo.
python main_pc_session.py --routine auto

echo.
echo Session ended. Press any key to exit.
pause