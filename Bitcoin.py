import requests
import demjson
import time
import pyglet
import threading
import re



class Miner:
    def __init__(self):
        self.medianValueForProfit=6910
        self.mining=True
        self.currentStatus="Mining"
        
        self.alert=pyglet.media.load('yousuffer.mp3',streaming=False)

    def output(self):
        print("UDS:{}\nTime:{}\n".format(self.b_usd,self.b_time))
        self.playTune()

    def getData(self):
        tempUSD=self.jsonData['bpi']['USD']['rate']
        self.b_usd=float(re.sub('[,]','',tempUSD))
        self.b_time=self.jsonData['time']['updated']

    def getResponse(self):
        
        self.response=requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        self.jsonData=self.response.json()
        self.getData()
        
        if self.b_usd<=self.medianValueForProfit and self.mining:
            self.mining=False
            self.currentStatus="Idle"
            threading.Thread(target=self.output).start()

        elif self.b_usd>self.medianValueForProfit and self.mining!=True:
            self.mining=True
            self.currentStatus="Mining"
            threading.Thread(target=self.output).start()
            
        print(self.currentStatus+' '+str(self.b_usd))
            
    def playTune(self):
        self.alert.play()
        
    def controller(self):
        while True:
            self.getResponse()
            time.sleep(2)
        
            
m=Miner()
threading.Thread(target=m.controller).start()
pyglet.app.run()


