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

b.verbose = True
p = b.YieldToPrice(0.05)
print(p)
b.verbose = False

print(b.PriceToYield(p))
