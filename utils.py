import json
import pandas as pd
import os
from reportlab.pdfgen import canvas

def export_results(results, format_type):
    if not results:
        print("No data to export.")
        return

    os.makedirs("reports", exist_ok=True)

    if format_type == "CSV":
        df = pd.DataFrame(results)
        df.to_csv("reports/results.csv", index=False)
    
    elif format_type == "JSON":
        with open("reports/results.json", "w") as f:
            json.dump(results, f)
    
    elif format_type == "PDF":
        c = canvas.Canvas("reports/results.pdf")
        c.drawString(100, 750, "OverloadX-2.0 Test Results")
        y = 730
        for i, result in enumerate(results):
            text = f"Test {i+1}: {result['name']} - {result.get('avg_response_time', 'N/A')} ms"
            c.drawString(100, y, text)
            y -= 20
        c.save()
