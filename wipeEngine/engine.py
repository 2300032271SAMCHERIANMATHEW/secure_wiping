# wipeEngine/engine.py
import os
from wipeEngine.strategies import AVAILABLE_STRATEGIES
from wipeEngine.utils import classify_file
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from wipeEngine import strategies

class WipeEngine:
    def __init__(self, strategy_key, passes=3, chunk_size=1024*1024):
        if strategy_key not in AVAILABLE_STRATEGIES:
            raise ValueError("Invalid strategy key")
        self.strategy_key = strategy_key
        self.strategy_name, self.strategy_func = AVAILABLE_STRATEGIES[strategy_key]
        self.passes = passes
        self.chunk_size = chunk_size

    # ------------------- Scan folder -------------------
    def scan_folder(self, folder_path):
        """Scan folder and return list of files with metadata"""
        files_list = []
        if os.path.isfile(folder_path):
            files_list.append(folder_path)
        else:
            for root, dirs, files in os.walk(folder_path):
                for f in files:
                    files_list.append(os.path.join(root, f))
        report = []
        for fpath in files_list:
            size = os.path.getsize(fpath)
            category = classify_file(fpath)
            report.append({"path": fpath, "size": size, "category": category})
        return report

    # ------------------- Wipe folder -------------------
    def wipe_folder(self, folder_path, strategy_func=None, delete=True, hexdump_func=None):
        """Wipe folder or file and generate PDF report at the end"""
        if strategy_func is None:
            strategy_func = self.strategy_func

        # Prepare target files
        if os.path.isfile(folder_path):
            targets = [folder_path]
        else:
            targets = []
            for root, dirs, files in os.walk(folder_path):
                for f in files:
                    targets.append(os.path.join(root, f))

        # Prepare report data
        report_data = []

        for fpath in targets:
            size = os.path.getsize(fpath)
            category = classify_file(fpath)

            # 🔎 BEFORE WIPE HEXDUMP
            if hexdump_func:
                hexdump_func(fpath, f"--- BEFORE WIPE ({fpath}) ---")

            try:
                strategy_func(fpath, delete=delete)
                deleted = delete
            except Exception as e:
                print(f"❌ Failed to wipe {fpath}: {e}")
                deleted = False

            # 🔎 AFTER WIPE HEXDUMP (if not deleted)
            if hexdump_func and not deleted:
                hexdump_func(fpath, f"--- AFTER WIPE ({fpath}) ---")
            elif deleted:
                print(f"--- AFTER WIPE ({fpath}) ---")
                print("File has been removed ✅")

            report_data.append({
                "path": fpath,
                "category": category,
                "size": size,
                "deleted": deleted
            })

        # Generate PDF once at the end
        self._generate_pdf(report_data)

        return report_data

    def run_wipe(self,file_path, strategy="1", delete=True, hexdump_func=None):
        """
        Wipe a file using selected strategy.
        Optionally call hexdump_func before and after.
        """
        if hexdump_func:
            hexdump_func(file_path, "Before wipe")

        # Pick strategy
        if strategy not in strategies.AVAILABLE_STRATEGIES:
            raise ValueError(f"Invalid strategy {strategy}")

        name, func = strategies.AVAILABLE_STRATEGIES[strategy]
        print(f"\n>> Running wipe: {name}")
        func(file_path, delete=delete)

        if hexdump_func and delete is False:
            hexdump_func(file_path, "After wipe")
        elif not delete:
            print("File kept after wipe.")
        else:
            print("File has been removed after wipe ✅")
    # ------------------- PDF Generation -------------------
    def _generate_pdf(self, file_reports, output_file="wipe_report.pdf"):
        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate(output_file, pagesize=A4)
        elements = []

        elements.append(Paragraph("🔒 Secure Wipe Report", styles['Title']))
        elements.append(Spacer(1, 12))

        # Table header
        data = [["Path", "Category", "Size (bytes)", "Deleted"]]
        for r in file_reports:
            data.append([
                r["path"], r["category"], str(r["size"]), "Yes" if r["deleted"] else "No"
            ])

        table = Table(data, colWidths=[250, 100, 80, 50])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.gray),
            ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('ALIGN',(2,1),(-1,-1),'RIGHT'),
        ]))

        elements.append(table)
        doc.build(elements)
