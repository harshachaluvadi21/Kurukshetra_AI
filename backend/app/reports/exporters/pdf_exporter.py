import os
import re
import textwrap
import markdown

class PdfExporter:
    @staticmethod
    def export(md_path: str, output_dir: str, report_id: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        pdf_path = os.path.join(output_dir, f"report_{report_id}.pdf")
        
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
            
        html_content = markdown.markdown(md_content, extensions=['tables'])
        
        styled_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 5px; }}
                h2 {{ color: #34495e; margin-top: 20px; }}
                strong {{ color: #000; }}
                ul {{ margin-bottom: 15px; }}
                li {{ margin-bottom: 5px; }}
                hr {{ border: 0; border-top: 1px solid #ccc; margin: 20px 0; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # NOTE: Weasyprint requires GTK3 on Windows. If it fails, generate a simple PDF fallback.
        try:
            from weasyprint import HTML
            HTML(string=styled_html).write_pdf(pdf_path)
            return pdf_path
        except Exception:
            PdfExporter._write_fallback_pdf(pdf_path, md_content)
            return pdf_path

    @staticmethod
    def _escape_pdf_text(text: str) -> str:
        return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    @staticmethod
    def _markdown_to_lines(md_content: str) -> list[str]:
        lines: list[str] = []
        for raw_line in md_content.splitlines():
            line = raw_line.strip()
            if not line:
                lines.append("")
                continue
            if line.startswith("#"):
                lines.append(re.sub(r"^#{1,6}\s*", "", line).upper())
                continue
            text = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
            if text.startswith("- "):
                text = f"• {text[2:].strip()}"
            wrapped = textwrap.wrap(text, width=92) or [""]
            lines.extend(wrapped)
        return lines

    @staticmethod
    def _write_fallback_pdf(pdf_path: str, md_content: str) -> None:
        lines = PdfExporter._markdown_to_lines(md_content)
        pages = [lines[i:i + 44] for i in range(0, len(lines), 44)] or [[]]

        def stream_for(page_lines: list[str]) -> bytes:
            body = ["BT", "/F1 12 Tf", "14 TL", "72 760 Td"]
            for index, line in enumerate(page_lines):
                escaped = PdfExporter._escape_pdf_text(line)
                if index == 0:
                    body.append(f"({escaped}) Tj")
                else:
                    body.append("T*")
                    body.append(f"({escaped}) Tj")
            body.append("ET")
            payload = "\n".join(body).encode("latin-1", "replace")
            return b"<< /Length " + str(len(payload)).encode("ascii") + b" >>\nstream\n" + payload + b"\nendstream"

        objects: list[tuple[int, bytes]] = []
        objects.append((1, b"<< /Type /Catalog /Pages 2 0 R >>"))
        kids = " ".join(f"{5 + (i * 2)} 0 R" for i in range(len(pages)))
        objects.append((2, f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode("ascii")))
        objects.append((3, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"))
        for index, page_lines in enumerate(pages):
            contents_number = 4 + (index * 2)
            page_number = 5 + (index * 2)
            objects.append((contents_number, stream_for(page_lines)))
            page_dict = (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                f"/Resources << /Font << /F1 3 0 R >> >> /Contents {contents_number} 0 R >>"
            ).encode("ascii")
            objects.append((page_number, page_dict))

        pdf_bytes = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for number, body in objects:
            offsets.append(len(pdf_bytes))
            pdf_bytes.extend(f"{number} 0 obj\n".encode("ascii"))
            pdf_bytes.extend(body)
            pdf_bytes.extend(b"\nendobj\n")

        xref_offset = len(pdf_bytes)
        total_objects = len(objects) + 1
        pdf_bytes.extend(f"xref\n0 {total_objects}\n".encode("ascii"))
        pdf_bytes.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            pdf_bytes.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
        pdf_bytes.extend(f"trailer\n<< /Size {total_objects} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF".encode("ascii"))

        with open(pdf_path, "wb") as handle:
            handle.write(pdf_bytes)

