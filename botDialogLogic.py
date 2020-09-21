import logging
from models.users import UserChats
from models.person import Person

class BotDialogLog:

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    
    def getResponse(self, usr, msg):
        if msg.lower() == 'cancel' or msg == 'quit':
            usr.state = 7
            return "Ok, I'm going to sleep just message me again to wake me up!"

        if usr.state == 0:
            return self.status_zero(usr)

        elif usr.state == 1:
            return self.status_one(usr,msg)
        
        elif usr.state == 2:
            return self.status_two(usr,msg)
        
        elif usr.state == 3:
            return self.status_three(usr,msg)
        
        elif usr.state == 4:
            return self.status_four(usr,msg)
        
        elif usr.state == 5:
            return self.status_five(usr,msg)
        
        elif usr.state == 6:
            return self.status_six(usr,msg)


    ##---Methods to with all the status of dialog that the bot shld interact with---##
    def status_zero(self, usr):
        usr.state = 1
        return "Hi, would you like to split a bill?\nEnter total amount of payment on bill\ne.g. xxxx.xx\n\nJust send cancel at anytime to end our chat!"

    def status_one(self, usr, msg):
        amt = self.converToFloat(msg)
        if amt:
            usr.ript.totalAmt = amt
            usr.state = 2
            return "What precentage was the GST(%)?"
        else:
            return "Please input the amount in this format: xxxx.xx\ne.g. 120.34"

    def status_two(self, usr, msg):
        gst = self.convertToInt(msg)
    
        if gst or msg == '0':
            usr.ript.gst = gst
            usr.state = 3
            return "What precentage was the service charge(%)?"
        else:
            return "Please input the GST\ne.g. 7"

    def status_three(self, usr, msg):
        serCharge = self.convertToInt(msg)

        if serCharge or msg == '0':
            usr.ript.serviceCharge = serCharge
            usr.state = 4
            return "How many people was your bill with?"
        else:
            return "Please input the service charge\ne.g. 10"

    def status_four(self, usr, msg):
        total_ppl = self.convertToInt(msg)
        if total_ppl:
            self.createListOfPpl(usr,total_ppl)
            usr.state = 5
            return "How many people had a separate non-shared cost?"
        else:
            return "Please input the number of people\ne.g. 4"

    def status_five(self, usr, msg):
        numberOfSolo = self.convertToInt(msg)
        if (numberOfSolo and numberOfSolo <= len(usr.listOfPpl)) or msg == '0':
           
            usr.nonShareNo = numberOfSolo
            self.setIndividuals(usr,numberOfSolo)
            usr.inputNum = 0
            usr.ript.nonSharedCosts = 0
            return self.checkIndividualInputs(usr, msg)
        
        elif numberOfSolo and numberOfSolo > len(usr.listOfPpl):
            return "That's not right. There less people sharing the bill. Lets try again\nHow many people had a separate non-shared cost?"

        else:
            return "Please input the number of people\ne.g. 4"

    def status_six(self, usr, msg):
        extra = self.converToFloat(msg)
        if extra:
            usr.listOfPpl[usr.inputNum].extraAmt = extra
            usr.ript.nonSharedCosts += extra 
            usr.inputNum += 1 #track preson to input 
            usr.nonShareNo -= 1 #decrease expected 
            return self.checkIndividualInputs(usr, msg)
        else:
            return "Please input the extra amount person "+ str(usr.inputNum+1) +" had?\ne.g. 4.50"

    ##--Helper methods--##
    #Converts the string msg to int
    def convertToInt(self, msg):
        try:
            return int(msg)
        except ValueError:
            return False
    
    #Converts the string msg to float
    def converToFloat(self, msg):
        try:
            return float(msg)
        except ValueError:
            return False

    #Creates a list of people that are sharing the bill
    def createListOfPpl(self, usr, num):
        i = 0
        usr.listOfPpl = []
        while i < num:
            usr.listOfPpl.append(Person(i))
            i += 1
        logging.info(len(usr.listOfPpl))

    #Sets the number of non-shared people
    def setIndividuals(self, usr, num):
        i = 0
        while i < num:
            usr.listOfPpl[i].individualInput = True
            i += 1

    #Prompts the user for the individual inputs
    def checkIndividualInputs(self,usr,num):
        if usr.nonShareNo > 0:
            usr.state = 6
            return "How much total extra did person "+ str(usr.inputNum+1)+" had(w/o gst & service charges)?"       
        else: 
            usr.state = 7
            return self.computingResults(usr)
    
    ##Computing the final spilt of the bill to the users
    def computingResults(self, usr):
        sharedValue = (usr.ript.totalAmt/usr.ript.getExtraCharges()) - usr.ript.nonSharedCosts
        individualSharedCost = sharedValue/ len(usr.listOfPpl)
        computedMsg = "Results:\n"
        totalCost = 0
        totalIndividualCost = 0 
        for person in usr.listOfPpl:
            person.amt = individualSharedCost
            totalIndividualCost = person.get_totalAmt() * usr.ript.getExtraCharges()
            totalCost += totalIndividualCost
            computedMsg = computedMsg + "Person "+str(person.id +1)+" = (" + str(round(person.amt,2)) + " + " + str(round(person.extraAmt,2))+") * "+str(usr.ript.getExtraCharges())+" = "+str(round(totalIndividualCost,2))+"\n\n"

        computedMsg = computedMsg + "Total Cost(based on rounded amts): "+str(round(totalCost,2))+"\n\nHere's the estimated amount owed by each person on the bill!\nChat with me again to spilt another bill! "

        return computedMsg
