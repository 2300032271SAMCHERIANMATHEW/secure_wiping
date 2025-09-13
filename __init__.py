# index.py
from fileSelector import select_files_in_folder, select_single_file
from validator import validate_path
from metadata import get_metadata
from utils import pretty_print_metadata

def run_demo():
    # Example: Change these to your test paths
    test_folder = "./testdata"
    test_file = "./testdata/sample.txt"

    # Select a folder
    try:
        files = select_files_in_folder(test_folder)
        print(f"✅ Found {len(files)} files in {test_folder}")
    except Exception as e:
        print(f"❌ Error: {e}")
        files = []

    # Add single file manually
    try:
        files += select_single_file(test_file)
    except Exception as e:
        print(f"❌ Error: {e}")

    # Validate + extract metadata
    for f in files:
        result = validate_path(f)
        if result["valid"]:
            meta = get_metadata(f)
            pretty_print_metadata(meta)
        else:
            print(f"⚠️ Skipping {f}: {result['reason']}")

if __name__ == "__main__":
    run_demo()
