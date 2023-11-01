class Line:

    tag = ""
    dirty = False
    valid = False

    def __init__(self):
        self.tag = ""
        self.dirty = False
        self.valid = True

    def rewrite_line(self, tag):
        self.tag = tag
        self.set_dirty()

    def set_dirty(self):
        self.dirty = True

    def set_clean(self):
        self.dirty = False

    def invalidate(self):
        self.valid = False

    def to_string(self) -> str:
        if self.tag == "":
            return ""
        else:
            return f'{self.tag} {"D" if self.dirty else " "} '
