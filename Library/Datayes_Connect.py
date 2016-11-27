# -*- coding: utf-8 -*-
import httplib
import urllib
import json
import pandas
from datetime import datetime,timedelta

import StringIO, gzip
HTTP_OK = 200
HTTP_AUTHORIZATION_ERROR = 401

class Client:
    #设置因网络连接，重连的次数
    # TODO: customize where to load token
    reconnectTimes=2
    httpClient = None
    def __init__( self ):
        self.domain = 'api.wmcloud.com'
        self.port = 443
        self.httpClient = httplib.HTTPSConnection(self.domain, self.port, timeout=60)
        #set token
        token_file = open('/home/shaunz/Documents/ChinaBond/Login/Dataeyes Token','r')
        self.token = token_file.read(64)
            
    def __del__( self ):
        if self.httpClient is not None:
            self.httpClient.close()
            
    def encodepath(self, path):
        #转换参数的编码
        start=0
        n=len(path)
        re=''
        i=path.find('=',start)
        while i!=-1 :
            re+=path[start:i+1]
            start=i+1
            i=path.find('&',start)
            if(i>=0):
                for j in range(start,i):
                    if(path[j]>'~'):
                        re+=urllib.quote(path[j])
                    else:
                        re+=path[j]  
                re+='&'
                start=i+1
            else:
                for j in range(start,n):
                    if(path[j]>'~'):
                        re+=urllib.quote(path[j])
                    else:
                        re+=path[j]  
                start=n
            i=path.find('=',start)
        return re
        
    def getData(self, path):
        result = None
        path='/data/v1' + path
        #print path
        path=self.encodepath(path)
        for i in range(self.reconnectTimes):
            try:
                #set http header here
                self.httpClient.request('GET', path, headers = {"Authorization": "Bearer " + self.token,
                                                                "Accept-Encoding": "gzip, deflate"})
                #make request
                response = self.httpClient.getresponse()
                result = response.read()
                compressedstream = StringIO.StringIO(result)  
                gziper = gzip.GzipFile(fileobj=compressedstream)
                try:
                    result = gziper.read()
                except:
                    pass
                if(path.find('.csv?')!=-1):
                    result=result.decode('GBK').encode('utf-8')
                return response.status, result
            except Exception, e:
                if i == self.reconnectTimes-1:
                    raise e
                if self.httpClient is not None:
                    self.httpClient.close()
                self.httpClient = httplib.HTTPSConnection(self.domain, self.port, timeout=60)
        return -1, result
    
    def getBondHistory(self,ticker):
        today = datetime.now()+timedelta(days=5)
        today_str = '%04d%02d%02d' % (today.year,today.month,today.day)
        url = '/api/bond/getMktIBBondsdCCXE.json?field=&secID=%s&startDate=&endDate=%s' % (ticker,today_str)
        code, result = self.getData(url)
        if code==200:
            ts_json = json.loads(result)
            if ts_json['retCode'] == -1:
                print ts_json['retMsg']
            else:
                ts_df = pandas.DataFrame(ts_json['data'])
                return ts_df
        else:
            print code
            print result
            
    def getBondInfo(self):
        url = '/api/bond/getBond.json?field=&ticker=&secID=&exchangeCD=XIBE'
        code, result = self.getData(url)
        if code==200:
            ts_json = json.loads(result)
        else:
            print code
            print result
        return ts_json
