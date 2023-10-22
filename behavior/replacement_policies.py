from cache.cache import Cache

def least_recently_used(c: 'Cache') -> (int, int):
    """
    least_recently_used will take a graph object and return the (tag, idx)
    of the block to be evicted. returns (-1, -1) if there is no victim block

    uses the LRU replacement policy to determine which cache line is being
    evicted
    """
    pass

def first_in_first_out(c: 'Cache') -> (int, int):
    """
    least_recently_used will take a graph object and return the (tag, idx)
    of the block to be evicted. returns (-1, -1) if there is no victim block

    uses the FIFO replacement policy to determine which cache line is being
    evicted
    """
    pass