import threading
from datetime import datetime
from termcolor import colored

class EventLogger:
    
    def __init__ (self):
        self.mutex = threading.Lock ()
        self.dataLog = []

    def info (self, message, *args):
        self.mutex.acquire ()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.dataLog.append (date + " [INFO] " + str(message))
        if args: print ("   " + self.getLastEntryNoTime ())
        self.mutex.release ()
    
    def warning (self, message, *args):
        self.mutex.acquire ()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.dataLog.append (date + " [" + colored ("WARN", "yellow") + "] " + str(message))
        if args: print ("   " + self.getLastEntryNoTime ())
        self.mutex.release ()
    
    def error (self, message, *args):
        self.mutex.acquire ()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.dataLog.append (date + " [" + colored ("ERRO", "red") + "] " + str(message))
        if args: print ("   " + self.getLastEntryNoTime ())
        self.mutex.release ()
    
    def okay (self, message, *args):
        self.mutex.acquire ()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.dataLog.append (date + " [" + colored ("OKAY", "green") + "] " + str(message))
        if args: print ("   " + self.getLastEntryNoTime ())
        self.mutex.release ()

    def getCurrent (self):
        return self.dataLog
    
    def getCurrentAsString (self):
        return ''.join(self.dataLog)
    
    def getLastEntry (self):
        return str(self.dataLog[-1])
    
    def getLastEntryNoTime (self):
        return str(self.dataLog[-1][20:])
   
    def dump (self):
        self.mutex.acquire ()
        print ()
        for entry in self.dataLog:
            print (entry)
        self.dataLog = []
        self.mutex.release ()