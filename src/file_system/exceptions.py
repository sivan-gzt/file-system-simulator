class InvalidNameError(Exception):
    """
    Exception raised for invalid names.
    
    Attributes:
        name (str): The invalid name.
        reason (str): Explanation of why the name is invalid.
    """
    def __init__(self, name: str, reason: str):
        self.name = name
        self.reason = reason
        message = f"Invalid name '{name}': {reason}"
        super().__init__(message)

class DuplicateNameError(Exception):
    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
        message = f"'{name}' already exists in {directory}"
        super().__init__(message)