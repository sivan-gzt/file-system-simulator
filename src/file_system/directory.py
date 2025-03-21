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
from src.file_system.file import File
from src.file_system.linked_list import LinkedList

class Directory(FSNode):
    def __init__(self, name: str = ROOT): 
        super().__init__(name)
        self.children = LinkedList()
        self.count = 0  # Track the number of children

    def __str__(self):
        return (f"{PREFIX_DIRECTORY} " if self.parent else "") + super().__str__()

    def find_child(self, name: str) -> FSNode | None:
        if name == '':
            return self
        child = self.children.find(value=name, key=lambda x: x.name)
        if child is None:
            return None
        return child.data

    def add_child(self, node: FSNode, overwrite: bool = False) -> None:
        """
        Adds a child node to the directory and updates modification time.

        Args:
            node (FSNode): The child node to add.
            overwrite (bool): If True, overwrites an existing child with the same name.

        Raises:
            DuplicateNameError: If a child with the same name already exists and overwrite is False.
        """
        existing_child = self.find_child(node.name)
        if existing_child is not None:
            if overwrite:
                if isinstance(existing_child, File) and isinstance(node, File):
                    existing_child.write(node.content)  # Overwrite content
                    self.modify()  # Update the modification time
                    return
                else:
                    self.children.remove(existing_child)
                    self.update_size(-existing_child.size)  # Trigger size propagation
                    self.count -= 1
            else:
                self.raise_error(DuplicateNameError, name=node.name, directory=self.name)

        self.children.append(node)
        node.parent = self
        self.update_size(node.size)  # Trigger size propagation
        self.count += 1
        self.modify()

    def remove_child(self, name: str) -> bool:
        """
        Removes a child node by name and updates modification time.

        Args:
            name (str): The name of the child to remove.

        Returns:
            bool: True if the child was successfully removed.

        Raises:
            NotFoundError: If the child does not exist.
        """
        child = self.find_child(name)
        if child is None:
            self.raise_error(NotFoundError, name=name, directory=self.name)

        self.children.remove(child)
        self.update_size(-child.size)  # Trigger size propagation
        self.count -= 1
        self.modify()
        return True

    def list(self, prefix: str = "", is_last: bool = True, recurse: bool = False) -> str:
        """
        Produces a tree-formatted directory using a recursive approach.
        """
        # For root directory, no prefix is used
        buffer = f"{str(self)}{PATH_DELIMITER}\n"
        if self.parent is None:
            child_prefix = ""  # No indentation for the first level under root
        else:
            marker = TREE_LAST if is_last else TREE_BRANCH
            buffer = f"{prefix}{marker}" + buffer
            child_prefix = prefix + (TREE_SPACE if is_last else TREE_VERTICAL)
        
        for is_last, child in self.children.enumerate():
            # If at root, don't add extra indent to children
            new_prefix = child_prefix if self.parent is not None else ""
            
            if hasattr(child, "list") and recurse:
                buffer += child.list(prefix=new_prefix, is_last=is_last, recurse=recurse)
            else:
                marker = TREE_LAST if is_last else TREE_BRANCH
                buffer += f"{new_prefix}{marker}{str(child)}{PATH_DELIMITER if isinstance(child, Directory) else ''}\n"
        
        return buffer

    def get_absolute_path(self) -> str:
        """
        Returns the absolute path of the directory.

        Returns:
            str: The absolute path of the directory.
        """        
        if self.parent is None:
            return self.name
        
        return super().get_absolute_path()