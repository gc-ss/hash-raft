from .context import hashraft
from hashraft.util.logging.logger import Logger
import unittest
import threading

class LoggingTest (unittest.TestCase):

    def setUp (self):
        self.testLogger = Logger ()

    def tearDown (self):
        del self.testLogger

    def test_info (self):
        self.testLogger.info ("test message")
        self.assertIn ("test message", self.testLogger.getCurrentAsString ())
        self.assertIn ("INFO", self.testLogger.getCurrentAsString ())

    def test_warning (self):
        self.testLogger.warning ("test message")
        self.assertIn ("test message", self.testLogger.getCurrentAsString ())
        self.assertIn ("WARNING", self.testLogger.getCurrentAsString ())
    
    def test_error (self):
        self.testLogger.error ("test message")
        self.assertIn ("test message", self.testLogger.getCurrentAsString ())
        self.assertIn ("ERROR", self.testLogger.getCurrentAsString ())

    def test_thread (self):
        testThread = threading.Thread (target=(lambda logger: logger.info ("in thread")), args=[self.testLogger])
        testThread.start ()
        self.testLogger.info ("out of thread")
        testThread.join ()

        log = self.testLogger.getCurrentAsString ()
        self.assertIn ("out of thread", log)
        self.assertIn ("in thread", log)

    