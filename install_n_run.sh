#!/usr/bin/sh
# Script to install ALL dependencies, 
# set up virtual environment for the libs, set up token variable
# and RUN the bot

# Uncomment below line to install python
#brew install python3
python3 -m venv env
pip install -r requirements.txt
export BOT_API_TOKEN="832870755:AAHoS4O6MzKXR6pMWRpANU46NKDE_xuTf10"
python3 main.py
