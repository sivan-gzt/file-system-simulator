from file_system.node import FSNode

class File(FSNode):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)