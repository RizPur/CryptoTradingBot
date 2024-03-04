@echo off

cd C:\Users\Joel\Desktop\Engineering\Python3Stuff\CryptoTradingBot
call venv\Scripts\activate.bat
python schedule_prices_logging.py

REM Deactivate the virtual environment when done
call venv\Scripts\deactivate.bat