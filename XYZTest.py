import XYZ
from datetime import date

inputs = {'uid' : 12345,
          'issue' : date(2016, 1, 1),    
          'maturity' : date(2026, 1, 1),
          'CouponFreq' : 2,
          'coupon' : 0.05,
          'price' : 115,
          'PricingDate' : date(2016, 11, 17)
}

b = XYZ.Bond(inputs)
b.Print()
print('-----------------------------------')

b.verbose = True
p = b.YieldToPrice(0.05)
b.verbose = False
clean = b.YieldToPrice(0.05, clean=True)
print('Dirty Price : ', "{:10.4f}%".format(p*100))
print('Clean Price : ', "{:10.4f}%".format(clean*100))
print('    Accrued : ', "{:10.4f}%".format(b.data['accrued']*100))
print('-----------------------------------')

y = b.PriceToYield(p)
print('Yield : ', "{:10.4f}%".format(y*100))

b.data['yield'] = y
delta = b.Duration()
print('Delta : ', "{:10.4f}".format(delta))
gamma = b.Gamma()
print('Gamma : ', "{:10.4f}".format(gamma))

shock = 0.01
y += shock
pred = p + shock*delta + gamma*shock*shock/2
actual = b.YieldToPrice(y)
print('Predicted : ', "{:10.4f}".format(pred))
print('    Delta : ', "{:10.4f}".format(shock*delta))
print('    Gamma : ', "{:10.4f}".format(gamma*shock*shock/2))
print('   Actual : ', "{:10.4f}".format(actual))
