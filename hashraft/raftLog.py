
class logEntry:
    term = None
    commandKey = None
    commandValue = None
    committed = False

    def __init__(self, term, commandKey, commandValue):
        self.term = term
        self.commandKey = commandKey
        self.commandValue = commandValue
    
    def setCommitted(self, committed):
        self.committed = committed

class raftLog:

    logs = []
    currentIndex = 0
    commitIndex = 0
    currentTerm = None

    def __init__(self):
        pass
    
    ###
    # Raft defines committing as a majority of servers replying that they have added to their own logs. Committed status means log entries are safe to
    # move to state machine. Follower learn about commit status in AppendEntries RPC call from committedIndex attribute
    #####
    def commit (self, term, commandKey, commandValue):
        self.currentTerm = term
        logs.append(logEntry(term, commandKey, commandValue))

    #return current index (raft uses 1-index)
    def getCurrentRaftIndex(self):
        return self.index+1
    
    #return given raft index (raft uses 1-index)
    def getRaftIndex(self, index):
        return logs[index-1]

    #return last comitted raft index
    def getCommitRaftIndex(self):
        return self.commitIndex+1