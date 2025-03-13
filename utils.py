import pandas as pd
import os
from reportlab.pdfgen import canvas

# Ensure reports directory exists
os.makedirs("reports", exist_ok=True)

def export_results(format_type):
    """Exports test results in CSV, HTML, or PDF format."""
    results_file = "reports/test_results.csv"  # Assume Locust saves results as CSV

    if not os.path.exists(results_file) or os.path.getsize(results_file) == 0:
        return None  # No results available

    df = pd.read_csv(results_file)  # Load results

    # Export based on format type
    if format_type == "CSV":
        return results_file  # Already in CSV format

    elif format_type == "HTML":
        html_path = "reports/results.html"
        df.to_html(html_path, index=False)
        return html_path

    elif format_type == "PDF":
        pdf_path = "reports/results.pdf"
        c = canvas.Canvas(pdf_path)
        c.drawString(100, 750, "OverloadX-2.0 Test Results")

        y = 730
        for i, row in df.iterrows():
            text = f"{row['name']} - {row['num_requests']} Requests - {row['avg_response_time']} ms"
            c.drawString(100, y, text)
            y -= 20
            if y < 100:  # New page if needed
                c.showPage()
                y = 750

        c.save()
        return pdf_path

    return None
