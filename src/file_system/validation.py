import re

from file_system import MAX_LENGTH_NAME, InvalidNameError

def validate_name(entity_type, name):
    """
    Validates a name for a filesystem entity (File or Directory).
    
    Parameters:
        entity_type (str): The type of entity, e.g., "File" or "Directory".
        name (str): The name to validate.
    
    Raises:
        InvalidNameError: If the name is invalid, with a message indicating the entity type.
    """ 
    if not name or name == "":
        raise InvalidNameError(name, f"{entity_type} name cannot be empty.")

    if name in {".", ".."}:
        raise InvalidNameError(name, f"Reserved names '.' and '..' are not allowed for {entity_type.lower()}s.")

    if len(name) > MAX_LENGTH_NAME:
        raise InvalidNameError(name, f"{entity_type} name exceeds the maximum length of {MAX_LENGTH_NAME} characters.")

    if name.strip() != name:
        raise InvalidNameError(name, f"{entity_type} name cannot have leading or trailing spaces.")

    if name.startswith("-"):
        raise InvalidNameError(name, f"{entity_type} name cannot start with a hyphen ('-').")

    if re.search(r'[/:*?"<>|]', name):
        raise InvalidNameError(name, f"{entity_type} name contains invalid characters: / : * ? \" < > |")

    if any(ord(c) < 32 for c in name):
        raise InvalidNameError(name, f"{entity_type} name contains control characters.")

    return None
