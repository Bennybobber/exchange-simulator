# exchange-simulator
Disseration project for a cryptocurrnecy exchange simulator

Server folder contains the Flask server, which hosts all the backend API calls.
To build the server flask files ensure that:
1. Install Python
2. Ensure that a config.py is placed in the server folder (see after step 4).
3. In the server directory run "pip install -r requirements.txt"
4. Run the server in the /server directory by running "flask run"

*** SAMPLE CONFIG FILE ***
* Name config.py and place inside the /server directory *
from flask import Flask, Config

class DefaultConfig():
    COIN_API_KEY = "xxxxxxxxx" (Please get a coin api key from https://docs.coincap.io/)
    TOP_CURRENCY_COUNT = 10
    DB_URI = "mongodb://localhost:xxxx" (set your own mongodb port)
    SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXX' (Set as your own random string for hasing tokens)
    

def get_config():
    config = DefaultConfig()
    return config

Frontend contains the vue.js server.
1. Ensure Node + NPM is installed
2. Go the /frontend directory
3. Run the command "npm install"
4. Run the command "npm run serve"