import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pypdfium2 as pdfium
from app.reports.exporters.pdf_exporter import PdfExporter

def test_reports():
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs", "reports"))
    test_run_ids = [
        "00cf9eba-51c9-403a-bfc5-404c4d6f2834",
        "3f36c8a7-0142-4094-9099-e3ae592bccce",
        "362f61a1-16a3-4fb6-97e0-aec94428e7a0",
    ]

    for rid in test_run_ids:
        jpath = os.path.join(reports_dir, f"report_{rid}.json")
        if not os.path.exists(jpath):
            print(f"Skipping {rid}, file not found")
            continue

        with open(jpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        idea_name = data.get("idea_name", "Unknown")
        print(f"\n=======================================================")
        print(f"Testing PDF Export for: '{idea_name}' (Run ID: {rid})")
        print(f"=======================================================")

        pdf_path = PdfExporter.export(data, reports_dir, f"test_{rid}")
        print(f"Generated PDF: {pdf_path}")
        print(f"File Size: {os.path.getsize(pdf_path)} bytes")

        # Open and inspect pages with pypdfium2
        doc = pdfium.PdfDocument(pdf_path)
        total_pages = len(doc)
        print(f"Total Pages Generated: {total_pages}")

        # Render Page 1 (Cover) and Page 2 (Dashboard)
        img_p1 = doc[0].render(scale=2).to_pil()
        p1_path = f"test_out_{rid[:8]}_p1.png"
        img_p1.save(p1_path)
        print(f"Saved Cover Image: {p1_path}")

        img_p2 = doc[1].render(scale=2).to_pil()
        p2_path = f"test_out_{rid[:8]}_p2.png"
        img_p2.save(p2_path)
        print(f"Saved Dashboard Image: {p2_path}")

        # Render one interior page (e.g. Page 3 or 4)
        if total_pages > 2:
            img_p3 = doc[2].render(scale=2).to_pil()
            p3_path = f"test_out_{rid[:8]}_p3.png"
            img_p3.save(p3_path)
            print(f"Saved Interior Image: {p3_path}")

if __name__ == "__main__":
    test_reports()
