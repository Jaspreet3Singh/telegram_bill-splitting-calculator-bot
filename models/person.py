class Person:
    id = None
    amt = 0
    individualInput = False
    extraAmt = 0

    def __init__(self, id):
        self.id = id

    def set_Id(self, id):
        self.id = id
    
    def set_Amt(self, amt):
        self.amt = amt

    def set_IndividualInput(self, individualInput):
        self.individualInput = individualInput

    def set_ExtraAmt(self, extraAmt):
        self.extraAmt = extraAmt

    def get_totalAmt(self):
        return self.extraAmt+self.amt