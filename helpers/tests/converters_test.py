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
import converters

import unittest
import logging

# see this SO link https://stackoverflow.com/questions/7472863/pydev-unittesting-how-to-capture-text-logged-to-a-logging-logger-in-captured-o
# for info on injecting the logger into the unittest output capture space
logger = logging.getLogger()
logger.level = logging.DEBUG

class TestConverters(unittest.TestCase):
    def test_hex_str_to_bin_str(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        try:
            one = converters.hex_str_to_bin_str("1")
            self.assertEqual(one, "0"*31 + "1")
            f = converters.hex_str_to_bin_str("F")
            self.assertEqual(f, "0"*28 + "1111")
            ff = converters.hex_str_to_bin_str("FF")
            self.assertEqual(ff, "0"*24 + "1"*8)
        finally:
            logger.removeHandler(stream_handler)