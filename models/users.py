from .person import Person
from .receipt import Receipt

class UserChats:
    chat_id = None
    state = "empty"
    active = None
    lastMsgTime = 0
    
    #Handle the data for each user
    listOfPpl =[]
    ript = Receipt()

    #Dealing with the separate inputs for non-shared items
    nonShareNo = 0
    inputNum = 0

    def __init__(self, chat_id, state, active, lastMsgTime):
        self.chat_id = chat_id
        self.state = state
        self.active = active
        self.lastMsgTime = lastMsgTime
        