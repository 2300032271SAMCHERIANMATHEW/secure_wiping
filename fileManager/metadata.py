# metadata.py
import os
import mimetypes
import time

def get_metadata(path):
    """
    Extract metadata for a file or folder.
    """
    if not os.path.exists(path):
        return {"path": path, "exists": False}

    stat = os.stat(path)
    info = {
        "path": path,
        "exists": True,
        "is_file": os.path.isfile(path),
        "is_dir": os.path.isdir(path),
        "size": os.path.getsize(path) if os.path.isfile(path) else None,
        "permissions": oct(stat.st_mode)[-3:],  # e.g. '644'
        "last_modified": time.ctime(stat.st_mtime),
        "type": mimetypes.guess_type(path)[0] if os.path.isfile(path) else "directory"
    }
    return info
