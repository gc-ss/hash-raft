import json
from . import config
import random as random

class voteResult:

    term = None
    success = None

    def __init__(self, term, success):
        self.term = term
        self.success = success

class appendEntriesResult:

    term = None
    voteGranted = None

    def __init__(self, term, voteGranted):
        self.term = term
        self.voteGranted = voteGranted

class Raft:

    def __init__ (self, candidate, currentTerm, myLastLogIndex, myLastLogTerm):
        self.currentTerm = currentTerm
        self.candidate = candidate
        self.myLastLogIndex = myLastLogIndex
        self.myLastLogTerm = myLastLogTerm
        self.votedFor = None

        # Random heartbeat delay 150-300 ms recommended
        self.heartbeatTimeout = random.randint(150, 300)
        

    ####
    #  Would-be remotely invoked call for a node to vote for the requester. 
    #  TODO: Return statement should be a broadcast to all nodes
    ####
    def requestVote (self, term, candidateId, lastLogIndex, lastLogTerm):
        # Reply false if term < currentTerm
        if term < self.currentTerm:
            return voteResult(self.currentTerm, False)
        #If votedFor is null or candidateId, and candidate’s log is at least as up-to-date as receiver’s log, grant vote
        if (self.votedFor is None or self.votedFor == candidateId) and ((lastLogIndex == self.myLastLogIndex) and (lastLogTerm == self.myLastLogTerm)):
            self.votedFor = candidateId
            return voteResult(self.currentTerm, True)

    def appendEntries (self, term, leaderId, prevLogIndex, prevLogTerm, entries, leaderCommit):
        if term < self.currentTerm:
            return appendEntries(self.currentTerm, False)
        #TODO: Reply false if log doesn’t contain an entry at prevLogIndex whose term matches prevLogTerm
        #TODO: If an existing entry conflicts with a new one (same index but different terms), delete the existing entry and all that follow it 
        #TODO: Append any new entries not already in the log
        #TODO: If leaderCommit > commitIndex, set commitIndex = min(leaderCommit, index of last new entry)

    def load (self):
        with open(config.SAVEFILE, 'r') as f:
            data = json.load(f)
            self.currentTerm = data["currentTerm"]
            self.candidate = data["candidate"]
            self.myLastLogIndex = data["lastLogIndex"]
            self.myLastLogTerm = data["lastLogTerm"]
            self.votedFor = data["votedFor"]

    ####
    #  Based on Raft specs currentTerm, votedFor and log[] MUST be persisted BEFORE responding to RPC
    ####
    def save (self):
        with open(config.SAVEFILE, 'w') as f:
            data = {}
            data["currentTerm"] = self.currentTerm
            data["candidate"] = self.candidate
            data["lastLogIndex"] = self.myLastLogIndex
            data["lastLogTerm"] = self.myLastLogTerm
            data["votedFor"] = self.votedFor
            json.dump(data, f, indent=2) 

    def getCurrentTerm(self):
        return self.currentTerm

    def getVotedFor(self):
        return self.votedFor

