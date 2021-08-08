from hashraft.util.eventlogger import EventLogger
from hashraft.util.Exceptions import *
import hashraft.api as api
import threading
import sys

def interactive (logger):
    logger.info ("Started in interactive")
    while (True):
        try:
            userInput = input (">> ").strip ().split (" ")
            logger.info ("User Input: \"" + str(userInput) + "\"")
            try:
                exec ("api." + userInput[0] + "(logger" +  ((", "+ str(userInput[1:])[1:-1] + ")") if len (userInput) > 1 else ")"))
            except Exception as e:
                if type(e) is TerminalQuit: return
                else: 
                    logger.warning ("Unknown Command: \"" + userInput[0] + "\"")

        except KeyboardInterrupt:
            print ()
            logger.warning ("Exiting on keyboard interrupt.")
            return 

def quickstart (logger, arguments):
    logger.info ("Started with arguments: " + str(arguments))
    api.create (logger, arguments[0])
    api.start (logger)
    interactive (logger)

if __name__ == '__main__':
    logger = EventLogger ()
    arguments = sys.argv[1:]

    if len(arguments) > 0:
        quickstart (logger, arguments)
    else:
        interactive (logger)

    api.terminate (logger)
    logger.warning ("Finished.")
    logger.dump ()    