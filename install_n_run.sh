#!/usr/bin/sh
# Script to install ALL dependencies, 
# set up virtual environment for the libs, set up token variable
# and RUN the bot

# Uncomment below line to install python
#brew install python3
python3 -m venv env
pip install -r requirements.txt
export BOT_API_TOKEN="813975112:AAEnHpE9CJVNRTa7GF8815IZ1hyWnwPrTOs"
python3 main.py
