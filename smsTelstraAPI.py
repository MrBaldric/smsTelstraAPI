#used to send sms messages using Telstra API


import pycurl, certifi, time
from StringIO import StringIO
from urllib import urlencode

message = ''            #<place message string here>
number = ''             #<add Australian mobile number string here>
myConsumerKey= ''       #<added registered ConsumerKey string here>
mySecret = ''           #<add secret key string here>

def storeDatafile(number,message):
    sCurrentDate = time.strftime("%Y-%m-%d",time.localtime((time.time())))
    sCurrentTime = time.strftime("%H:%M:%S",time.localtime((time.time())))
    storeData = open('smsLog.txt','a')		
    storeData.write("{}\t{}\tsms sent to :\t{} with message = \t{}\n".format(sCurrentDate,sCurrentTime,number,message))	
    storeData.close()				

def getToken(myKey,mySec):
    buffer = StringIO()
    h = ['Content-Type: application/x-www-form-urlencoded']
    d = {'client_id':'{}'.format(myKey),'client_secret':'{}'.format(mySec),'grant_type':'client_credentials','scope':'SMS'}
    str1 = 'client_id={}&client_secret={}&grant_type=client_credentials&scope=SMS'.format(myConsumerKey,mySecret)
    c = pycurl.Curl()
    c.setopt(c.VERBOSE, True)
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.URL, "https://api.telstra.com/v1/oauth/token")
    c.setopt(c.HTTPHEADER, h)
    c.setopt(c.POSTFIELDS, str1)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue().split('"')
    return body


def sendSms(number,token,message):
    buffer = StringIO()
    h = ['Content-Type: application/json','Authorization: Bearer {}'.format(token)]
    str2 = '{\"to\":\"' + number + '\", \"body\":\"' + message + '\"}'
    c = pycurl.Curl()
    c.setopt(c.VERBOSE, True)
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.URL, "https://api.telstra.com/v1/sms/messages")
    c.setopt(c.HTTPHEADER, h)
    c.setopt(c.POSTFIELDS, str2)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    return body
    
token = getToken(myConsumerKey,mySecret)
result = sendSms(number,token[3],message)
storeDatafile(number,message)


