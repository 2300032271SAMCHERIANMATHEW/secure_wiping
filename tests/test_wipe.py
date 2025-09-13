import os
import subprocess
import binascii
from wipeEngine import strategies

TEST_FILE = "tests/secret.txt"

def hexdump(file_path, label, length=64):
    """Cross-platform hex dump (tries xxd, else pure Python)."""
    print(f"\n--- {label} ---")
    try:
        # Try system xxd (Linux/Mac, maybe on Windows with Git Bash)
        output = subprocess.check_output(["xxd", file_path]).decode()
        print(output)
    except (FileNotFoundError, subprocess.CalledProcessError):
        # Fallback: Pure Python hexdump
        with open(file_path, "rb") as f:
            data = f.read(length)  # only read first chunk (avoid huge spam)
            hex_data = binascii.hexlify(data).decode()
            print(" ".join([hex_data[i:i+2] for i in range(0, len(hex_data), 2)]))
            if len(data) == length:
                print("... (truncated)")

def create_test_file():
    """Create a sample test file with sensitive content."""
    os.makedirs(os.path.dirname(TEST_FILE), exist_ok=True)
    with open(TEST_FILE, "w") as f:
        f.write("THIS IS A SECRET MESSAGE. DO NOT LEAK.\n")

if __name__ == "__main__":
    # 1. Create file
    create_test_file()
    hexdump(TEST_FILE, "Before wipe")

    # 2. Apply wipe strategy (try zero_fill, random_fill, doD_wipe)
    strategies.zero_fill(TEST_FILE)

    # 3. Verify removal
    if os.path.exists(TEST_FILE):
        hexdump(TEST_FILE, "After wipe")
    else:
        print("\nFile has been removed after wipe ✅")
