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
        logger.warning ("No raft configuration set.")
        return
    if len (runningNodes) > 0:
        logger.warning ("A raft configuration is currently running.")
        return 

    logger.info ("Attempting to start raft configuration...")
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
            logger.okay ("Started server for node: " + str(node.name) + " [" + node.addressStr + "]")
        except Exception as e:
            logger.error ("Unable to start server for node: " + str(node.name) + " [" + node.addressStr + "]")
            terminate (logger)
            return

    logger.okay ("Raft configuration started successfully.")

def create (logger, *args):

    #Attempt Default Configuration File
    if os.path.isfile (DEFAULTCONFIG):
        logger.okay ("Default [" + str(DEFAULTCONFIG) + "] Configuration File Detected")
        file = DEFAULTCONFIG
    else:
        file = input ("Please enter a config file: ") if len (args) == 0 else args[0]

    try:
        raftDict = ConfigFactory.create (file).parse ()
    except Exception as e:
        logger.warning (str(e))
        return


    if raftDict["logging"]["level"]["root"] is not None:
        try:
            logger.setLevel(LoggingLevel[raftDict["logging"]["level"]["root"]])
            logger.okay("Logging level set to "  + logger.getLevel())
        except Exception as e:
            logger.warning (str(e))
            return

    configuration.clear ()

    for k,v in raftDict["nodes"].items():
        print (v)
        configuration.append (RaftServer (k, v["ip"], v["port"], raftDict["nodes"], logger))   


    logger.okay ("Raft configuration set.")

def terminate (logger):
    try: 
        for node in runningNodes:
            socket = so.socket ()
            socket.connect ((node.ip, node.port))
            socket.send (str.encode ("stop"))
            logger.okay ("Termination request sent for node: " + node.name + "[" + node.addressStr + "]")
            socket.recv (2)
            socket.shutdown (so.SHUT_RDWR)
            socket.close ()
    except:
        logger.error ("A unknown server termination error occured.")
        socket.close ()
        logger.dump ()
        sys.exit ()
    nodeThreads.clear ()
    runningNodes.clear ()

def status (logger, *args):
    if len (runningNodes) == 0:
        logger.info ("No raft configuration is running.")
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
            if ping > 500: logger.warning (node.name + " responded in " + str(ping) + "ms")
            else: logger.info (node.name + " responded in " + str(ping) + "ms")
            socket.close ()
    except KeyboardInterrupt:
        print ()
        logger.warning ("Status was interrupted.") 
    except BaseException as e:
        print (sys.exc_info()[0])

def check (logger, *args):
    if len(args) != 2:
        logger.error ("Incorrect number of arguments.")
    try:
        ip = None
        port = None
        toCheck = None
        for node in runningNodes:
            if node.name == args[0]:
                ip = node.ip
                port = node.port
            if node.name == args[1]:
                toCheck = node.name
            if ip != None and toCheck != None:
                socket = so.socket ()
                socket.connect ((ip, port))
                socket.send ( str.encode ("check " + toCheck))
                stat = socket.recv (1024).decode ()
                if stat == "good":
                    logger.okay ("Good!")
                else:
                    logger.warning ("Not Good!")
                socket.close ()
                return
    except BaseException as e:
        print (sys.exc_info()[0])

def help (*args):
    print ("\n   Below is a list of commands and a brief description:")
    print ("      create | Takes a file and creates a new raft configuration.")
    print ("      start  | Starts the current raft configuration.")
    print ("      status | Lists the status of the current running nodes.")
    print ("      check  | Takes two node names as arguments and has the first one call the second one to check connections.")
    print ("      quit   | Ends the current temrinal session.")
    print ()



