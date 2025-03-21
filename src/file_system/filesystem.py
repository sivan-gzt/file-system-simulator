from src.file_system.constants import PATH_DELIMITER
from src.file_system.exceptions import DuplicateNameError,  FileSystemError, NotADirectoryError
from src.file_system.directory import Directory
from src.file_system.file import File
from src.file_system.path_resolver import PathResolver


class FileSystem:
    """
    Simulates a file system with basic operations like mkdir, touch, ls, and read.
    """
    def __init__(self):
        """
        Initializes the file system with a root directory.
        """
        self.root = Directory()
        self.current: Directory = self.root

    def ls(self, recurse: bool = False) -> str:
        """
        Lists the contents of the current directory.

        Args:
            recurse (bool): If True, recursively list subdirectories.

        Returns:
            str: A string representation of the directory contents.
        """
        return self.current.list(recurse=recurse)
    
    def mkdir(self, *paths: str) -> None:
        """
        Creates one or more directories, including parent directories if necessary.

        Args:
            *paths (str): One or more directory paths to create. Paths can be nested (e.g., "a/b/c").

        Raises:
            DuplicateNameError: If a directory or file with the same name already exists.
            NotADirectoryError: If a path component is not a directory.
        """
        for path in paths:
            current = self.current  # Start from the current directory
            components = path.split(PATH_DELIMITER)

            for component in components:
                if not component:  # Skip empty components (e.g., from leading/trailing slashes)
                    continue

                child = current.find_child(component)
                if not child:
                    # Create the directory if it doesn't exist
                    new_dir = Directory(component)
                    current.add_child(new_dir)
                    current = new_dir
                elif isinstance(child, Directory):
                    # Navigate into the existing directory
                    current = child
                else:
                    # Raise an error if the path component is not a directory
                    current.raise_error(NotADirectoryError, name=component, directory=current.name)

    def read(self, path: str) -> str:
        """
        Reads the content of a file.

        Args:
            path (str): The path to the file.

        Returns:
            str: The content of the file, or None if the file does not exist.

        Raises:
            NotFoundError: If the file does not exist.
            NotADirectoryError: If the path points to a directory instead of a file.
        """
        target = PathResolver.resolve(self, path, must_exist=True)
        if not isinstance(target, File):
            target.raise_error(FileSystemError, f"Cannot read: '{path}' is not a valid file.")
        return target._content
    
    def touch(self, *paths: str, content: str = '') -> None:
        """
        Creates one or more files, including parent directories if necessary.
        Supports appending or overwriting content for existing files.

        Args:
            *paths (str): One or more file paths to create. Paths can be nested (e.g., "a/b/c.txt").
            content (str, optional): The content to write to the file. Defaults to an empty string.
            append (bool): If True, appends content to an existing file. Defaults to False.
            overwrite (bool): If True, overwrites content of an existing file. Defaults to False.

        Raises:
            NotADirectoryError: If a path component is not a directory.
        """
        if not paths:
            self.current.raise_error(FileSystemError, "touch: missing file operand")

        for path in paths:
            parent, file_name = PathResolver.resolve_parent(self, path)

            # Check if the file already exists
            try:
                parent.add_child(File(name=file_name, content=content))
            except DuplicateNameError:
                existing_file = parent.find_child(file_name)
                if isinstance(existing_file, File):
                    parent.size -= len(existing_file)
                    existing_file.write(content)
                    parent.size += len(existing_file)
                else:
                    self.current.raise_error(DuplicateNameError, name=file_name, directory=parent.name)
    
    def pwd(self, recurse) -> str:
        return self.current.get_absolute_path() if recurse else str(self.current)
    
    def write(self, path: str, content: str, overwrite: bool = False) -> None:
        """
        Writes to a file. Supports appending content.

        Args:
            path (str): The path to the file.
            content (str): The content to write to the file.
            append (bool): If True, appends content to the file. Defaults to False.

        Raises:
            NotFoundError: If the file does not exist.
            NotADirectoryError: If the path points to a directory instead of a file.
        """
        target = PathResolver.resolve(self, path, must_exist=True)

        if not isinstance(target, File):
            self.current.raise_error(NotADirectoryError, name=target.name, directory=self.current.name)

        target.parent.size -= len(target)
        if overwrite:
            target.write(content)
        else:
            target.append(content)
        target.parent.size += len(target)
    
    def del_(self, path: str, recurse: bool = False) -> None:
        """
        Deletes a file or directory.

        Args:
            path (str): The path to the file or directory to delete.
            recurse (bool): If True, recursively delete subdirectories.

        Raises:
            NotFoundError: If the path does not exist.
            NotADirectoryError: If attempting to delete a directory without the recurse flag.
        """
        target = PathResolver.resolve(self, path, must_exist=True)

        if isinstance(target, Directory):
            if recurse:
                # Recursively delete all children
                while len(target.children) > 0:
                    child = target.children.head.data  # Get the first child
                    target.remove_child(child.name)  # Remove the child (recursive call)
                # Remove the directory itself
                target.parent.remove_child(target.name)
            else:
                target.raise_error(FileSystemError, f"Cannot delete: '{path}' is a directory. Use -R to delete directories.")
        else:
            # If it's a file, simply remove it
            target.parent.remove_child(target.name)
    
    def cd(self, path: str) -> bool:
        """
        Changes the current directory.

        Args:
            path (str): The path to change to.

        Returns:
            bool: True if the directory change is successful, False otherwise.

        Raises:
            NotFoundError: If the path does not exist.
            NotADirectoryError: If the target is not a directory.
        """
        target = PathResolver.resolve(self, path, must_exist=True)
        if not isinstance(target, Directory):
            target.raise_error(NotADirectoryError, name=target.name, directory=self.current.name)
        self.current = target
        return True
    
    def size(self, path: str):
        """
        Get the size of a file or directory.

        Args:
            path (str): The path to the file or directory.

        Returns:
            int: The size of the file or directory in bytes.

        Raises:
            NotFoundError: If the path does not exist.
        """
        target = PathResolver.resolve(self, path, must_exist=True)
        return target.size