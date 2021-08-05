import threading
from datetime import datetime

class EventLogger:
    
    def __init__ (self):
        self.mutex = threading.Lock ()
        self.dataLog = []

    def info (self, message):
        self.mutex.acquire ()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.dataLog.append ("[INFO] " + date + " " + message)
        self.mutex.release ()
    
    def warning (self, message):
        self.mutex.acquire ()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.dataLog.append ("[WARNING] " + date + " " + message)
        self.mutex.release ()
    
    def error (self, message):
        self.mutex.acquire ()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.dataLog.append ("[ERROR] " + date + " " + message)
        self.mutex.release ()

    def getCurrent (self):
        return self.dataLog
    
    def getCurrentAsString (self):
        return ''.join(self.dataLog)
   
    def dump (self):
        self.mutex.acquire ()
        for entry in self.dataLog:
            print (entry)
        self.dataLog = []
        self.mutex.release ()