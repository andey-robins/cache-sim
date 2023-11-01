from enum import Enum


class ReplacementPolicy(Enum):
    LRU = 1
    FIFO = 2


class InclusionProperty(Enum):
    INCLUSIVE = 1
    NONINCLUSIVE = 2
    EXCLUSIVE = 3
