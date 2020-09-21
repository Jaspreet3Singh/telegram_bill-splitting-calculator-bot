import logging
import requests  
from bottle import Bottle, response, request as bottle_request
from datetime import datetime
import configparser as cfg
from models.users import UserChats
from botDialogLogic import BotDialogLog

class BotHandler:  
    BOT_URL = None
    userList = [] #maintains list of active users the bot is chatting with
    chat = None #current user the bot is chatting with
    counter = 0

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    def get_chat_id(self, data):
       ## Check if the users have pending previous request and gets the chat id
        
        chat_id = data['message']['chat']['id']
        logging.info(data)
        
        self.setUser(chat_id)
        logging.info(self.counter)
        return chat_id

    def get_message(self, data):
       
      ##  Method to get message
      
        message_text = data['message']['text']

        return message_text

    def send_message(self, prepared_data):
        ## Sends reply from the bot to the users

        message_url = self.BOT_URL + 'sendMessage'
        requests.post(message_url, json=prepared_data)
       # self.userList[self.counter] = self.chat

    def setUser(self, chat_id):
        #Check to find if the users is already chatting if not adds them to list
        self.counter = 0 
        foundUser = False
        now = datetime.now() # time object
        if len(self.userList) != 0:
            for usr in self.userList:
                if usr.chat_id == chat_id:
                    self.chat = usr
                    logging.info((now-self.chat.lastMsgTime).total_seconds())
                    self.chat.lastMsgTime = now 
                    foundUser = True
                    break
                self.counter += 1

        if foundUser == False:
            self.chat = UserChats(chat_id,0,True,now)
            self.userList.append(self.chat)
        
    #removes users from list that have completed/cancelled the chat with the bot
    def endedChat(self, chatId):
        logging.info("Number of user")
        logging.info(len(self.userList))
        index = 0
        for usr in self.userList:
            if (usr.chat_id == chatId):
                break
            else:
                index+=1
        self.userList.pop(index)
        logging.info("Remove user")
        logging.info(len(self.userList))

      
    # this method will be scheduled by a timer [NOT in used]
    def removeUserFromList(self):
        now = datetime.now() # time object
        logging.info(len(self.userList))
        tempList = []
        for usr in self.userList:
            if (now-self.chat.lastMsgTime).total_seconds()<=30:
                tempList.append(usr)
            elif (now-self.chat.lastMsgTime).total_seconds()>30:
                json_data = {
                    "chat_id": usr.chat_id,
                    "text": "Hi seems like you have't replied so I'm going to sleep just message me again to wake me up!",
                }
                self.send_message(json_data)
           
        ##Clear remove old list and set updated list
        self.userList.clear()
        self.userList = tempList   

        logging.info(len(self.userList)) 

    

class TelegramBot(BotHandler, Bottle):  
    BOT_URL = None
    dialog = BotDialogLog()

    def __init__(self, *args, **kwargs):
        super(TelegramBot, self).__init__()
        self.BOT_URL = 'https://api.telegram.org/bot{}/'.format(self.read_token_from_config_file("configs/config.cfg"))
        self.route('/', callback=self.post_handler, method="POST")
        #Timer functions [not yet implemented]
        #t = threading.Timer(10.0, self.removeUserFromList())
        #t.setName('t1')
        #t.start()
         

    #Bot logic
    def response_text_message(self, message):
        return self.dialog.getResponse(self.chat,message)

    def prepare_data_for_answer(self, data):
        chat_id = self.get_chat_id(data) 
        message = self.get_message(data) 
        answer = self.response_text_message(message)

        if(self.chat.state == 7):
            self.endedChat(chat_id)
    
        json_data = {
            "chat_id": chat_id,
            "text": answer,
        }

        return json_data

    def post_handler(self):
        data = bottle_request.json
        answer_data = self.prepare_data_for_answer(data)
        self.send_message(answer_data)

        return response

    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')