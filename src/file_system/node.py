from datetime import datetime
from src.file_system.linked_list.linked_list import LinkedList
from src.file_system.constants import PATH_DELIMITER
from .validation import validate_name

class FSNode:
    """
    Simulates a file or directory
    """    
    def __init__(self, name: str):
        """
        Initializes an entity representing a file or directory.

        Args:
            name (str): name of entity, validated by validate_name()
            parent (FSNode, optional): Parent of entity. Defaults to None.
        """            
        self.entity_type = self.__class__.__name__
        self.validate(name)
        self.name   = name
        self.ctime  = datetime.now()
        self.mtime  = self.ctime
        
    def __str__(self):
        return self.name

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

    def __getattr__(self, name):
        """
        Fallback for missing attributes.

        Args:
            name (str): The name of the attribute being accessed.

        Returns:
            Any: The value of the attribute, or None if it's 'parent'.
        """
        if name == 'parent':
            return None
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def get_absolute_path(self):
        path    = LinkedList(self.name)
        current = self.parent
        while current:
            path.append(current.name)
            current = current.parent
        
        return PATH_DELIMITER.join(path.reversed())

    def raise_error(self, exception_class, **kwargs):
        """
        Utility method to raise an exception with context.

        Args:
            exception_class (type): The exception class to raise.
            **kwargs: Additional context for the exception.
        """
        raise exception_class(**kwargs)