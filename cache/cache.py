class Cache:
    """
    Cache is a generic cache class that can be used as any level of cache. it
    supports being associated with an inner and outer cache to dispatch write 
    and read requests to related cache systems, and will behave as expected
    even in an absense of these related caches (i.e. it's fully functional and
    won't complain if there is only a single cache instantiated)
    """

    inner_cache = None
    outer_cache = None

    contents = {}

    def __init__(self, config: dict, outer: 'Cache' = None, inner: 'Cache' = None):
        """
        __init__ takes a config object (generated from the argument parser) and two optional
        related caches and constructs a memory hierarchy of caches in accordance with those
        arguments

        outer is for cache at a further level from the CPU (i.e. if this is L2, outer would be L3)
        inner is for cache at a closer level to the CPU (i.e. if this is L2, inner would be L1)
        """
        self.outer_cache = outer
        self.inner_cache = inner
        self.contents = {}