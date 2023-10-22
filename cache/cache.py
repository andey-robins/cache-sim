from cache.assoc_set import AssociativeSet
from cache.line import Line
import helpers.converters as conv
from enum import Enum
import math

class LookupResult(Enum):
    HIT = 1
    MISS = 2

class Cache:
    """
    Cache is a generic cache class that can be used as any level of cache. it
    supports being associated with an inner and outer cache to dispatch write 
    and read requests to related cache systems, and will behave as expected
    even in an absense of these related caches (i.e. it's fully functional and
    won't complain if there is only a single cache instantiated)
    """

    size = 0
    associativity = 0
    block_size = 0

    inner_cache = None
    outer_cache = None

    sets = []

    def __init__(self, size: int, associativity: int, block_size: int, outer: 'Cache' = None, inner: 'Cache' = None):
        """
        __init__ takes some config parameters and two optional
        related caches and constructs a memory hierarchy of caches in accordance with those
        arguments

        outer is for cache at a further level from the CPU (i.e. if this is L2, outer would be L3)
        inner is for cache at a closer level to the CPU (i.e. if this is L2, inner would be L1)
        """
        self.outer_cache = outer
        self.inner_cache = inner
        self.sets = []

        self.size = size
        self.associativity = associativity
        self.block_size = block_size

        set_count = size / (associativity * block_size)
        for i in range(int(set_count)):
            self.sets.append(AssociativeSet(associativity))

    def write(self, addr: str):
        tag, idx, _ = self.hex_addr_to_cache_idx(addr)

    def read(self, addr: str):
        tag, idx, _ = self.hex_addr_to_cache_idx(addr)

    def lookup(self, tag: int, idx: int) -> ['LookupResult', Line]:
        cache_set = self.sets[idx]
        return cache_set.lookup(tag)

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

