import os
import markdown
from fpdf import FPDF

class PdfExporter:
    @staticmethod
    def export(md_path: str, output_dir: str, report_id: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        pdf_path = os.path.join(output_dir, f"report_{report_id}.pdf")
        
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
                
            # Replace common unicode characters that standard Helvetica doesn't support
            md_content = md_content.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'").replace('—', '-')
            
            # Convert markdown to HTML
            html_content = markdown.markdown(md_content, extensions=['tables'])
            
            # Simple wrapper to make HTML text readable in FPDF
            styled_html = f"""
            <font face="Helvetica" size="11">
            {html_content}
            </font>
            """
            
            # Use fpdf2 to write html
            pdf = FPDF()
            pdf.add_page()
            
            # fpdf2 allows HTML directly
            pdf.write_html(styled_html)
            
            pdf.output(pdf_path)
            return pdf_path
            
        except Exception as e:
            print(f"FPDF Export Failed: {e}")
            # Absolute basic fallback
            return PdfExporter._fallback_text_pdf(md_content, pdf_path)

    @staticmethod
    def _fallback_text_pdf(md_content: str, pdf_path: str) -> str:
        # If even HTML fails, just write lines
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=10)
        
        for line in md_content.splitlines():
            # encode to latin-1 and replace unknown chars with dash so fpdf doesn't crash on standard fonts
            clean_line = line.encode("latin-1", "replace").decode("latin-1").replace("?", "-")
            pdf.multi_cell(0, 5, clean_line)
            
        pdf.output(pdf_path)
        return pdf_path
