class FSNode:
    def __init__(self, name, parent=None):
        self.name   = name
        self.parent = parent

    def get_parent(self):
        return self.parent