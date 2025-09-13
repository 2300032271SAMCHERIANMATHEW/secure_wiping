# validator.py
import os

def validate_path(path):
    """
    Validate if a file/folder exists and has R/W permissions.
    Returns a dictionary with result and reason.
    """
    if not os.path.exists(path):
        return {"valid": False, "reason": "Path does not exist"}

    if not os.access(path, os.R_OK):
        return {"valid": False, "reason": "No read permission"}

    if os.path.isfile(path) and not os.access(path, os.W_OK):
        return {"valid": False, "reason": "No write permission"}

    return {"valid": True, "reason": "OK"}
