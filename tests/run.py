import unittest
from .loggingTest import LoggingTest
import pkgutil


test_classes = [LoggingTest]

def suite ():
    loader = unittest.TestLoader ()
    suite = unittest.TestSuite ()

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase (test_class)
        suite.addTests (tests)

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner ()
    runner.run (suite ())