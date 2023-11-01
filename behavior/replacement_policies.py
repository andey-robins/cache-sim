from cache.cache import Cache


def least_recently_used(c: 'Cache', tag: int, idx: int) -> (int, int):
    """
    least_recently_used will take a graph object and the tag and idx of the
    new block being put into cache and return the (tag, idx) of the block to
    be evicted. returns (-1, -1) if there is no victim block

    uses the LRU replacement policy to determine which cache line is being
    evicted
    """
    victim_set = c.sets[idx]


def first_in_first_out(c: 'Cache') -> (int, int):
    """
    least_recently_used will take a graph object and return the (tag, idx)
    of the block to be evicted. returns (-1, -1) if there is no victim block

    uses the FIFO replacement policy to determine which cache line is being
    evicted
    """
    pass
