from __future__ import annotations
from datetime import datetime
from .node import FSNode

class File(FSNode):
    
    def __init__(self, name: str, parent=None, content: str=''):
        super().__init__(name, parent)
        self.content = content
        self.size = len(content)
        self.rtime = None
        
    def __len__(self):
        return self.size
    
    # def __str__(self):
    #     return super().__str__() + f" ({self.entity_type})"

    def __update_content(self, data: str):
        self.content = data
        self.size = len(data)
        super().modify()
        
    def write(self, data: str):
        self.__update_content(data)
    
    def append(self, data: str):
        self.__update_content(self.content + data)

    def read(self) -> tuple[str, int]:
        """
        Reads and returns file content

        Returns:
            tuple[str, int]: _description_
        """        
        self.rtime = datetime.now()
        return self.content, len(self)
    
    