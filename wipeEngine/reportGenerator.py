import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import os
import tempfile

class PDFReport:
    def __init__(self, output_file="wipe_report.pdf"):
        self.output_file = output_file
        self.logs = []
        self.total_size = 0
        self.success_count = 0
        self.failure_count = 0

    def log_file(self, file_path, size, status, strategy):
        """Log each file deletion"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append({
            "time": timestamp,
            "path": file_path,
            "size": size,
            "status": status,
            "strategy": strategy
        })
        self.total_size += size if status == "Success" else 0
        if status == "Success":
            self.success_count += 1
        else:
            self.failure_count += 1

    def generate_charts(self):
        """Generate a pie chart for success vs failure and save to a temp file"""
        plt.figure(figsize=(4,4))
        plt.pie(
            [self.success_count, self.failure_count],
            labels=["Success", "Failure"],
            autopct="%1.1f%%",
            colors=["green", "red"]
        )
        temp_file = os.path.join(tempfile.gettempdir(), "chart_temp.png")
        plt.savefig(temp_file, bbox_inches='tight')
        plt.close()
        return temp_file

    def finalize(self, strategy, target_path):
        """Build PDF report"""
        pdf = SimpleDocTemplate(self.output_file, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Title
        elements.append(Paragraph(f"Secure Wiping Report", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Paragraph(f"Path wiped: {target_path}", styles['Normal']))
        elements.append(Paragraph(f"Wipe strategy: {strategy}", styles['Normal']))
        elements.append(Spacer(1, 12))

        # Summary
        elements.append(Paragraph(f"Total files wiped: {self.success_count + self.failure_count}", styles['Normal']))
        elements.append(Paragraph(f"Files successfully wiped: {self.success_count}", styles['Normal']))
        elements.append(Paragraph(f"Files failed to wipe: {self.failure_count}", styles['Normal']))
        elements.append(Paragraph(f"Total size freed: {self.total_size} bytes", styles['Normal']))
        elements.append(Spacer(1, 12))

        # Charts
        chart_file = self.generate_charts()
        if os.path.exists(chart_file):
            elements.append(Paragraph("Success vs Failure:", styles['Heading3']))
            elements.append(Image(chart_file, width=200, height=200))
            elements.append(Spacer(1, 12))
            # Do NOT delete yet; ReportLab reads it during build
            # os.remove(chart_file)

        # Table of logs
        data = [["Time", "File Path", "Size (bytes)", "Status", "Strategy"]]
        for log in self.logs:
            data.append([log["time"], log["path"], str(log["size"]), log["status"], log["strategy"]])

        table = Table(data, colWidths=[100, 250, 80, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
            ('TEXTCOLOR',(0,0),(-1,0),colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN',(0,0),(-1,-1),'TOP')
        ]))
        elements.append(table)

        # Build PDF
        pdf.build(elements)

        # Now safe to delete chart
        if os.path.exists(chart_file):
            os.remove(chart_file)
