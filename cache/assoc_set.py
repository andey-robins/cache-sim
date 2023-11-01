from cache.line import Line
from cache.enums import LookupResult
from behavior.enums import ReplacementPolicy
import sys


class AssociativeSet:
    """
    an AssociativeSet keeps track of a number of cache lines
    equal to the associativity of the set. it also tracks relevant
    datastructures for performing eviction
    """

    lines = []

    """
    0x400341a0
    Memory: 01000000000000110100000110100000
    Tag:    01000000000000110100000
    Index:  11010

    0xdfcfa8
    Memory: 110111111100111110101000
    Tag:    110111111100111
    Index:  11010

    The debug text has the tag listed in hex and the
    index in decimal -- NOT in hex, hex. As such, the index
    of 26 (dec) == 11010 (bin). Which, when we consider a block
    size of 16 (which takes 4 offset bits) are bits the 5th to
    10th least significant bits (1-indexed).
    """

    lru = []
    fifo = []

    def __init__(self, associativity):
        for i in range(associativity):
            self.lines.append(Line())
        self.lru = []
        self.fifo = []

    def lookup(self, tag: int) -> ('LookupResult', 'Line'):
        """
        lookup takes a tag and will go through the lines in the
        current set to see if one has a matching tag. It
        returns a LookupResult and a Line in a tuple. If the
        lookup was a miss, Line will be None. Otherwise the Line
        will be the relevant line in memory
        """
        for line in self.lines:
            if line.tag == tag:
                return LookupResult.HIT, line
        return LookupResult.MISS, None

    def allocate_block(self, addr: str, mode: 'ReplacementPolicy', outer_cache, debug: bool) -> 'Line':
        """
        allocate_block takes an address, a replacement policy, an outer cache, and a debug
        flag and performs the steps to allocate a block (evicting an appropriate one, 
        writing back if necessary, and reading from outer) before returning the cache line
        that has been allocated
        """
        # find the block to replace
        victim_line = self.select_line_for_eviction(mode)

        # perform a writeback if necessary
        if victim_line.dirty and victim_line.valid and outer_cache:
            outer_cache.write(addr, debug)

        # pull in block from higher level cache
        if outer_cache:
            outer_cache.read(addr, debug)

        # return block for writing in the main cache write method
        return victim_line

    def select_line_for_eviction(self, mode: 'ReplacementPolicy') -> 'Line':
        """
        evict_block takes a replacement policy option and invalidates the
        appropriate line according to that policy.

        Returns the line to be evicted
        """
        for line in self.lines:
            if not line.valid:
                # if the invalid line was in tracking somewhere, remove it
                # before we return that line
                if line.tag in self.lru:
                    self.lru.remove(line.tag)
                if line.tag in self.fifo:
                    self.fifo.remove(line.tag)

                return line

        victim_tag = ""

        # if there were no invalid lines to replace, use the appropriate
        # replacment policy datastructure to select one
        if mode == ReplacementPolicy.LRU:
            victim_tag = self.lru[0]
            self.lru = self.lru[1:]
        elif mode == ReplacementPolicy.FIFO:
            victim_tag = self.fifo[0]
            self.fifo = self.fifo[1:]

        for line in self.lines:
            if line.tag == victim_tag:
                return line

    def update_replacement_tracking(self, tag: int, mode: 'ReplacementPolicy') -> None:
        """
        update_replacement_tracking takes a line tag and a ReplacementPolicy mode
        and updates the appropriate datastructes in the set to maintain the
        replacement policy. This is a handy wrapper to prevent needing to check
        the specific policy everywhere we need to perfor updates in the cache.
        If an invalid 'mode' is provided, will fatally exit

        Returns nothing
        """
        if mode == ReplacementPolicy.LRU:
            self.update_lru(tag)
        elif mode == ReplacementPolicy.FIFO:
            self.update_fifo(tag)
        else:
            print("Fatal error, invalid replacement policy detected.")
            print(f"ReplacementPolicy={mode}")
            sys.exit()

    def update_lru(self, tag: int) -> None:
        """
        update_lru takes a tag and updates the LRU ordering for the set
        by moving the tag element to the end of the LRU list. The list
        is therefore sorted from least recently used to most recently
        used. On eviction, we remove the element at index 0

        The function has no return value
        """
        if tag in self.lru:
            self.lru.remove(tag)
        self.lru.append(tag)

    def update_fifo(self, tag: int) -> None:
        """
        update_fifo takes a tag and updates the fifo queue by adding
        the tag if it's not already in the queue and doing nothing
        otherwise.

        The function has no return value
        """
        if not tag in self.fifo:
            self.fifo.append(tag)

    def to_string(self) -> str:
        s = ""
        for line in self.lines:
            s += line.to_string()
        return s
