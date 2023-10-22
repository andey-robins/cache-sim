from cache.line import Line
from cache.lookup_result import LookupResult

class AssociativeSet:

    """
    an AssociativeSet keeps track of a number of cache lines
    equal to the associativity of the set
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

    def __init__(self, associativity):
        for i in range(associativity):
            self.lines.append(Line())

    def lookup(self, tag: int) -> ['LookupResult', Line]:
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