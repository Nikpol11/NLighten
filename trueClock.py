from adafruit_datetime import datetime

class trueClock():
    def __init__(self, storedTime):
        self.storedTime = datetime.fromisoformat(storedTime)
        self.storedEpoch = datetime.now()
        self.currentTime = self.storedTime+(datetime.now()-self.storedEpoch)
        
    def getTime(self):
        self.updateTime()
        return self.currentTime
    
    def updateTime(self):
        self.currentTime = self.storedTime+(datetime.now()-self.storedEpoch)
        
    def storeTime(self, storedTime):
        self.storedTime = datetime.fromisoformat(storedTime)
        self.storedEpoch = datetime.now()
        self.updateTime()
