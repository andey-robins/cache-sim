import sys
import behavior.replacement_policies as rps
import behavior.inclusion_properties as ips
from pathlib import Path

def try_convert(value, default, *types):
    """
    https://stackoverflow.com/questions/12451531/python-try-catch-block-inside-lambda

    type conversion attempt, returns default if unable to convert
    """
    for t in types:
        try:
            return t(value)
        except (ValueError, TypeError):
            continue
    return default

def arg_parser(args) -> dict:
    """
    validate arguments are provided through the CLI and
    have the form of <BLOCKSIZE> <L1_SIZE> <L1_ASSOC>
    <L2_SIZE> <L2_ASSOC> <REPLACEMENT_POLICY>
    <INCLUSION_PROPERTY> <trace_file>

    Where all arguments are positive integers except
    trace_file:
        BLOCKSIZE: block size in bytes
        L1_SIZE: L1 size in bytes
        L1_ASSOC: L1 set-associativity
        L2_SIZE: L2 size in bytes. 0 -> no L2 cache present
        L2_ASSOC: 
        REPLACEMENT_POLICY: 0=LRU; 1=FIFO
        INCLUSION_PROPERTY: 0=non-inclusive; 1=inclusive
        trace_file: string: full name of trace file
    """
    parsed_args = {}
    
    positive_integer = lambda i_str: try_convert(i_str, 0, int)

    for i, e in enumerate(["block_size", "l1_size", "l1_assoc", "l2_size", "l2_assoc", "replacement_policy", "inclusion_property", "trace_file"]):
        # 0 is the filename in sys.argv, so we need to offset by 1
        arg_idx = i+1

        if i == 0:
            block_size = positive_integer(args[arg_idx])
            if block_size == 0:
                print("Invalid block size. Please try again.")
                sys.exit()
            parsed_args[e] = block_size
        elif i == 1 or i == 3:
            # size
            cache_size = positive_integer(args[arg_idx])
            parsed_args[e] = cache_size
        elif i == 2 or i == 4:
            # assoc
            associativity = positive_integer(args[arg_idx])
            parsed_args[e] = associativity
        elif i == 5:
            # replacement policy
            policy_number = positive_integer(args[arg_idx])
            parsed_args[e] = rps.first_in_first_out if policy_number == 1 else rps.least_recently_used
        elif i == 6:
            # inclusion property
            inclusion_number = positive_integer(args[arg_idx])
            parsed_args[e] = ips.inclusive if inclusion_number == 1 else ips.non_inclusive
        elif i == 7:
            # trace_file
            parsed_args[e] = Path(args[arg_idx])
        else:
            print("Too many arguments encountered. Please try again.")
    return parsed_args