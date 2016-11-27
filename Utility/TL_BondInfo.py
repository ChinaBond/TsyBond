'''
Created on Nov 26, 2016

@author: shaunz
'''
from Library.Datayes_Connect import Client
import pandas

client = Client()
bondInfo = client.getBondInfo()
df = pandas.DataFrame(bondInfo['data'])
#202010101 is the typeID for Treasuries
tsy = df[df['typeID']==202010101]
tsy.to_csv('%sbondIno.csv' % (client.getHomePath()),encoding='utf-8')
print 'bond info saved'