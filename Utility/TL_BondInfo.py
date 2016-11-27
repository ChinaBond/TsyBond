'''
Created on Nov 26, 2016

@author: shaunz
'''
from Library.Datayes_Connect import Client
import pandas

client = Client()
bondInfo = client.getBondInfo()
df = pandas.DataFrame(bondInfo['data'])
#0202010101 is the typeID for Treasuries
tsy = df.loc[df['typeID']==u'0202010101']
tsy.to_csv('%s/bondInfo.csv' % (client.getHomePath()),encoding='utf-8')
print('bond info saved at %s/bondInfo.csv' % client.getHomePath())