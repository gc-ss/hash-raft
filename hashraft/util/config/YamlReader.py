from .ConfigReader import ConfigReader
import yaml

class YamlReader (ConfigReader):

    def __init__ (self, file):
        super ().__init__ (file)

    # Overriden Method
    def parse (self):
        with open(self.file, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError:
                raise Exception ("An error occured while parsing a yaml config file.")
