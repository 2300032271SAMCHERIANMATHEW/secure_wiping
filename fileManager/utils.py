# utils.py
import subprocess, binascii

def pretty_print_metadata(meta):
    """
    Print metadata in a nice readable format.
    """
    print("\n📄 File Metadata:")
    for key, value in meta.items():
        print(f"  {key}: {value}")
    print("-" * 40)
def hexdump(file_path, label, length=64):
    print(f"\n--- {label} ---")
    try:
        output = subprocess.check_output(["xxd", file_path]).decode()
        print(output)
    except Exception:
        with open(file_path, "rb") as f:
            data = f.read(length)
            hex_data = binascii.hexlify(data).decode()
            print(" ".join(hex_data[i:i+2] for i in range(0, len(hex_data), 2)))
            if len(data) == length:
                print("... (truncated)")