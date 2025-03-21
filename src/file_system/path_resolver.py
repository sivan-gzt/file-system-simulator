from src.file_system.constants import ROOT, PATH_DELIMITER
from src.file_system.exceptions import NotFoundError, NotADirectoryError
from src.file_system.node import FSNode
from src.file_system.directory import Directory

class PathResolver:
    """
    Helper class for resolving paths in the file system.
    """

    @staticmethod
    def resolve(fs, path: str, must_exist: bool = True) -> FSNode:
        """
        Resolves a path to a file or directory node.

        Args:
            fs (FileSystem): The file system instance.
            path (str): The path to resolve.
            must_exist (bool): If True, raises an error if the path does not exist.

        Returns:
            FSNode: The resolved node.

        Raises:
            NotFoundError: If the path does not exist and must_exist is True.
            NotADirectoryError: If a path component is not a directory.
        """
        # Determine if the path is absolute or relative
        if path.startswith(ROOT):
            current = fs.root  # Start from the root for absolute paths
        else:
            current = fs.current  # Start from the current directory for relative paths

        # Traverse the path components
        parts = path.split(PATH_DELIMITER)
        for part in parts:
            if part == "." or part == "":  # Skip current directory and empty components
                continue  # Stay in the current directory
            elif part == "..":
                if current.parent is None:
                    current.raise_error(NotFoundError, name="..", directory=ROOT)
                current = current.parent  # Move to the parent directory
            elif part == ROOT:
                current = fs.root
            else:
                child = current.find_child(name=part)
                if child is None and must_exist:
                    current.raise_error(NotFoundError, name=part, directory=current.name)
                elif not must_exist:
                    return current  # Return the last valid directory if must_exist is False
                
                if isinstance(child, Directory):
                    current = child  # Move into the directory
                else:
                    if part == parts[-1]:  # Last component can be a file
                        return child
                    current.raise_error(NotADirectoryError, name=part, directory=current.name)

        return current

    @staticmethod
    def resolve_parent(fs, path: str) -> tuple[Directory, str]:
        """
        Resolves the parent directory of a given path and the final component.

        Args:
            fs (FileSystem): The file system instance.
            path (str): The path to resolve.

        Returns:
            (Directory, str): The parent directory and the final component of the path.

        Raises:
            NotFoundError: If the parent directory does not exist.
            NotADirectoryError: If a path component is not a directory.
        """
        parts = path.split(PATH_DELIMITER)
        parent_path = PATH_DELIMITER.join(parts[:-1])  # Get the parent directory path
        final_component = parts[-1]  # Get the final component (file or directory name)

        parent = PathResolver.resolve(fs, parent_path, must_exist=True)
        if not isinstance(parent, Directory):
            parent.raise_error(NotADirectoryError, name=parent.name, directory=parent_path)

        return parent, final_component