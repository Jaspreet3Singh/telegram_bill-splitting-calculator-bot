class Receipt:
    totalAmt = 0
    gst = 0.00
    serviceCharge = 0.00
    nonSharedCosts = 0 ## total non shared cost
    
    def set_TotalAmt(self, totalAmt):
        self.totalAmt = totalAmt

    def set_Gst(self, gst):
        self.gst = gst

    def set_ServiceCharge(self, serviceCharge):
        self.serviceCharge = serviceCharge

    ## returns the total service charges in non precentage form
    def getExtraCharges(self):
        return ((self.gst+self.serviceCharge)/100) + 1
    


