from datetime import datetime
from src.file_system.constants import PREFIX_FILE
from src.file_system.node import FSNode

class File(FSNode):
    
    def __init__(self, name: str, content: str = ''):
        super().__init__(name)
        self._content = content  # Privatize the content attribute
        self.update_size(len(content))  # Initialize size based on content
        
    @property
    def size(self) -> int:
        """
        Returns the size of the file based on its content.
        """
        return len(self._content)
    
    @property
    def content(self) -> str:
        """
        Provides read-only access to the file's content.
        """
        return self._content

    def __str__(self):
        return f"{PREFIX_FILE} " + super().__str__()
    
    def __getattr__(self, name):
        if name == 'content':
            return ''
        return super().__getattr__(name)
    
    def write(self, content: str, overwrite: bool = True):
        """
        Writes content to the file. Updates size dynamically and modification time.
        """
        if overwrite:
            size_difference = len(content) - len(self._content)  # Calculate size difference before overwriting
            self._content = content  # Replace the content entirely
        else:
            size_difference = len(content)  # Appending adds the full length of the new content
            self._content += content  # Append the new content

        self.update_size(size_difference)  # Trigger size propagation
        self.modify()  # Update the modification time
    
    def append(self, data: str):
        """
        Appends data to the file.
        """
        self.write(data, overwrite=False)

    def read(self) -> tuple[str, int]:
        """
        Reads and returns file content.

        Returns:
            tuple[str, int]: The content and its size.
        """        
        self.rtime = datetime.now()
        return self._content, len(self._content)

