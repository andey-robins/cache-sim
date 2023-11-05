import sys
import helpers.parsing as parsers
from cache.cache import *
from cache.enums import Command
from behavior.enums import ReplacementPolicy, InclusionProperty

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
    print(
        f'REPLACEMENT POLICY:    {"LRU" if config["replacement_policy"] == ReplacementPolicy.LRU else "FIFO"}')
    print(
        f'INCLUSION PROPERTY:    {"non-inclusive" if config["inclusion_property"] == InclusionProperty.NONINCLUSIVE else "inclusive"}')
    print(f'trace_file:{" "*12}{config["trace_file"].split("/")[-1]}')

    # initialize two levels of VCache
    l1_cache = Cache(config['l1_size'], config['l1_assoc'],
                     config['block_size'], config["replacement_policy"], config["inclusion_property"], "L1")
    l2_cache = Cache(config['l2_size'], config['l2_assoc'],
                     config['block_size'], config["replacement_policy"], config["inclusion_property"], "L2")

    # only associate the two VCaches if the second one is in use
    if l2_cache.size != 0:
        l1_cache.add_outer_cache(l2_cache)
        l2_cache.add_inner_cache(l1_cache)

    commands = parsers.parse_commands_from_file(config['trace_file'])

    for i, command in enumerate(commands):
        # input(f"Press enter to execute the next command - {command}")
        # must slice off \n since we split on ' ' <space> not '\n'
        op, addr = command[0], command[1][:-1]

        if i + 1 == 63568:
            input()

        if debug:
            command_num = i+1  # numbers in output are 1-indexed
            print('-'*40)
            print(
                f'# {command_num} : {"write" if op == Command.WRITE else "read"} {addr}')

        # dispatch commands to the VCache
        if op == Command.READ:
            l1_cache.read(addr, debug=debug)
        if op == Command.WRITE:
            l1_cache.write(addr, debug=debug)

    print("===== L1 contents =====")
    l1_cache.print_contents()
    if l2_cache.size != 0:
        print("===== L2 contents =====")
        l2_cache.print_contents()

    # calculate some meta-stats using the collected stats
    l1_mr = (l1_cache.stats['read_misses'] + l1_cache.stats['write_misses']
             ) / (l1_cache.stats['reads'] + l1_cache.stats['writes'])
    l2_mr = 0
    mem_traffic = l1_cache.stats['read_misses'] + \
        l1_cache.stats['write_misses'] + l1_cache.stats['write_backs']

    if l2_cache.size != 0:
        l2_mr = (l2_cache.stats['read_misses']
                 ) / (l2_cache.stats['reads'])
        mem_traffic = l2_cache.stats['read_misses'] + \
            l2_cache.stats['write_misses'] + l2_cache.stats['write_backs']

    print(f"===== Simulation results (raw) =====")
    print(f'a. number of L1 reads:        {l1_cache.stats["reads"]}')
    print(f'b. number of L1 read misses:  {l1_cache.stats["read_misses"]}')
    print(f'c. number of L1 writes:       {l1_cache.stats["writes"]}')
    print(f'd. number of L1 write misses: {l1_cache.stats["write_misses"]}')
    print('e. L1 miss rate:              %.6f' % l1_mr)
    print(f'f. number of L1 writebacks:   {l1_cache.stats["write_backs"]}')
    print(f'g. number of L2 reads:        {l2_cache.stats["reads"]}')
    print(f'h. number of L2 read misses:  {l2_cache.stats["read_misses"]}')
    print(f'i. number of L2 writes:       {l2_cache.stats["writes"]}')
    print(f'j. number of L2 write misses: {l2_cache.stats["write_misses"]}')
    print('k. L2 miss rate:              %.6f' %
          l2_mr if l2_mr != 0 else 'k. L2 miss rate:              0')
    print(f'l. number of L2 writebacks:   {l2_cache.stats["write_backs"]}')
    print(f'm. total memory traffic:      {mem_traffic}')


if __name__ == "__main__":
    # rather than overriding the logging class, we're going to just use a global
    # debug variable to enable/disable debugging output since the assignment
    # requires very specific output formatting and it would take more time than
    # its worth to override the logging formats appropriately
    cli_driver()
