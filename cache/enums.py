from enum import Enum

class LookupResult(Enum):
    HIT = 1
    MISS = 2

class Command(Enum):
    READ = 1
    WRITE = 2