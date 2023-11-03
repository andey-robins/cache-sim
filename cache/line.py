class Line:

    address = ""
    tag = 0
    dirty = False
    valid = False

    def __init__(self):
        self.tag = 0
        self.address = ""
        self.dirty = False
        self.valid = False

    def rewrite_line(self, tag: int, idx: int, addr: str, dirty: bool):
        """
        update a line item in the cache set to a new block
        takes a tag, index, address, and dirty flag and updates
        the state of the line item.

        returns nothing. dirty should only be set when we're writing to the line
        not when we need to re-allocate and read the line
        """
        self.tag = tag
        self.index = idx
        self.address = addr
        self.valid = True

        if dirty:
            self.set_dirty()
        else:
            self.set_clean()

    def set_dirty(self):
        self.dirty = True

    def set_clean(self):
        self.dirty = False

    def invalidate(self):
        self.rewrite_line(0, self.index, "", False)
        self.valid = False

    def to_string(self) -> str:
        if self.tag == 0:
            return ""
        else:
            return f'{hex(self.tag)[2:]} {"D" if self.dirty else " "} '

    def to_eviction_string(self) -> str:
        """
        the formatting of the line when we do an eviction is more than just the tag
        so we need to add all that info and put it into a string for display in the
        debugging output
        """
        if self.tag == 0:
            return ""
        else:
            return f'{self.address[:-1] + "0"} (tag {hex(self.tag)[2:]}, index {self.index}, {"dirty" if self.dirty else "clean"})'
