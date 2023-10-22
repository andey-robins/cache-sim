from cache.assoc_set import AssociativeSet
from cache.line import Line
from cache.enums import LookupResult
import helpers.converters as conv
import math

class Cache:
    """
    Cache is a generic cache class that can be used as any level of cache. it
    supports being associated with an inner and outer cache to dispatch write 
    and read requests to related cache systems, and will behave as expected
    even in an absense of these related caches (i.e. it's fully functional and
    won't complain if there is only a single cache instantiated)
    """
    global debug

    size = 0
    associativity = 0
    block_size = 0

    inner_cache = None
    outer_cache = None

    sets = []
    name = "GenericCache"

    def __init__(self, size: int, associativity: int, block_size: int, name: str):
        """
        __init__ takes some config parameters and two optional
        related caches and constructs a memory hierarchy of caches in accordance with those
        arguments
        """
        self.sets = []

        self.size = size
        self.associativity = associativity
        self.block_size = block_size
        self.name = name

        if associativity == 0 or block_size == 0:
            return

        set_count = size / (associativity * block_size)
        for i in range(int(set_count)):
            self.sets.append(AssociativeSet(associativity))

    def add_outer_cache(self, related_cache: 'Cache'):
        """
        outer is for cache at a further level from the CPU (i.e. if this is L2, outer would be L3)
        """
        self.outer_cache = related_cache

    def add_inner_cache(self, related_cache: 'Cache'):
        """
        inner is for cache at a closer level to the CPU (i.e. if this is L2, inner would be L1)
        """
        self.inner_cache = related_cache

    def write(self, addr: str, debug: bool):
        tag, idx, _ = self.hex_addr_to_cache_idx(addr)

        if debug:
            print(f'{self.name} write : {addr}, (tag {hex(tag)[2:]}, index {idx})')

        res, line = self.lookup(tag, idx)
        if res == LookupResult.MISS:
            # TODO: write allocation and writeback
            # must find a victim and allocate the block
            # invoke replacement policy to determine which line we evict
            # if victim, update blocks based on inclusion property
            pass

    def read(self, addr: str, debug: bool):
        tag, idx, _ = self.hex_addr_to_cache_idx(addr)

        if debug:
            print(f'{self.name} read : {addr}, (tag {hex(tag)[2:]}, index {idx})')

        res, line = self.lookup(tag, idx, debug=debug)
        

    def lookup(self, tag: int, idx: int, debug: bool) -> ('LookupResult', Line):
        cache_set = self.sets[idx]
        res, line = cache_set.lookup(tag)

        if debug:
            print(f'{self.name} {"hit" if res == LookupResult.HIT else "miss"}')

        return res, line

    def print_contents(self):
        """
        print_contents will output the entire contents of this cache
        by invoking the to_string method on each set (which also invokes
        to_string() on each line in the set). Formatting is consistent with
        the memory outputs at the end of test files
        """
        # if the cache has size 0, there is nothing to print
        if self.size == 0:
            return
        
        for set_id in range(len(self.sets)):
            print(f'Set     {set_id}:\t{self.sets[set_id].to_string()}')

    def hex_addr_to_cache_idx(self, addr: str) -> [int, int, int]:
        """
        hex_addr_to_cache_idx will take a string representation
        of an address (in hex encoding) and convert it into a binary
        string before slicing into the three pieces [tag, set, offset]

        These three values are returned after being converted from
        bin back to decimal integers (for easy comparison in sets)
        """
        offset_len = int(math.log2(self.block_size))
        sets_len = int(math.log2(len(self.sets)))

        # convert from hex to bin and MSB to LSB
        addr = "".join(reversed(conv.hex_str_to_bin_str(addr)))

        # we convert back from LSB to MSB with the reversed, then
        # have to convert from a reversed object to a string with join
        offset = int("".join(reversed(addr[:offset_len])), 2)
        set_id = int("".join(reversed(addr[offset_len:(offset_len+sets_len)])), 2)
        tag = int("".join(reversed(addr[(offset_len+sets_len):])), 2)

        return [tag, set_id, offset]

