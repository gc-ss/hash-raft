from hashraft.util.eventlogger import EventLogger
import sys

def interactive (logger):
    logger.info ("Started in interactive")
    while (True):
        userInput = input (">> ")
        logger.info ("User Input: \"" + userInput + "\"")
        if userInput == "quit":
            return
        

def quickstart (logger, arguments):
    logger.info ("Started with arguments")
    logger.info (arguments)


if __name__ == '__main__':
    logger = EventLogger ()
    arguments = sys.argv[1:]

    if len(arguments) > 0:
        quickstart (logger, arguments)
    else:
        interactive (logger)

    logger.warning ("Terminated!")
    logger.error ("Testing")
    logger.dump ()
    