class Line:

    tag = ""
    dirty = False

    def __init__(self):
        self.tag = ""
        self.dirty = False

    def to_string(self) -> str:
        if self.tag == "":
            return ""
        else:
            return f'{self.tag} {"D" if self.dirty else " "} '