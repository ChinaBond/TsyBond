class Bond:
    """generic class for bond"""

    data = {}
    
    # data
    def SetData(self, inputs):
        self.data = inputs

    def __init__(self, inputs):
        self.SetData(inputs)

    def Print(self):
        print(self.data['maturity'], self.data['coupon'])

    # Analytics
    def PriceToYield(self, p):
        pass

    def YieldToPrice(self, y):
        pass

    def Duration(self):
        pass

    def Gamma(self):
        pass
    
    
