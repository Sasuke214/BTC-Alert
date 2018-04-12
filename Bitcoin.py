import requests
import demjson
import time
import pyglet
import threading
import re



class Miner:
    def __init__(self):
        #The value above which we tends to earn profit
        self.medianValueForProfit=6910

        #Current Status
        self.mining=True
        self.currentStatus="Mining"

        #Loading the alter into memory
        self.alert=pyglet.media.load('yousuffer.mp3',streaming=False)

    def output(self):
        print("UDS:{}\nTime:{}\n".format(self.b_usd,self.b_time))
        self.playTune()

    def getData(self):
        #Retrieve the data from json which is obtained from api
        tempUSD=self.jsonData['bpi']['USD']['rate']
        self.b_usd=float(re.sub('[,]','',tempUSD))
        
        #Time of data retrieval
        self.b_time=self.jsonData['time']['updated']

    def getResponse(self):
        #Getting the response from api providing url        
        self.response=requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')

        #Converting response to json
        self.jsonData=self.response.json()
        self.getData()

        #If it's not efficient for mining just change the status to idle and alert user
        if self.b_usd<=self.medianValueForProfit and self.mining:
            self.mining=False
            self.currentStatus="Idle"
            
            #Display the output
            threading.Thread(target=self.output).start()
        
        #If it's time then change the status to mining 
        elif self.b_usd>self.medianValueForProfit and self.mining!=True:
            self.mining=True
            self.currentStatus="Mining"

            #Display the output
            threading.Thread(target=self.output).start()

        #Display current status and rate
        print(self.currentStatus+' '+str(self.b_usd))

    '''Play the alert'''
    def playTune(self):
        self.alert.play()

    '''Main Controller'''
    def controller(self):
        while True:
            self.getResponse()
            time.sleep(2)
        
            
m=Miner()
threading.Thread(target=m.controller).start()
pyglet.app.run()


