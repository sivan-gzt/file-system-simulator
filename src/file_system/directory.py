from src.file_system.constants import (
    PREFIX_DIRECTORY,
    ROOT,
    PATH_DELIMITER,
    TREE_BRANCH,
    TREE_LAST,
    TREE_SPACE,
    TREE_VERTICAL
)
from src.file_system.exceptions import (
    DuplicateNameError,
    NotFoundError
)
from src.file_system.node import FSNode
from src.file_system.linked_list import LinkedList

class Directory(FSNode):
    def __init__(self, name: str=ROOT): 
        super().__init__(name)
        self.children = LinkedList()
        self.size     = 0
        self.count    = 0
        
    def __str__(self):
        return (f"{PREFIX_DIRECTORY} " if self.parent else "") + super().__str__()
    
    def update_size(self, delta: int):
        """
        Updates the size of the directory
        """        
        self.size += delta
        if self.parent:
            self.parent.update_size(delta)
    
    def find_child(self, name: str) -> FSNode | None:
        if name == '':
            return self
        child = self.children.find(value=name, key=lambda x: x.name)
        if child is None:
            return None
        return child.data

    def add_child(self, child: FSNode, overwrite: bool = False) -> None:
        """
        Adds a child node to the directory.

        Args:
            child (FSNode): The child node to add.
            overwrite (bool): If True, overwrites an existing child with the same name.

        Raises:
            DuplicateNameError: If a child with the same name already exists and overwrite is False.
        """
        existing_child = self.find_child(child.name)
        if existing_child:
            if overwrite:
                self.update_size(-existing_child.size)  # Subtract the size of the existing child
                self.children.remove(existing_child)
            else:
                existing_child.parent.raise_error(DuplicateNameError, name=child.name, directory=self.name)
        self.count += 1
        child.parent = self
        self.children.append(child)
        self.update_size(child.size)  # Add the size of the new child
        
    
    def remove_child(self, name: str) -> None:
        """
        Removes a child node by name.

        Args:
            name (str): The name of the child to remove.

        Raises:
            NotFoundError: If the child does not exist.
        """
        child = self.find_child(name)
        if child is None:
            self.raise_error(NotFoundError, name=name, directory=self.name)

        self.children.remove(child)
        self.count -= 1
        self.update_size(-child.size)  # Subtract the size of the removed child

    def list(self, prefix: str = "", is_last: bool = True, recurse: bool = False) -> str:
        """
        Produces a tree-formatted directory
        """
        # for root directory no prefix is used
        buffer = f"{str(self)}{PATH_DELIMITER}\n"
        if self.parent is None:
            child_prefix = ""  # no indentation for the first level under root
        else:
            marker       = TREE_LAST if is_last else TREE_BRANCH
            buffer       = f"{prefix}{marker}" + buffer
            child_prefix = prefix + (TREE_SPACE if is_last else TREE_VERTICAL)
        
        for is_last, child in self.children.enumrate():
            # if at root don't add extra indent to children
            new_prefix = child_prefix if self.parent is not None else ""
            
            if hasattr(child, "list") and recurse:
                buffer += child.list(prefix=new_prefix, is_last=is_last, recurse=recurse)
            else:
                marker  = TREE_LAST if is_last else TREE_BRANCH
                buffer += f"{new_prefix}{marker}{str(child)}{PATH_DELIMITER if isinstance(child, Directory) else ''}\n"
        
        return buffer

    def get_absolute_path(self) -> str:
        """
        returns the absolute path of the directory

        Returns:
            str: The absolute path of the directory.
        """        
        if self.parent is None:
            return self.name
        
        return super().get_absolute_path()