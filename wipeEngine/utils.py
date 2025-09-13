# wipeEngine/utils.py
import os

def classify_file(file_path):
    """Classify file by type for forensic report"""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    if ext in [".txt", ".md", ".log"]:
        return "Text"
    elif ext in [".jpg", ".png", ".bmp", ".gif"]:
        return "Image"
    elif ext in [".mp4", ".avi", ".mov"]:
        return "Video"
    elif ext in [".zip", ".rar", ".7z"]:
        return "Archive"
    else:
        return "Other"
