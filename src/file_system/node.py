from __future__ import annotations
from datetime import datetime
from src.file_system.constants import PATH_DELIMITER
from .validation import validate_name

class FSNode:
    """
    Simulates a file or directory
    """    
    def __init__(self, name: str, parent=None):
        """
        Initializes an entity representing a file or directory.

        Args:
            name (str): name of entity, validated by validate_name()
            parent (Directory, optional): Parent of entity. Defaults to None.
        """            
        self.entity_type = self.__class__.__name__
        self.validate(name)
        self.name   = name
        self.parent = parent
        self.ctime  = datetime.now()
        self.mtime  = self.ctime
        
    def __str__(self):
        return f"{self.name}"

    def modify(self):
        self.mtime = datetime.now()

    def validate(self, name: str):
        """
        Calls the validator function

        Args:
            name (str): name to be validated
        """        
        validate_name(self.entity_type, name)

    def rename(self, new_name: str):
        """
        Renames the node with validation

        Args:
            new_name (str): new name
        """        
        self.validate(new_name)
        self.name = new_name

    def get_absolute_path(self):
        path = [self.name]
        current = self.parent
        while current:
            path.append(current.name)
            current = current.parent
        
        return PATH_DELIMITER + PATH_DELIMITER.join(reversed(path))
    