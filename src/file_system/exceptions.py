class FileSystemError(Exception):
    """Base class for file system-related exceptions."""
    def __init__(self, reason: str):
        """
        Args:
            reason (str): The reason for the error.
        """
        self.reason = reason
        super().__init__(reason)  # Explicitly call the base class initializer

    def __str__(self):
        return f"[{self.__class__.__name__}] {self.reason}"


class InvalidNameError(FileSystemError):
    """Exception raised for invalid names."""
    def __init__(self, name: str, reason: str):
        """
        Args:
            name (str): The invalid name.
            reason (str): Explanation of why the name is invalid.
        """
        self.name = name
        super().__init__(reason)


class DuplicateNameError(InvalidNameError):
    """Exception raised for duplicate names in a directory."""
    def __init__(self, name: str, directory: str):
        """
        Args:
            name (str): The duplicate name.
            directory (str): The directory where the duplication occurred.
        """
        self.directory = directory
        reason = f"'{name}' already exists in directory '{directory}'"
        super().__init__(name, reason)


class NotADirectoryError(FileSystemError):
    """Exception raised when a path component is not a directory."""
    def __init__(self, name: str, directory: str):
        """
        Args:
            name (str): The name of the invalid path component.
            directory (str): The directory where the error occurred.
        """
        self.name = name
        self.directory = directory
        reason = f"'{name}' is not a directory in '{directory}'"
        super().__init__(reason)



class NotFoundError(FileSystemError):
    """Exception raised when a file is not found."""
    def __init__(self, name: str, directory: str):
        """
        Args:
            name (str): The name of the file.
            directory (str): The directory where the file was expected.
        """
        self.name = name
        self.directory = directory
        reason = f"File '{name}' not found in directory '{directory}'"
        super().__init__(reason)
