from abc import ABC, abstractmethod

class ConfigReader (ABC):
    def __init__ (self, file):
        self.file = file
    
    @abstractmethod
    def parse (self):
        pass