#!/usr/bin/env python3
import os
import platform
import sys
from configManager.configManager import ConfigManager
from fileManager.utils import hexdump
from wipeEngine.engine import WipeEngine
from wipeEngine.strategies import AVAILABLE_STRATEGIES
from wipeEngine.reportGenerator import PDFReport

# ------------------- Helpers -------------------
def normalize_path(user_path: str) -> str:
    system = platform.system()
    user_path = os.path.expanduser(user_path.strip())
    if system == "Windows":
        if user_path.startswith("/mnt/"):
            drive_letter = user_path.split("/")[2].upper() + ":"
            converted = drive_letter + "\\" + "\\".join(user_path.split("/")[3:])
            return os.path.normpath(converted)
        else:
            return os.path.normpath(user_path)
    else:
        if ":" in user_path and "\\" in user_path:
            drive_letter = user_path[0].lower()
            converted = "/mnt/" + drive_letter + "/" + "/".join(user_path[3:].split("\\"))
            return os.path.normpath(converted)
        else:
            return os.path.normpath(user_path)

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def banner():
    print("=" * 50)
    print(" 🔒 Secure Data Wiper - Module 1 (CLI Interface) 🔒")
    print("=" * 50)

def ask_path():
    while True:
        user_input = input("\n👉 Enter the file/folder path you want to clean: ").strip()
        normalized = normalize_path(user_input)
        if os.path.exists(normalized):
            print(f"✅ Path found: {normalized}")
            return normalized
        else:
            print(f"❌ Invalid path! Tried: {normalized}\nPlease try again.")

def main():
    clear_screen()
    banner()
    target_path = ask_path()
    print("\n📌 System Details:")
    print(f"   OS         : {platform.system()} {platform.release()}")
    print(f"   Python Ver : {platform.python_version()}")
    print(f"   Selected path for cleaning: {target_path}")
    return target_path

# ------------------- Main Execution -------------------
if __name__ == "__main__":
    try:
        # 1️⃣ Get target path
        target_path = main()

        # 2️⃣ Load Config
        cfg = ConfigManager()
        print("\n📂 Current Configuration:")
        print(cfg.config)

        # 3️⃣ Select wipe strategy
        print("\n🔧 Select a wipe strategy:")
        for key, (name, _) in AVAILABLE_STRATEGIES.items():
            print(f"  {key}. {name}")

        while True:
            choice = input("Enter your choice [1-3]: ").strip()
            if choice in AVAILABLE_STRATEGIES:
                strategy_name, strategy_func = AVAILABLE_STRATEGIES[choice]
                print(f"✅ Selected: {strategy_name}")
                break
            else:
                print("❌ Invalid choice. Try again.")

        # 4️⃣ Ask for number of passes if not DoD
        if strategy_name != "DoD Wipe (3-pass)":
            while True:
                try:
                    passes = int(input("🔢 Enter number of passes (default 3): ").strip() or 3)
                    if passes < 1:
                        print("❌ Must be >= 1")
                        continue
                    cfg.update_option("passes", passes)
                    break
                except ValueError:
                    print("❌ Invalid number, try again")
        else:
            passes = 3  # DoD is fixed
            cfg.update_option("passes", passes)

        chunk_size = cfg.get_option("chunk_size") or 1024*1024

        print("\n📂 Updated Configuration:")
        print(cfg.config)
        print("\nOverwrite method:", strategy_name)
        print(f"Passes: {passes}, Chunk size: {chunk_size} bytes")

        # 5️⃣ Initialize WipeEngine with passes and chunk_size
        engine = WipeEngine(choice, passes=passes, chunk_size=chunk_size)

        # 6️⃣ Scan folder and show files
        report = engine.scan_folder(target_path)
        print("\n📊 Files detected for wiping:")
        for f in report:
            print(f"[{f['category']}] {f['path']} - {f['size']} bytes")

        # 7️⃣ Confirm wipe
        confirm = input("\nDo you want to proceed with wiping? (y/n): ").lower()
        pdf_report = PDFReport(output_file="wipe_report.pdf")

        if confirm == "y":
            final_report = engine.wipe_folder(
                target_path,
                strategy_func=strategy_func,
                delete=False,  # keep file for after-wipe check
                hexdump_func=hexdump
            )

            # Log each file to PDFReport
            for f in final_report:
                status = "Success" if f["deleted"] else "Wiped (Kept)"
                pdf_report.log_file(
                    file_path=f['path'],
                    size=f['size'],
                    status=status,
                    strategy=strategy_name
                )
                print(f"[{status}] {f['category']} | {f['path']} | {f['size']} bytes")

            pdf_report.finalize(strategy=strategy_name, target_path=target_path)
            print("\n✅ Wiping completed successfully!")
            print("📄 PDF report generated: wipe_report.pdf")

        else:
            print("\n⚠️ Wipe canceled by user.")

    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user. Exiting safely...")
        sys.exit(0)
