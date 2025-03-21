from datetime import datetime
from file_system import PREFIX_FILE, FSNode

class File(FSNode):
    
    def __init__(self, name: str, content: str=''):
        super().__init__(name)
        self._content = content
        self.size = len(content)
        self.rtime = None
        
    def __len__(self):
        return self.size
    
    def __str__(self):
        return f"{PREFIX_FILE} " + super().__str__()
    
    def __getattr__(self, name):
        if name == 'content':
            return ''
        return super().__getattr__(name)
    
    def __update_content(self, data: str):
        self._content = data
        self.size = len(data)
        super().modify()
        
    def write(self, data: str):
        self.__update_content(data)
    
    def append(self, data: str):
        self.__update_content(self._content + data)

    def read(self) -> tuple[str, int]:
        """
        Reads and returns file content

        Returns:
            tuple[str, int]: _description_
        """        
        self.rtime = datetime.now()
        return self._content, len(self)
    
    