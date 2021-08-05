# Unit Testing Package for Hash Raft

## How to run
In a terminal with Python 3 installed, navigate to this projects root directory. 
Enter the command: `python3 -m tests.run` in your terminal.

## How to add your own unit tests
    1. Create a new file under `/tests`, name if after the file you would like to test.
    2. Add the import statement `from .context import hashraft` to your new file.
    3. Add an import statement for the file(s) that you wish to test. If you wish to test the event logger, you might write `from hashraft.util.eventlogger import EventLogger`
    4. Add an import statement for unittest: `import unittest`
    5. Create a new class, named however you'd like, that inherits `unittest.TestCase`. For example: `class Name (unittest.TestCase):`
    6. Each class method you add becomes it's own unit test. If you need class wide set up and tear down you can define that by implementing the `setUp (self)` and `tearDown (self)` methods. 
    7. Add your class name to the `test_classes` list in `run.py`.

## What is currently tested
    - EventLogger
    