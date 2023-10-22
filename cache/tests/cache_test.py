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
from cache.cache import Cache

import unittest
import logging

# see this SO link https://stackoverflow.com/questions/7472863/pydev-unittesting-how-to-capture-text-logged-to-a-logging-logger-in-captured-o
# for info on injecting the logger into the unittest output capture space
logger = logging.getLogger()
logger.level = logging.DEBUG

class TestCache(unittest.TestCase):
    def test_hex_addr_to_cache_idx(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        try:
            d0_cache = Cache(
                size=1024, 
                associativity=2, 
                block_size=16
            )

            tag, idx, off = d0_cache.hex_addr_to_cache_idx("400341a0")
            self.assertEqual(tag, 2097568)
            self.assertEqual(idx, 26)
            tag, idx, off = d0_cache.hex_addr_to_cache_idx("dfcfa8")
            self.assertEqual(tag, 28647)
            self.assertEqual(idx, 26)
            tag, idx, off = d0_cache.hex_addr_to_cache_idx("7b034dd4")
            self.assertEqual(tag, 4030886)
            self.assertEqual(idx, 29)
        finally:
            logger.removeHandler(stream_handler)