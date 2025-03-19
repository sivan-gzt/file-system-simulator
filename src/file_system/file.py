from file_system.node import FSNode
import datetime

class File(FSNode):
    def __init__(self, name, parent=None, content=''):
        super().__init__(name, parent)
        self.content = content
        self.ctime = datetime.now()
        

    def rename(self, name):
        self.name = name
    
    