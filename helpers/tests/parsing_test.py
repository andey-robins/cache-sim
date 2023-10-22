# python must be in the same working dir to import test files
# we must change the dir to be able to import the file
# and we must do it relative to the file's location if
# we want to be able to run the unittest command from other
# directories
import sys
import os

script_dir = os.path.dirname(__file__)
module_dir = os.path.join(script_dir, "..")
sys.path.append(module_dir)
import parsing
sys.path.append(os.path.join(module_dir, "..", "cache"))
from cache.enums import Command

import unittest
import logging

# see this SO link https://stackoverflow.com/questions/7472863/pydev-unittesting-how-to-capture-text-logged-to-a-logging-logger-in-captured-o
# for info on injecting the logger into the unittest output capture space
logger = logging.getLogger()
logger.level = logging.DEBUG

class TestParser(unittest.TestCase):
    def test_command_parser(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        try:
            c = ["r deadbeef", "w deadbeef", "r feedface"]
            parse_res = parsing.command_parser(c)
            self.assertEqual(parse_res[0], (Command.READ, "deadbeef"))
            self.assertEqual(parse_res[1], (Command.WRITE, "deadbeef"))
            self.assertEqual(parse_res[2], (Command.READ, "feedface"))
        finally:
            logger.removeHandler(stream_handler)