from hashraft.util import config
from hashraft.util.Exceptions import *
from hashraft.util.config import ConfigFactory
from .server import RaftServer
from timeit import default_timer as timer
from hashraft.util.LoggingLevel import LoggingLevel

import threading
import socket as so
import sys
import os.path


configuration = []
runningNodes = []
nodeThreads = []
DEFAULTCONFIG = "raftConfig.yaml"

def quit (*args):
    raise TerminalQuit

def start (logger, *args):
    if len (configuration) == 0:
        logger.warning ("No raft configuration set.", True)
        return
    if len (runningNodes) > 0:
        logger.warning ("A raft configuration is currently running.", True)
        return 

    logger.info ("Attempting to start raft configuration...", True)
    for node in configuration:
        try:
            startEvent = threading.Event ()
            thread = threading.Thread (target=node.start, daemon=True, args=[startEvent])
            thread.start ()
            if not startEvent.wait (1):
                return 
            startEvent.clear ()
            nodeThreads.append (thread)
            runningNodes.append (node)
            logger.okay ("Started server for node: " + str(node.name) + " [" + node.addressStr + "]", True)
        except Exception as e:
            logger.error ("Unable to start server for node: " + str(node.name) + " [" + node.addressStr + "]", True)
            terminate (logger)
            return

    logger.okay ("Raft configuration started successfully.", True)

def create (logger, *args):

    
    #Attempt Default Configuration File
    if os.path.isfile (DEFAULTCONFIG):
        logger.okay ("Default [" + str(DEFAULTCONFIG) + "] Configuration File Detected", True)
        file = DEFAULTCONFIG
    else:
        file = input ("Please enter a config file: ") if len (args) == 0 else args[0]

    try:
        raftDict = ConfigFactory.create (file).parse ()
    except Exception as e:
        logger.warning (str(e), True)
        return


    if raftDict["logging"]["level"]["root"] is not None:
        try:
            logger.setLevel(LoggingLevel[raftDict["logging"]["level"]["root"]])
            logger.okay("Logging level set to "  + logger.getLevel(), True)
        except Exception as e:
            logger.warning (str(e), True)
            return

    configuration.clear ()
    for k,v in raftDict["nodes"].items():
        configuration.append (RaftServer (k, v["ip"], v["port"], logger))   

    logger.okay ("Raft configuration set.", True)

def terminate (logger):
    try: 
        for node in runningNodes:
            socket = so.socket ()
            socket.connect ((node.ip, node.port))
            socket.send (str.encode ("stop"))
            logger.okay ("Termination request sent for node: " + node.name + "[" + node.addressStr + "]", True)
            socket.recv (2)
            socket.shutdown (so.SHUT_RDWR)
            socket.close ()
    except:
        logger.error ("A unknown server termination error occured.", True)
        socket.close ()
        logger.dump ()
        sys.exit ()
    nodeThreads.clear ()
    runningNodes.clear ()

def status (logger, *args):
    if len (runningNodes) == 0:
        logger.info ("No raft configuration is running.", True)
        return
    try:
        for node in runningNodes:
            socket = so.socket ()
            socket.connect ((node.ip, node.port))
            start = timer ()
            socket.send (str.encode ("status"))
            socket.recv (2)
            end = timer ()
            ping = round (((end-start) * 1000), 2)
            if ping > 500: logger.warning (node.name + " responded in " + str(ping) + "ms", True)
            else: logger.info (node.name + " responded in " + str(ping) + "ms", True)
            socket.close ()
    except KeyboardInterrupt:
        print ()
        logger.warning ("Status was interrupted.", True) 
    except BaseException as e:
        print (sys.exc_info()[0])



def help (*args):
    print ("\n   Below is a list of commands and a brief description:")
    print ("      create | Takes a file and creates a new raft configuration.")
    print ("      start  | Starts the current raft configuration.")
    print ("      status | Lists the status of the current running nodes.")
    print ("      quit   | Ends the current temrinal session.")
    print ()



