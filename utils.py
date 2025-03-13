import json
import pandas as pd
import os
from reportlab.pdfgen import canvas

def export_results(results, format_type):
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
            c.drawString(100, y, f"Test {i+1}: {result}")
            y -= 20
        c.save()
