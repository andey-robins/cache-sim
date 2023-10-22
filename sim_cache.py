import sys
import helpers.parsing as parsers
from cache.cache import *
from behavior import inclusion_properties, replacement_policies

def cli_driver():
    global debug
    config = parsers.arg_parser(sys.argv)

    print(f'===== Simulator configuration =====')
    print(f'BLOCKSIZE:{" "*13}{config["block_size"]}')
    print(f'L1_SIZE:{" "*15}{config["l1_size"]}')
    print(f'L1_ASSOC:{" "*14}{config["l1_assoc"]}')
    print(f'L2_SIZE:{" "*15}{config["l2_size"]}')
    print(f'L2_ASSOC:{" "*14}{config["l2_assoc"]}')
    print(f'REPLACEMENT POLICY:    {"LRU" if config["replacement_policy"] == replacement_policies.least_recently_used else "FIFO"}')
    print(f'INCLUSION PROPERTY:    {"non-inclusive" if config["inclusion_property"] == inclusion_properties.non_inclusive else "inclusive"}')
    print(f'trace_fille:{" "*11}{config["trace_file"]}')

    cache = Cache(config['l1_size'], config['l1_assoc'], config['block_size'])


if __name__ == "__main__":
    global debug
    debug = True
    cli_driver()
