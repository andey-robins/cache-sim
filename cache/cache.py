from cache.assoc_set import AssociativeSet
from cache.line import Line
from cache.enums import LookupResult
from behavior.enums import ReplacementPolicy, InclusionProperty
import helpers.converters as conv
import math
import sys


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

    replacement_policy = 0
    inclusion_property = 0

    stats = {}

    def __init__(self, size: int, associativity: int, block_size: int, rep_policy: 'ReplacementPolicy', inc_property: 'InclusionProperty', name: str):
        """
        __init__ takes some config parameters and two optional
        related caches and constructs a memory hierarchy of caches in accordance with those
        arguments
        """
        self.sets = []
        self.stats = {
            'reads': 0,
            'writes': 0,
            'read_misses': 0,
            'write_misses': 0,
            'write_backs': 0
        }

        self.size = size
        self.associativity = associativity
        self.block_size = block_size
        self.name = name

        self.inner_cache = None
        self.outer_cache = None

        self.replacement_policy = rep_policy
        self.inclusion_property = inc_property

        if associativity == 0 or block_size == 0:
            return

        set_count = size / (associativity * block_size)
        for i in range(int(set_count)):
            self.sets.append(AssociativeSet(associativity, self.name))

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
        self.stats['writes'] += 1

        tag, idx, _ = self.hex_addr_to_cache_idx(addr)

        if debug:
            print(
                f'{self.name} write : {addr[:-1] + "0"} (tag {hex(tag)[2:]}, index {idx})')

        res, line = self.lookup(tag, idx, debug=debug)
        # select victim set
        victim_set = self.sets[idx]

        if res == LookupResult.HIT:
            line.set_dirty()
        elif res == LookupResult.MISS:
            self.stats['write_misses'] += 1
            # perform the eviction of our victim to an outer cache
            victim_line, did_wb = victim_set.allocate_block(
                addr, self.replacement_policy, self.inclusion_property, self.inner_cache, self.outer_cache, debug)

            # if the allocation required a writeback, track that in stats
            if did_wb:
                self.stats['write_backs'] += 1

            # place the newly fetched block into the victim slot in the set
            victim_line.rewrite_line(tag, idx, addr, dirty=True)

        # update replacement policy tracking information regardless of whether
        # there was a cache hit or cache miss initially
        victim_set.update_replacement_tracking(
            tag, self.replacement_policy)

        print(f'{self.name} update {"LRU" if self.replacement_policy == ReplacementPolicy.LRU else "FIFO"}')
        print(f'{self.name} set dirty')

    def read(self, addr: str, debug: bool):
        self.stats['reads'] += 1

        tag, idx, _ = self.hex_addr_to_cache_idx(addr)

        if debug:
            print(
                f'{self.name} read : {addr[:-1] + "0"} (tag {hex(tag)[2:]}, index {idx})')

        res, line = self.lookup(tag, idx, debug=debug)
        # select victim set
        victim_set = self.sets[idx]

        if res == LookupResult.HIT:
            pass
        elif res == LookupResult.MISS:
            self.stats['read_misses'] += 1
            # perform the eviction of our victim to an outer cache
            victim_line, did_wb = victim_set.allocate_block(
                addr, self.replacement_policy, self.inclusion_property, self.inner_cache, self.outer_cache, debug)

            # if the allocation required a writeback, track that in stats
            if did_wb:
                self.stats['write_backs'] += 1

            # place the newly fetched block into the victim slot in the set
            victim_line.rewrite_line(tag, idx, addr, dirty=False)
        else:
            print(
                f'A fatal error occured. LookupResult={res} encountered. Quitting.')
            sys.exit()

        victim_set.update_replacement_tracking(
            tag, self.replacement_policy)

        print(f'{self.name} update {"LRU" if self.replacement_policy == ReplacementPolicy.LRU else "FIFO"}')

    def lookup(self, tag: int, idx: int, debug: bool) -> ('LookupResult', Line):
        cache_set = self.sets[idx]
        res, line = cache_set.lookup(tag)

        if debug:
            print(
                f'{self.name} {"hit" if res == LookupResult.HIT and line.tag == tag else "miss"}')

        return res, line

    def back_invalidate_if_present(self, addr: str, debug: bool) -> None:
        # if we're trying to back invalidate an empty line, there's nothing
        # to invalidate, so return early
        if addr == "":
            return

        tag, idx, _ = self.hex_addr_to_cache_idx(addr)
        victim_set = self.sets[idx]
        res, victim_line = self.lookup(tag, idx, False)
        if res == LookupResult.HIT:
            if debug:
                print(f'{self.name} invalidated: {victim_line.to_eviction_string()}')
            victim_line.invalidate()

            # once we invalidate, remove from the replacement datastructures
            if self.replacement_policy == ReplacementPolicy.LRU and victim_line.tag in victim_set.lru:
                victim_set.lru.remove(victim_line.tag)
            elif self.replacement_policy == ReplacementPolicy.FIFO and victim_line.tag in victim_set.fifo:
                victim_set.fifo.remove(victim_line.tag)

            if victim_line.dirty:
                print("L1 writeback to main memory directly")
            #     self.stats['writes'] += 1

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
        set_id = int(
            "".join(reversed(addr[offset_len:(offset_len+sets_len)])), 2)
        tag = int("".join(reversed(addr[(offset_len+sets_len):])), 2)

        return [tag, set_id, offset]
