from hashraft.util.eventlogger import EventLogger
import hashraft.terminal as tm
import sys

def interactive (logger):
    logger.info ("Started in interactive")
    while (True):
        try:
            userInput = input (">> ")
            logger.info ("User Input: \"" + userInput + "\"")
            try:
                exec ("tm." + userInput + "(logger)")
            except Exception as e:
                if type(e) is tm.TerminalQuit: return
                else: 
                    logger.warning ("Unknown Command: \"" + userInput + "\"")
                    print (logger.getLastEntryNoTime ())
        except KeyboardInterrupt:
            print ()
            logger.warning ("Exiting on keyboard interrupt.")
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

    logger.warning ("Finished.")
    logger.dump ()
    