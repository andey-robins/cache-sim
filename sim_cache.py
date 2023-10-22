import sys
import helpers.parsing as parsers
from cache.cache import *
from behavior import inclusion_properties, replacement_policies
from cache.enums import Command

debug = True

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
    print(f'trace_file:{" "*12}{config["trace_file"].split("/")[-1]}')

    l1_cache = Cache(config['l1_size'], config['l1_assoc'], config['block_size'], "L1")
    l2_cache = Cache(config['l2_size'], config['l2_assoc'], config['block_size'], "L2")

    if l2_cache.size != 0:
        l1_cache.add_outer_cache(l2_cache)
        l2_cache.add_inner_cache(l1_cache)

    commands = parsers.parse_commands_from_file(config['trace_file'])

    for i, command in enumerate(commands):
        command_num = i+1
        op, addr = command[0], command[1][:-1] # must slice off \n
        if debug:
            print('-'*40)
            print(f'# {command_num} : {"write" if op == Command.WRITE else "read"} {addr}')
        
        if op == Command.READ:
            l1_cache.read(addr, debug=debug)
        if op == Command.WRITE:
            l1_cache.write(addr, debug=debug)


    print("===== L1 contents =====")
    l1_cache.print_contents()
    if l2_cache.size != 0:
        print("===== L2 contents =====")
        l2_cache.print_contents()

if __name__ == "__main__":
    # rather than overriding the logging class, we're going to just use a global
    # debug variable to enable/disable debugging output since the assignment
    # requires very specific output formatting and it would take more time than
    # its worth to override the logging formats appropriately
    cli_driver()
