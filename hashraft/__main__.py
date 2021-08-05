from hashraft.util.eventlogger import EventLogger

if __name__ == '__main__':
    logger = EventLogger ()
    logger.warning ("started!")
    logger.error ("Ending!")
    logger.dump ()
    