import os
import requests
from bottle import Bottle, response, request as bottle_request
from bot import TelegramBot

if __name__ == '__main__':  
    app = TelegramBot()
    app.run(host="localhost", port="5000") ## Used for running locally
    # app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000))) ## used for running on Heroku
   