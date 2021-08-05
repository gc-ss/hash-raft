from .context import hashraft
from hashraft.util.eventlogger import EventLogger
import unittest
import threading

class LoggingTest (unittest.TestCase):

    def setUp (self):
        self.testLogger = EventLogger ()

    def tearDown (self):
        del self.testLogger

    def test_info (self):
        self.testLogger.info ("test message")
        self.assertIn ("test message", self.testLogger.getCurrentAsString ())
        self.assertIn ("INFO", self.testLogger.getCurrentAsString ())

    def test_warning (self):
        self.testLogger.warning ("test message")
        self.assertIn ("test message", self.testLogger.getCurrentAsString ())
        self.assertIn ("WARN", self.testLogger.getCurrentAsString ())
    
    def test_error (self):
        self.testLogger.error ("test message")
        self.assertIn ("test message", self.testLogger.getCurrentAsString ())
        self.assertIn ("ERRO", self.testLogger.getCurrentAsString ())
    
    def test_OKAY (self):
        self.testLogger.okay ("test message")
        self.assertIn ("test message", self.testLogger.getCurrentAsString ())
        self.assertIn ("OKAY", self.testLogger.getCurrentAsString ())

    def test_get_last (self):
        self.testLogger.error ("test message")
        self.testLogger.error ("last")
        self.assertIn ("last", self.testLogger.getLastEntry ())
        self.assertEqual ("[", self.testLogger.getLastEntryNoTime ()[0])

    def test_thread (self):
        testThread = threading.Thread (target=(lambda logger: logger.info ("in thread")), args=[self.testLogger])
        testThread.start ()
        self.testLogger.info ("out of thread")
        testThread.join ()

        log = self.testLogger.getCurrentAsString ()
        self.assertIn ("out of thread", log)
        self.assertIn ("in thread", log)

    