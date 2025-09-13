import os

def zero_fill(file_path, passes=1, delete=True, chunk_size=1024*1024):
    """Overwrite file with zeros safely in chunks"""
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    try:
        size = os.path.getsize(file_path)
        for i in range(passes):
            with open(file_path, "r+b") as f:
                f.seek(0)
                written = 0
                while written < size:
                    write_size = min(chunk_size, size - written)
                    f.write(b"\x00" * write_size)
                    written += write_size
            print(f"✅ Zero fill pass {i+1}/{passes} completed for {file_path}")
        if delete:
            os.remove(file_path)
            print(f"🗑️ File deleted: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Failed zero fill {file_path}: {e}")
        return False

def random_fill(file_path, passes=3, delete=True, chunk_size=1024*1024):
    """Overwrite file with random bytes safely in chunks"""
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    try:
        size = os.path.getsize(file_path)
        for i in range(passes):
            with open(file_path, "r+b") as f:
                f.seek(0)
                written = 0
                while written < size:
                    write_size = min(chunk_size, size - written)
                    f.write(os.urandom(write_size))
                    written += write_size
            print(f"✅ Random fill pass {i+1}/{passes} completed for {file_path}")
        if delete:
            os.remove(file_path)
            print(f"🗑️ File deleted: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Failed random fill {file_path}: {e}")
        return False

def doD_wipe(file_path, delete=True):
    """3-pass DoD style overwrite"""
    return random_fill(file_path, passes=3, delete=delete)

AVAILABLE_STRATEGIES = {
    "1": ("Zero Fill", zero_fill),
    "2": ("Random Fill", random_fill),
    "3": ("DoD Wipe (3-pass)", doD_wipe)
}
