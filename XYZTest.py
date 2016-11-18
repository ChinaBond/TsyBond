import XYZ

inputs = {'uid' : 12345,
      'maturity' : '1/1/2026',
      'coupon' : 0.05,
      'price' : 115
}

b = XYZ.Bond(inputs)
b.Print()
