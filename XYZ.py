import numpy
from datetime import date, datetime
from pandas.tseries.offsets import DateOffset
from scipy import optimize

# TODO: write a pricing env to include global info such as Pricing Date, etc

class Bond:
    """generic class for bond"""

    # TODO:
    # add SelectTemplate to provide default values
    # more precise day count calculation
    
    data = {}
    verbose = False
    
    # data
    def SetData(self, inputs):
        self.data = inputs

    def __init__(self, inputs):
        self.SetData(inputs)

    def Print(self):
        print('Bond ', self.data['maturity'], self.data['coupon'])

    # Analytics
    def PriceToYield(self, p, clean = False):
        def f(y):
            err = self.YieldToPrice(y, clean) - p
            return(err)
        return optimize.brentq(f, -1, 1)
        
    def YieldToPrice(self, y, clean = False):
        PricingDate = self.data['PricingDate']
        IssueDate = self.data['issue']
        MaturityDate = self.data['maturity']
        freq = self.data['CouponFreq']
        YearFraction = 1/freq
        coupon = self.data['coupon']
        NextCoupon = DateOffset(months = round(12/freq))

        if PricingDate > MaturityDate:
            return 0
        else:
            p = 0
            d = IssueDate
            df = 1
            t = 0
            tprev = 0
            accrued = -1
            while d <= MaturityDate:
                dprev = d
                d = (d + NextCoupon).date()
                if d >= PricingDate:
                    if accrued < 0:
                        DaysAccrued = (PricingDate - dprev).days
                        DaysInPeriod = (d - dprev).days
                        accrued = coupon*YearFraction/DaysInPeriod*DaysAccrued
                        if self.verbose:
                            print(d, 'Accrued : {:10.4f}%'.format(accrued*100))
                    t = (d - PricingDate).days/365
                    df *= 1/(1 + (t - tprev)*y)
                    p += coupon*YearFraction*df
                    tprev = t
                    if self.verbose:
                        print(d, "Coupon {:10.4f} {:10.4f} {:10.4f}%".format(t, df, p*100))
            p += df
            self.data['accrued'] = accrued
            if clean:
                p -= accrued
        return p

    def Duration(self):
        y = self.data['yield']
        DeltaShock = 0.0001
        p0 = self.YieldToPrice(y)
        p1 = self.YieldToPrice(y + DeltaShock)
        return (p1 - p0)/DeltaShock

    def Gamma(self):
        y = self.data['yield']
        DeltaShock = 0.0001
        p0 = self.YieldToPrice(y - 0.0001)
        p1 = self.YieldToPrice(y)
        p2 = self.YieldToPrice(y + 0.0001)
        return (p0 + p2 - 2*p1)/DeltaShock/DeltaShock
        

