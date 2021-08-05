class TerminalQuit (Exception):
    pass

def quit (*args):
    raise TerminalQuit

def start (logger):
    n = input ("With how many nodes?: ")
    logger.info ("Attempting to start with " + str(n) + " nodes...")
    # logger.okay ("Started with " + str(n) + " nodes.")
    logger.error ("Failed to start!")
    print (logger.getLastEntryNoTime())

def help (*args):
    print ("\nBelow is a list of commands and a brief description:")
    print ("\tstart | unimplemented")
    print ("\tquit  | Ends the current temrinal session.")
    print ()

