import sys
import helpers.parsing as parsers
from cache.cache import *


def cli_driver():
    config = parsers.arg_parser(sys.argv)
    print(config)
    cache = Cache(config)


if __name__ == "__main__":
    cli_driver()
