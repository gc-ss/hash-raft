from .context import hashraft
from hashraft.raft import Raft
import unittest
import threading


class raftTest (unittest.TestCase):

    def setUp (self):
        self.raftClient1 = Raft (1,2,1,1)
        
    def tearDown (self):
        del self.raftClient1
        

    #Succesful request for vote to node 1 for node 2
    def test_votePass (self):
        result = self.raftClient1.requestVote (3, 2, 1, 1)
        self.assertTrue(result.voteGranted)

    def test_votedFor(self):
        result = self.raftClient1.requestVote (3, 2, 1, 1)
        self.assertTrue(self.raftClient1.getVotedFor() == 2)

    def test_currentTerm(self):
        self.assertTrue(self.raftClient1.getCurrentTerm() == 2)
        
        
    #Unsuccesful request for vote to node 1 for node 2
    def test_voteFail_wrong_term (self):
        result = self.raftClient1.requestVote (1, 2, 1, 1)
        self.assertFalse(result.voteGranted)

    def test_save_load (self):
        self.raftClient1.save()
        del self.raftClient1
        self.raftClient1 = Raft(0,0,0,0)
        self.assertTrue(self.raftClient1.getCurrentTerm() == 0)
        self.raftClient1.load()
        self.assertTrue(self.raftClient1.getCurrentTerm() == 2)
    