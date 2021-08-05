
from .YamlReader import YamlReader
from ..Exceptions import InvalidExtension
import os.path

def create (file):

    if not os.path.isfile (file):
        raise FileNotFoundError ("Config file: \"" + str(file) + "\" was not found.")

    name, extension =  file.split('.')

    if extension == "yaml":
        return YamlReader (file)
    else: 
        raise InvalidExtension