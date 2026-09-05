"""
Kurukshetra.ai — Complete PDF Report Redesign & Export Engine
Generates McKinsey / BCG / Apple-grade executive intelligence reports.
Fully dynamic for any startup idea, 100% data preservation, strict A4 grid.
"""

import os
import re
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from app.reports.models import ExecutiveReport, ReportSection

# ---------------------------------------------------------------------------
# Font Registration (TrueType System Fonts with Helvetica fallback)
# ---------------------------------------------------------------------------
FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"
FONT_BOLD_ITALIC = "Helvetica-BoldOblique"

try:
    if os.path.exists("C:/Windows/Fonts/segoeui.ttf"):
        pdfmetrics.registerFont(TTFont("SegoeUI", "C:/Windows/Fonts/segoeui.ttf"))
        pdfmetrics.registerFont(TTFont("SegoeUI-Bold", "C:/Windows/Fonts/segoeuib.ttf"))
        pdfmetrics.registerFont(TTFont("SegoeUI-Italic", "C:/Windows/Fonts/segoeuii.ttf"))
        FONT_REGULAR = "SegoeUI"
        FONT_BOLD = "SegoeUI-Bold"
        FONT_ITALIC = "SegoeUI-Italic"
        FONT_BOLD_ITALIC = "SegoeUI-Bold"
    elif os.path.exists("C:/Windows/Fonts/arial.ttf"):
        pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
        pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))
        pdfmetrics.registerFont(TTFont("Arial-Italic", "C:/Windows/Fonts/ariali.ttf"))
        FONT_REGULAR = "Arial"
        FONT_BOLD = "Arial-Bold"
        FONT_ITALIC = "Arial-Italic"
        FONT_BOLD_ITALIC = "Arial-Bold"
except Exception:
    pass

# ---------------------------------------------------------------------------
# Color Palette & Brand Tokens
# ---------------------------------------------------------------------------
NAVY = colors.HexColor("#101828")
TEXT_DARK = colors.HexColor("#1D2939")
TEXT_MUTED = colors.HexColor("#667085")
TEXT_LIGHT = colors.HexColor("#98A2B3")
PURPLE = colors.HexColor("#5B5CEB")
PURPLE_LIGHT = colors.HexColor("#F4F3FF")
PURPLE_BORDER = colors.HexColor("#D9D6FE")
GOLD = colors.HexColor("#C99A3D")
BG_GRAY = colors.HexColor("#F8F9FC")
BG_CARD = colors.HexColor("#FFFFFF")
BORDER_LIGHT = colors.HexColor("#EAECF0")
BORDER_SUBTLE = colors.HexColor("#F2F4F7")

# Verdict Styling (Strict Consulting Matrix)
VERDICT_COLORS = {
    "high risk": {"bg": colors.HexColor("#FFF1F2"), "text": colors.HexColor("#BE123C"), "border": colors.HexColor("#FECDD3")},
    "critical": {"bg": colors.HexColor("#FFF1F2"), "text": colors.HexColor("#BE123C"), "border": colors.HexColor("#FECDD3")},
    "medium risk": {"bg": colors.HexColor("#FFFBEB"), "text": colors.HexColor("#B45309"), "border": colors.HexColor("#FDE68A")},
    "moderate risk": {"bg": colors.HexColor("#FFFBEB"), "text": colors.HexColor("#B45309"), "border": colors.HexColor("#FDE68A")},
    "pivot required": {"bg": colors.HexColor("#FFFBEB"), "text": colors.HexColor("#B45309"), "border": colors.HexColor("#FDE68A")},
    "proceed with caution": {"bg": colors.HexColor("#FFFBEB"), "text": colors.HexColor("#B45309"), "border": colors.HexColor("#FDE68A")},
    "strong": {"bg": colors.HexColor("#F0FDF4"), "text": colors.HexColor("#15803D"), "border": colors.HexColor("#BBF7D0")},
    "ready to scale": {"bg": colors.HexColor("#F0FDF4"), "text": colors.HexColor("#15803D"), "border": colors.HexColor("#BBF7D0")},
    "low risk": {"bg": colors.HexColor("#F0FDF4"), "text": colors.HexColor("#15803D"), "border": colors.HexColor("#BBF7D0")},
}

# Standard Strategic Subtitles for all 21 Sections
SECTION_SUBTITLES = {
    "01": "Strategic intelligence synthesis and core venture evaluation.",
    "02": "Venture architecture, business model classification, and strategic thesis.",
    "03": "Target customer personas, acute pain points, and ecosystem context.",
    "04": "Market size quantification, macro tailwinds, and regional opportunity hubs.",
    "05": "Adoption friction, decision drivers, and buyer persona psychology.",
    "06": "Differentiation wedge, core positioning, and defensive moats.",
    "07": "Competitive landscape mapping, incumbents, and relative positioning.",
    "08": "Unaddressed market opportunities and strategic wedge validation.",
    "09": "Monetization mechanics, revenue streams, and value chain alignment.",
    "10": "Unit pricing structure, purchasing power calibration, and tiering.",
    "11": "Modeled unit economics, CAC/LTV benchmarks, and break-even runway.",
    "12": "Core MVP scope, feature prioritization, and pilot deliverables.",
    "13": "De-risking hypotheses, pilot test design, and pass/fail thresholds.",
    "14": "Phased launch playbook, distribution channels, and cohort acquisition.",
    "15": "North Star metric, pilot KPIs, and validation telemetry targets.",
    "16": "Critical vulnerability matrix and defensive mitigation playbooks.",
    "17": "Skeptic stress-test, unproven assumptions, and counter-arguments.",
    "18": "High-impact default modes, vulnerability triggers, and warning indicators.",
    "19": "Quarterly phased milestones, de-risking gates, and execution roadmap.",
    "20": "Venture studio verdict, strategic directives, and critical success factors.",
    "21": "Verified intelligence sources, citations, and data references.",
}

# ---------------------------------------------------------------------------
# NumberedCanvas: Two-pass page numbering & running headers/footers
# ---------------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages: int):
        page = self._pageNumber
        startup_name = getattr(self, "analyzed_startup", "").strip()

        # PAGE 1: COVER PAGE
        if page == 1:
            self.saveState()
            assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
            plate_path = os.path.join(assets_dir, "cover_bottom_plate.png")
            
            if os.path.exists(plate_path):
                # Smooth bottom mountain topography and dynamic metadata stats
                self.drawImage(plate_path, 0, 0, width=595.28, height=348, mask="auto")

            self.setFont(FONT_REGULAR, 7.5)
            self.setFillColor(TEXT_MUTED)
            self.drawRightString(550, 25, f"Page 1 of {total_pages}")
            self.restoreState()
            return

        # PAGE 2+: INTERIOR PAGES
        self.saveState()

        # Kurukshetra.ai Official Watermark (Subtle 5.5% opacity, tilted 28°)
        assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        wm_path = os.path.join(assets_dir, "kurukshetra_watermark.png")
        if os.path.exists(wm_path):
            self.saveState()
            self.translate(297.64, 420.0)
            self.rotate(28)
            self.drawImage(wm_path, -190, -52, width=380, height=104, mask="auto")
            self.restoreState()

        # Running Header (y = 806)
        self.setFont(FONT_BOLD, 8.5)
        self.setFillColor(PURPLE)
        self.drawString(45, 806, "Kurukshetra.ai")
        
        self.setFont(FONT_REGULAR, 8)
        self.setFillColor(TEXT_LIGHT)
        self.drawString(104, 806, "|")
        self.setFillColor(TEXT_MUTED)
        self.drawString(112, 806, "AI Startup Intelligence")

        # Responsive Startup Header (NEVER awkwardly truncated with ellipsis!)
        if startup_name:
            self.setFillColor(NAVY)
            if len(startup_name) <= 36:
                self.setFont(FONT_BOLD, 8.0)
                self.drawRightString(550, 806, startup_name)
            elif len(startup_name) <= 50:
                # 2-line clean right-aligned display
                words = startup_name.split()
                mid = len(words) // 2
                l1 = " ".join(words[:mid])
                l2 = " ".join(words[mid:])
                self.setFont(FONT_BOLD, 7.0)
                self.drawRightString(550, 811, l1)
                self.drawRightString(550, 802, l2)
            else:
                # Long name: 3-line or smart split
                words = startup_name.split()
                chunk_len = len(words) // 2
                l1 = " ".join(words[:chunk_len])
                l2 = " ".join(words[chunk_len:])
                self.setFont(FONT_BOLD, 6.5)
                self.drawRightString(550, 811, l1)
                self.drawRightString(550, 802, l2)

        # Header Rule (y = 798)
        self.setStrokeColor(BORDER_LIGHT)
        self.setLineWidth(0.65)
        self.line(45, 798, 550, 798)

        # Footer Rule (y = 48)
        self.setStrokeColor(BORDER_LIGHT)
        self.setLineWidth(0.65)
        self.line(45, 48, 550, 48)

        # Running Footer (y = 36)
        self.setFont(FONT_REGULAR, 7.5)
        self.setFillColor(TEXT_LIGHT)
        self.drawString(45, 36, "Kurukshetra.ai — AI STARTUP INTELLIGENCE")

        self.setFont(FONT_REGULAR, 8)
        self.setFillColor(TEXT_MUTED)
        self.drawRightString(550, 36, f"Page {page:02d} of {total_pages:02d}")

        self.restoreState()


# ---------------------------------------------------------------------------
# Exporter Class
# ---------------------------------------------------------------------------
class PdfExporter:
    @staticmethod
    def export(report_or_md: Union[ExecutiveReport, Dict[str, Any], str], output_dir: str, report_id: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        pdf_path = os.path.join(output_dir, f"report_{report_id}.pdf")

        # Resolve Report Data
        report_data = PdfExporter._resolve_report(report_or_md, output_dir, report_id)

        # Build Document
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            leftMargin=45,
            rightMargin=45,
            topMargin=46,
            bottomMargin=48
        )

        styles = PdfExporter._create_styles()
        elements: List[Any] = []

        # 1. PAGE 1: Dynamic Editorial Cover
        PdfExporter._build_cover(elements, report_data, styles)
        elements.append(PageBreak())

        # 2. PAGE 2: Executive Summary Dashboard
        PdfExporter._build_executive_dashboard(elements, report_data, styles)
        elements.append(PageBreak())

        # 3. PAGES 3+: Sections 02 to 21
        PdfExporter._build_sections(elements, report_data, styles)

        # Compile Document with NumberedCanvas
        def make_canvas(*args, **kwargs):
            c = NumberedCanvas(*args, **kwargs)
            c.analyzed_startup = report_data.get("idea_name", "")
            return c

        doc.build(elements, canvasmaker=make_canvas)
        return pdf_path

    # -----------------------------------------------------------------------
    # Data Resolution & Normalization
    # -----------------------------------------------------------------------
    @staticmethod
    def _resolve_report(report_or_md: Any, output_dir: str, report_id: str) -> Dict[str, Any]:
        if isinstance(report_or_md, ExecutiveReport):
            return report_or_md.model_dump()
        elif isinstance(report_or_md, dict):
            return report_or_md

        # Check if companion JSON exists
        json_path = os.path.join(output_dir, f"report_{report_id}.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        # Parse from Markdown file
        if isinstance(report_or_md, str) and os.path.exists(report_or_md):
            with open(report_or_md, "r", encoding="utf-8") as f:
                content = f.read()
            return PdfExporter._parse_markdown_report(content, report_id)

        return {"idea_name": "Startup Idea", "report_id": report_id, "sections": []}

    @staticmethod
    def _parse_markdown_report(content: str, report_id: str) -> Dict[str, Any]:
        idea_name = "Startup Idea"
        m = re.search(r"\*\*Idea:\*\*\s*(.+)", content)
        if m:
            idea_name = m.group(1).strip()
        else:
            m2 = re.search(r"#\s*(.+)", content)
            if m2:
                idea_name = m2.group(1).replace("Executive Summary", "").replace(":", "").strip() or idea_name

        score = 50.0
        sm = re.search(r"\*\*Battle Score:\*\*\s*([0-9.]+)", content)
        if sm:
            try:
                score = float(sm.group(1))
            except ValueError:
                pass

        verdict = "Evaluation Complete"
        vm = re.search(r"\*\*Verdict:\*\*\s*([^\n]+)", content)
        if vm:
            verdict = vm.group(1).strip()

        conf = 0.8
        cm = re.search(r"\*\*Confidence:\*\*\s*([0-9.]+)%?", content)
        if cm:
            try:
                conf = float(cm.group(1)) / (100.0 if float(cm.group(1)) > 1.0 else 1.0)
            except ValueError:
                pass

        # Split into sections by Markdown headings
        raw_sections = re.split(r"\n(?=#{1,2}\s+)", content)
        sections = []
        for s in raw_sections:
            s_clean = s.strip()
            if not s_clean:
                continue
            lines = s_clean.split("\n")
            title = re.sub(r"^#{1,3}\s*", "", lines[0]).strip()
            sections.append({"title": title, "content_markdown": s_clean})

        return {
            "idea_name": idea_name,
            "battle_score": score,
            "confidence_score": conf,
            "verdict": verdict,
            "target_market": "India",
            "currency": "INR",
            "currency_symbol": "₹",
            "sections": sections,
            "report_id": report_id,
            "generated_at": datetime.utcnow().isoformat()
        }

    # -----------------------------------------------------------------------
    # Style System
    # -----------------------------------------------------------------------
    @staticmethod
    def _create_styles() -> Dict[str, ParagraphStyle]:
        styles = getSampleStyleSheet()

        custom = {
            "CoverTitle": ParagraphStyle(
                "CoverTitle",
                fontName=FONT_BOLD,
                fontSize=34,
                leading=38,
                textColor=NAVY
            ),
            "CoverSubtitle": ParagraphStyle(
                "CoverSubtitle",
                fontName=FONT_REGULAR,
                fontSize=10.5,
                leading=15,
                textColor=TEXT_MUTED
            ),
            "CoverQuote": ParagraphStyle(
                "CoverQuote",
                fontName=FONT_ITALIC,
                fontSize=10,
                leading=14,
                alignment=2,
                textColor=colors.HexColor("#475467")
            ),
            "CoverQuoteAuthor": ParagraphStyle(
                "CoverQuoteAuthor",
                fontName=FONT_BOLD,
                fontSize=7,
                leading=9,
                alignment=2,
                textColor=TEXT_MUTED
            ),
            "StartupLabel": ParagraphStyle(
                "StartupLabel",
                fontName=FONT_BOLD,
                fontSize=8,
                leading=10,
                textColor=TEXT_MUTED
            ),
            "StartupName": ParagraphStyle(
                "StartupName",
                fontName=FONT_BOLD,
                fontSize=17,
                leading=21,
                textColor=NAVY
            ),
            "MetaLabel": ParagraphStyle(
                "MetaLabel",
                fontName=FONT_REGULAR,
                fontSize=8,
                leading=10,
                textColor=TEXT_MUTED
            ),
            "MetaVal": ParagraphStyle(
                "MetaVal",
                fontName=FONT_BOLD,
                fontSize=9.5,
                leading=12,
                textColor=NAVY
            ),
            "SectionNum": ParagraphStyle(
                "SectionNum",
                fontName=FONT_BOLD,
                fontSize=11,
                leading=13,
                textColor=PURPLE,
                keepWithNext=True
            ),
            "SectionHeading": ParagraphStyle(
                "SectionHeading",
                fontName=FONT_BOLD,
                fontSize=18,
                leading=22,
                textColor=NAVY,
                keepWithNext=True
            ),
            "SectionSub": ParagraphStyle(
                "SectionSub",
                fontName=FONT_ITALIC,
                fontSize=8.5,
                leading=12,
                textColor=TEXT_MUTED,
                keepWithNext=True
            ),
            "SubHeading": ParagraphStyle(
                "SubHeading",
                fontName=FONT_BOLD,
                fontSize=10.5,
                leading=14,
                textColor=NAVY,
                keepWithNext=True,
                spaceBefore=6,
                spaceAfter=3
            ),
            "Body": ParagraphStyle(
                "Body",
                fontName=FONT_REGULAR,
                fontSize=9.0,
                leading=13,
                textColor=TEXT_DARK,
                spaceAfter=3
            ),
            "BodyBold": ParagraphStyle(
                "BodyBold",
                fontName=FONT_BOLD,
                fontSize=9.0,
                leading=13,
                textColor=NAVY,
                spaceAfter=3
            ),
            "Bullet": ParagraphStyle(
                "Bullet",
                fontName=FONT_REGULAR,
                fontSize=9.0,
                leading=13,
                textColor=TEXT_DARK,
                leftIndent=12,
                firstLineIndent=-12,
                spaceAfter=2.5
            ),
            "Callout": ParagraphStyle(
                "Callout",
                fontName=FONT_REGULAR,
                fontSize=9.0,
                leading=13.5,
                textColor=NAVY
            ),
            "TableHead": ParagraphStyle(
                "TableHead",
                fontName=FONT_BOLD,
                fontSize=8.0,
                leading=10.5,
                textColor=NAVY
            ),
            "TableCell": ParagraphStyle(
                "TableCell",
                fontName=FONT_REGULAR,
                fontSize=8.0,
                leading=11,
                textColor=TEXT_DARK
            ),
            "TableCellBold": ParagraphStyle(
                "TableCellBold",
                fontName=FONT_BOLD,
                fontSize=8.0,
                leading=11,
                textColor=NAVY
            ),
            "TableCellMuted": ParagraphStyle(
                "TableCellMuted",
                fontName=FONT_REGULAR,
                fontSize=7.5,
                leading=10,
                textColor=TEXT_MUTED
            ),
        }
        return custom

    # -----------------------------------------------------------------------
    # PAGE 1: Editorial Cover Page
    # -----------------------------------------------------------------------
    @staticmethod
    def _build_cover(elements: List[Any], data: Dict[str, Any], styles: Dict[str, ParagraphStyle]):
        assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        logo_path = os.path.join(assets_dir, "kurukshetra_logo.png")

        idea_name = data.get("idea_name", "Startup Idea")
        score = float(data.get("battle_score", 0.0))
        verdict = str(data.get("verdict", "Evaluation Complete")).strip()
        conf = float(data.get("confidence_score", 0.0))
        conf_pct = f"{int(round(conf * 100))}%" if conf <= 1.0 else f"{int(round(conf))}%"
        target_market = data.get("target_market", "India")
        
        # Format Date
        date_str = datetime.utcnow().strftime("%B %Y")
        gen_at = data.get("generated_at")
        if gen_at:
            try:
                date_str = datetime.fromisoformat(gen_at.replace("Z", "+00:00")).strftime("%B %Y")
            except Exception:
                pass

        # 1. Top Bar: Logo + Confidential Box
        if os.path.exists(logo_path):
            logo_img = RLImage(logo_path, width=144, height=39)
        else:
            logo_img = Paragraph("<b><font size='16' color='#5B5CEB'>Kurukshetra.ai</font></b>", styles["StartupName"])

        conf_text = Paragraph(
            '<para align="right"><font size="8" color="#475467"><b>CONFIDENTIAL</b></font><br/>'
            '<font size="7" color="#667085">AI STARTUP INTELLIGENCE REPORT</font><br/>'
            '<font size="7" color="#98A2B3">Ideas | Analysis | Clarity</font></para>',
            styles["CoverSubtitle"]
        )
        top_table = Table([[logo_img, conf_text]], colWidths=[280, 225])
        top_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        elements.append(top_table)
        elements.append(Spacer(1, 24))

        # 2. Eyebrow
        eyebrow = Paragraph('<font color="#C99A3D"><b>—</b></font> <font size="7.5" color="#667085"><b>BATTLE-TEST YOUR IDEA</b></font>', styles["CoverSubtitle"])
        elements.append(eyebrow)
        elements.append(Spacer(1, 8))

        # 3. Two-Column Title + Quote Box
        left_flowables = [
            Paragraph("AI Startup<br/>Intelligence Report", styles["CoverTitle"]),
            Spacer(1, 8),
            Paragraph("Deep research. Real debate. Clear direction.", styles["CoverSubtitle"])
        ]
        right_flowables = [
            Paragraph("“Clarity today<br/>builds better<br/>tomorrows.”", styles["CoverQuote"]),
            Spacer(1, 6),
            Paragraph('<font color="#C99A3D">—</font> KURUKSHETRA.AI', styles["CoverQuoteAuthor"])
        ]
        title_table = Table([[left_flowables, right_flowables]], colWidths=[355, 150])
        title_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        elements.append(title_table)
        elements.append(Spacer(1, 22))

        # 4. Analyzed Startup Information (100% Dynamic)
        elements.append(Paragraph("ANALYZED STARTUP IDEA", styles["StartupLabel"]))
        elements.append(Spacer(1, 4))
        
        # Scale font dynamically if idea name is long
        startup_style = styles["StartupName"]
        if len(idea_name) > 40:
            startup_style = ParagraphStyle("SLong", parent=startup_style, fontSize=15, leading=19)
        elements.append(Paragraph(idea_name, startup_style))
        elements.append(Spacer(1, 10))

        # Metadata Row
        meta_table = Table([
            [
                [Paragraph("Target Market", styles["MetaLabel"]), Spacer(1, 2), Paragraph(target_market, styles["MetaVal"])],
                [Paragraph("Report Date", styles["MetaLabel"]), Spacer(1, 2), Paragraph(date_str, styles["MetaVal"])],
            ]
        ], colWidths=[130, 200])
        meta_table.setStyle(TableStyle([
            ("LINEBEFORE", (1, 0), (1, 0), 1, BORDER_LIGHT),
            ("LEFTPADDING", (1, 0), (1, 0), 16),
            ("LEFTPADDING", (0, 0), (0, 0), 0),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 18))

        # 5. Executive Metric Block
        m_score = [
            Paragraph("BATTLE SCORE", ParagraphStyle("MLblP", fontName=FONT_BOLD, fontSize=7.5, leading=9, textColor=PURPLE)),
            Spacer(1, 6),
            Paragraph(f'<font size="24" color="#5B5CEB"><b>{score:.1f}</b></font> <font size="9" color="#667085">/ 100</font>', styles["Body"])
        ]

        # Dynamic Verdict Badge
        v_key = verdict.lower()
        v_style = VERDICT_COLORS.get(v_key, VERDICT_COLORS["medium risk"])
        badge_p = Paragraph(f'<para align="center"><font size="8" color="{v_style["text"].hexval()}"><b>{verdict.upper()}</b></font></para>', styles["Body"])
        verdict_badge = Table([[badge_p]], colWidths=[96])
        verdict_badge.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), v_style["bg"]),
            ("BOX", (0, 0), (-1, -1), 0.5, v_style["border"]),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))

        m_verdict = [
            Paragraph("VERDICT", ParagraphStyle("MLblG", fontName=FONT_BOLD, fontSize=7.5, leading=9, textColor=TEXT_MUTED)),
            Spacer(1, 8),
            verdict_badge
        ]

        m_conf = [
            Paragraph("CONFIDENCE", ParagraphStyle("MLblG2", fontName=FONT_BOLD, fontSize=7.5, leading=9, textColor=TEXT_MUTED)),
            Spacer(1, 6),
            Paragraph(f'<font size="24" color="#101828"><b>{conf_pct}</b></font>', styles["Body"])
        ]

        metric_table = Table([[m_score, m_verdict, m_conf]], colWidths=[170, 165, 170])
        metric_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), BG_GRAY),
            ("BOX", (0, 0), (-1, -1), 1, BORDER_LIGHT),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("LEFTPADDING", (0, 0), (-1, -1), 16),
            ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ]))
        elements.append(metric_table)

    # -----------------------------------------------------------------------
    # PAGE 2: Executive Summary Dashboard
    # -----------------------------------------------------------------------
    @staticmethod
    def _build_executive_dashboard(elements: List[Any], data: Dict[str, Any], styles: Dict[str, ParagraphStyle]):
        score = float(data.get("battle_score", 0.0))
        verdict = str(data.get("verdict", "Evaluation Complete")).strip()
        conf = float(data.get("confidence_score", 0.0))
        conf_pct = f"{int(round(conf * 100))}%" if conf <= 1.0 else f"{int(round(conf))}%"
        target_market = data.get("target_market", "India")
        currency_sym = data.get("currency_symbol", "₹")

        # Section Header
        PdfExporter._add_section_header(elements, "01", "EXECUTIVE SUMMARY", SECTION_SUBTITLES["01"], styles)
        elements.append(Spacer(1, 10))

        # 1. 4-Block Metric Row
        v_key = verdict.lower()
        v_style = VERDICT_COLORS.get(v_key, VERDICT_COLORS["medium risk"])
        b_score = [
            Paragraph("BATTLE SCORE", styles["MetaLabel"]),
            Spacer(1, 3),
            Paragraph(f'<font size="16" color="#5B5CEB"><b>{score:.1f}</b></font> <font size="8" color="#667085">/100</font>', styles["Body"])
        ]
        b_verdict = [
            Paragraph("VERDICT", styles["MetaLabel"]),
            Spacer(1, 3),
            Paragraph(f'<font size="11" color="{v_style["text"].hexval()}"><b>{verdict.upper()}</b></font>', styles["Body"])
        ]
        b_conf = [
            Paragraph("CONFIDENCE", styles["MetaLabel"]),
            Spacer(1, 3),
            Paragraph(f'<font size="16" color="#101828"><b>{conf_pct}</b></font>', styles["Body"])
        ]
        b_market = [
            Paragraph("TARGET MARKET", styles["MetaLabel"]),
            Spacer(1, 3),
            Paragraph(f'<font size="13" color="#101828"><b>{target_market}</b></font> <font size="8" color="#667085">({currency_sym})</font>', styles["Body"])
        ]

        metrics_row = Table([[b_score, b_verdict, b_conf, b_market]], colWidths=[126, 126, 126, 127])
        metrics_row.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), BG_GRAY),
            ("BOX", (0, 0), (-1, -1), 1, BORDER_LIGHT),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ]))
        elements.append(metrics_row)
        elements.append(Spacer(1, 10))

        # 2. Executive Directive / Recommendation Callout
        sec_exec = PdfExporter._find_section(data, ["executive summary", "business concept"])
        exec_content = sec_exec.get("content_markdown", "") if sec_exec else ""
        
        recommendation_text = ""
        m_rec = re.search(r"\*\*Recommendation:\*\*\s*(.+)", exec_content)
        if m_rec:
            recommendation_text = m_rec.group(1).strip()
        else:
            recommendation_text = f"{verdict}: Focus on customer discovery, pilot cohort retention, and margin validation in {target_market}."

        callout_p = [
            Paragraph(f'<font color="#5B5CEB"><b>EXECUTIVE DIRECTIVE:</b></font> &nbsp;{recommendation_text}', styles["Callout"])
        ]
        callout_table = Table([[callout_p]], colWidths=[505])
        callout_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PURPLE_LIGHT),
            ("LINELEFT", (0, 0), (0, 0), 3, PURPLE),
            ("BOX", (0, 0), (-1, -1), 0.5, PURPLE_BORDER),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ]))
        elements.append(callout_table)
        elements.append(Spacer(1, 12))

        # 3. Two-Column Cards: TOP STRENGTHS & KEY RISKS
        strengths = PdfExporter._extract_bullets(data, "Strengths", ["Strengths", "Key Strengths", "Top Strengths"])[:3]
        risks = PdfExporter._extract_risks(data)[:3]

        if not strengths:
            strengths = [
                f"Defensible go-to-market wedge tailored to local operational realities in {target_market}.",
                "Lean operating model capable of early unit economic proof before heavy platform burn."
            ]
        if not risks:
            risks = [
                f"Customer acquisition friction and retention volatility during early launch in {target_market}.",
                "Competitive response from established incumbents or alternative substitutes."
            ]

        str_items = [Paragraph("<b>TOP STRENGTHS</b>", ParagraphStyle("STitle", fontName=FONT_BOLD, fontSize=8.5, leading=11, textColor=colors.HexColor("#15803D"))), Spacer(1, 4)]
        for s in strengths:
            clean_s = re.sub(r"^\*\*[^*]+\*\*:\s*", "", s).strip()
            str_items.append(Paragraph(f'<font color="#15803D"><b>•</b></font> &nbsp;{clean_s}', styles["TableCell"]))
            str_items.append(Spacer(1, 3))

        risk_items = [Paragraph("<b>KEY RISKS</b>", ParagraphStyle("RTitle", fontName=FONT_BOLD, fontSize=8.5, leading=11, textColor=colors.HexColor("#BE123C"))), Spacer(1, 4)]
        for r in risks:
            clean_r = re.sub(r"^\*\*[^*]+\*\*:\s*", "", r).strip()
            risk_items.append(Paragraph(f'<font color="#BE123C"><b>•</b></font> &nbsp;{clean_r}', styles["TableCell"]))
            risk_items.append(Spacer(1, 3))

        cards_table = Table([[str_items, risk_items]], colWidths=[247, 248])
        cards_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#F0FDF4")),
            ("BOX", (0, 0), (0, 0), 1, colors.HexColor("#BBF7D0")),
            ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#FFF1F2")),
            ("BOX", (1, 0), (1, 0), 1, colors.HexColor("#FECDD3")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 11),
            ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ]))
        elements.append(cards_table)
        elements.append(Spacer(1, 12))

        # 4. Strategic Thesis Card
        thesis_match = re.search(r"\*\*Strategic Thesis:\*\*\s*([\s\S]+?)(?=\n\n|\n-|$)", exec_content)
        if not thesis_match:
            sec_concept = PdfExporter._find_section(data, ["business concept"])
            concept_content = sec_concept.get("content_markdown", "") if sec_concept else ""
            thesis_match = re.search(r"\*\*Strategic Thesis:\*\*\s*([\s\S]+?)(?=\n\n|\n-|$)", concept_content)
        
        thesis_text = thesis_match.group(1).strip() if thesis_match else f"{data.get('idea_name', 'Venture')} addresses unserved inefficiencies in {target_market} with a focused wedge tailored to operational realities."

        thesis_flow = [
            Paragraph("<b>STRATEGIC THESIS</b>", styles["SubHeading"]),
            Spacer(1, 2),
            Paragraph(thesis_text, styles["Body"])
        ]
        thesis_table = Table([[thesis_flow]], colWidths=[505])
        thesis_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), BG_GRAY),
            ("BOX", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
            ("LINELEFT", (0, 0), (0, 0), 2.5, PURPLE),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ]))
        elements.append(thesis_table)
        elements.append(Spacer(1, 12))

        # 5. Immediate Priorities & Venture Attributes (Balances Page 2 Gracefully)
        top_actions = []
        action_match = re.search(r"\*\*Top Actions:\*\*\s*\n([\s\S]*?)(?=\n\*\*|\n>|$)", exec_content)
        if action_match:
            for al in action_match.group(1).split("\n"):
                al_s = al.strip()
                if (al_s.startswith("- ") or al_s.startswith("* ")) and len(al_s) > 5:
                    top_actions.append(al_s[2:].strip())

        timing_match = re.search(r"\*\*Market Timing:\*\*\s*(.+)", exec_content)
        timing_val = timing_match.group(1).strip() if timing_match else "Supply chain digitization & localized demand aggregation"

        # Attribute highlight row
        att_c1 = [Paragraph("MARKET TIMING", styles["MetaLabel"]), Spacer(1, 2), Paragraph(f"<b>{timing_val}</b>", styles["TableCellBold"])]
        att_c2 = [Paragraph("BUSINESS MODEL", styles["MetaLabel"]), Spacer(1, 2), Paragraph(f"<b>{data.get('target_market', 'Regional')} Wedge</b>", styles["TableCellBold"])]
        att_c3 = [Paragraph("EXECUTION HORIZON", styles["MetaLabel"]), Spacer(1, 2), Paragraph("<b>90-Day Pilot Cohort</b>", styles["TableCellBold"])]
        
        att_table = Table([[att_c1, att_c2, att_c3]], colWidths=[205, 150, 150])
        att_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), BG_GRAY),
            ("BOX", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]))
        elements.append(att_table)
        elements.append(Spacer(1, 10))

        # 6. Data Classification Legend
        legend_cells = [
            Paragraph('<font size="7.5" color="#15803D"><b>[FACT]</b></font> <font size="7.5" color="#475467">Verified User / Source Data</font>', styles["TableCell"]),
            Paragraph('<font size="7.5" color="#1D4ED8"><b>[ESTIMATE]</b></font> <font size="7.5" color="#475467">Market Intelligence Estimate</font>', styles["TableCell"]),
            Paragraph('<font size="7.5" color="#B45309"><b>[ASSUMPTION]</b></font> <font size="7.5" color="#475467">Modeled Baseline Assumption</font>', styles["TableCell"]),
            Paragraph('<font size="7.5" color="#7C3AED"><b>[TARGET]</b></font> <font size="7.5" color="#475467">Recommended Pilot Milestone</font>', styles["TableCell"]),
        ]
        legend_table = Table([[legend_cells[0], legend_cells[1]], [legend_cells[2], legend_cells[3]]], colWidths=[252, 253])
        legend_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), BG_GRAY),
            ("BOX", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]))
        elements.append(legend_table)

    # -----------------------------------------------------------------------
    # PAGES 3+: 21 Report Sections
    # -----------------------------------------------------------------------
    @staticmethod
    def _build_sections(elements: List[Any], data: Dict[str, Any], styles: Dict[str, ParagraphStyle]):
        sections = data.get("sections", [])
        if not sections:
            legacy_keys = [
                "market_research", "swot_analysis", "competitor_analysis", "pricing_strategy",
                "financial_analysis", "go_to_market_strategy", "critic_analysis", "evidence_citations",
                "final_recommendation"
            ]
            sections = [data[k] for k in legacy_keys if k in data and isinstance(data[k], dict)]

        # Render sections 02 to 21
        for idx, sec in enumerate(sections, start=1):
            if idx == 1:
                continue

            sec_num = f"{idx:02d}"
            title = sec.get("title", f"Section {sec_num}")
            clean_title = re.sub(r"^Section\s+\d+:\s*", "", title, flags=re.I).strip()
            content = sec.get("content_markdown", "")
            subtitle = SECTION_SUBTITLES.get(sec_num, "Autonomous strategic intelligence assessment.")

            # Add Section Header (KeepTogether ensures never orphaned at bottom)
            PdfExporter._add_section_header(elements, sec_num, clean_title.upper(), subtitle, styles)
            elements.append(Spacer(1, 8))

            # Specialized Section Renderers
            if "competitor" in clean_title.lower():
                PdfExporter._render_competitor_section(elements, content, styles)
            elif "financial" in clean_title.lower():
                PdfExporter._render_financial_section(elements, content, styles)
            elif "swot" in clean_title.lower():
                PdfExporter._render_swot_section(elements, content, styles)
            elif "risk" in clean_title.lower() or "mitigation" in clean_title.lower():
                PdfExporter._render_risk_section(elements, content, styles)
            elif "failure scenario" in clean_title.lower():
                PdfExporter._render_failure_scenarios_section(elements, content, styles)
            elif "execution roadmap" in clean_title.lower() or "roadmap" in clean_title.lower():
                PdfExporter._render_execution_roadmap_section(elements, content, styles)
            elif "final recommendation" in clean_title.lower():
                PdfExporter._render_final_recommendation_section(elements, content, styles)
            elif "sources" in clean_title.lower() or "citation" in clean_title.lower():
                PdfExporter._render_citations_section(elements, content, sec.get("citations", []), styles)
            else:
                PdfExporter._render_generic_markdown(elements, content, styles)

            # Compact section spacer so content flows naturally without giant gaps
            elements.append(Spacer(1, 12))

    # -----------------------------------------------------------------------
    # Specialized Section Renderers
    # -----------------------------------------------------------------------
    @staticmethod
    def _render_competitor_section(elements: List[Any], content: str, styles: Dict[str, ParagraphStyle]):
        comp_rows = []
        raw_lines = content.split("\n")
        
        for line in raw_lines:
            line_str = line.strip()
            if not line_str:
                continue
            if line_str.startswith("- ") or line_str.startswith("* "):
                bullet = line_str[2:].strip()
                m = re.search(r"\*\*([^*]+)\*\*\s*(?:\(([^)]+)\))?(?:\s*\[([^\]]+)\])?\s*[-–:]\s*(.+)", bullet)
                if m:
                    name = m.group(1).strip()
                    cat = m.group(2).strip() if m.group(2) else "Competitor"
                    desc = m.group(4).strip()
                    
                    st_m = re.search(r"Strengths:\s*([^.]+)\.?\s*Weaknesses:\s*([^.]+)", desc, re.I)
                    if st_m:
                        strengths = st_m.group(1).strip()
                        weaknesses = st_m.group(2).strip()
                    else:
                        strengths = desc[:90] + "…" if len(desc) > 90 else desc
                        weaknesses = "Established market reach."

                    comp_rows.append([
                        Paragraph(f"<b>{name}</b>", styles["TableCellBold"]),
                        Paragraph(f"<font color='#667085'>{cat}</font>", styles["TableCellMuted"]),
                        Paragraph(strengths, styles["TableCell"]),
                        Paragraph(weaknesses, styles["TableCell"]),
                    ])

        if comp_rows:
            table_data = [[
                Paragraph("<b>COMPETITOR</b>", styles["TableHead"]),
                Paragraph("<b>CATEGORY</b>", styles["TableHead"]),
                Paragraph("<b>STRENGTHS</b>", styles["TableHead"]),
                Paragraph("<b>WEAKNESSES</b>", styles["TableHead"]),
            ]] + comp_rows

            comp_table = Table(table_data, colWidths=[110, 90, 150, 155], repeatRows=1)
            t_styles = [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F4F3FF")),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
            # Subtle alternating rows
            for r_idx in range(1, len(table_data)):
                if r_idx % 2 == 0:
                    t_styles.append(("BACKGROUND", (0, r_idx), (-1, r_idx), BG_GRAY))
            comp_table.setStyle(TableStyle(t_styles))
            elements.append(comp_table)
        else:
            PdfExporter._render_generic_markdown(elements, content, styles)

    @staticmethod
    def _render_financial_section(elements: List[Any], content: str, styles: Dict[str, ParagraphStyle]):
        metrics = []
        for line in content.split("\n"):
            line_str = line.strip()
            m = re.search(r"-\s*(?:\*\*)?([^*:\n]+?)(?:\*\*)?:\s*([^[<\n]+?)(?:\s*\[([^\]]+)\])?$", line_str)
            if m:
                label = m.group(1).strip().strip("*").strip()
                val = m.group(2).strip().strip("*").strip()
                tag = m.group(3).strip() if m.group(3) else "ASSUMPTION"
                
                tag_color = "#B45309" if "assump" in tag.lower() else "#7C3AED" if "target" in tag.lower() else "#15803D" if "fact" in tag.lower() else "#1D4ED8"
                tag_badge = f'<font size="7.5" color="{tag_color}"><b>[{tag.upper()}]</b></font>'

                metrics.append([
                    Paragraph(f"<b>{label}</b>", styles["TableCell"]),
                    Paragraph(f"<b>{val}</b>", styles["TableCellBold"]),
                    Paragraph(tag_badge, styles["TableCellMuted"]),
                ])

        if metrics:
            table_data = [[
                Paragraph("<b>FINANCIAL METRIC</b>", styles["TableHead"]),
                Paragraph("<b>PROJECTED VALUE</b>", styles["TableHead"]),
                Paragraph("<b>CLASSIFICATION</b>", styles["TableHead"]),
            ]] + metrics

            fin_table = Table(table_data, colWidths=[220, 155, 130])
            fin_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F4F3FF")),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]))
            elements.append(fin_table)
            elements.append(Spacer(1, 8))

            disc_match = re.search(r"> \[!IMPORTANT\][\s\S]*?\n>\s*([^\n]+(?:\n>[^\n]+)*)", content)
            if disc_match:
                disc_text = disc_match.group(1).replace(">", "").strip()
                disc_formatted = PdfExporter._markdown_to_xml(disc_text)
                disc_p = Paragraph(f'<font size="8" color="#667085"><i>{disc_formatted}</i></font>', styles["Body"])
                callout_d = Table([[disc_p]], colWidths=[505])
                callout_d.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), BG_GRAY),
                    ("BOX", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                    ("LINELEFT", (0, 0), (0, 0), 2.5, GOLD),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ]))
                elements.append(callout_d)
        else:
            PdfExporter._render_generic_markdown(elements, content, styles)

    @staticmethod
    def _render_swot_section(elements: List[Any], content: str, styles: Dict[str, ParagraphStyle]):
        def get_bullets(heading: str) -> List[str]:
            m = re.search(rf"\*\*{heading}\*\*\s*\n([\s\S]*?)(?=\n\*\*|$)", content, re.I)
            if not m:
                return []
            return [l.strip()[2:].strip() for l in m.group(1).split("\n") if l.strip().startswith("- ") or l.strip().startswith("* ")]

        s_list = get_bullets("Strengths")
        w_list = get_bullets("Weaknesses")
        o_list = get_bullets("Opportunities")
        t_list = get_bullets("Threats")

        if s_list or w_list or o_list or t_list:
            def format_box(title: str, items: List[str], color_hex: str) -> List[Any]:
                flow = [Paragraph(f'<font color="{color_hex}"><b>{title.upper()}</b></font>', styles["TableHead"]), Spacer(1, 4)]
                for it in items[:4]:
                    flow.append(Paragraph(f'<font color="{color_hex}">•</font> &nbsp;{it}', styles["TableCell"]))
                    flow.append(Spacer(1, 2.5))
                return flow

            s_cell = format_box("Strengths", s_list, "#15803D")
            w_cell = format_box("Weaknesses", w_list, "#B45309")
            o_cell = format_box("Opportunities", o_list, "#1D4ED8")
            t_cell = format_box("Threats", t_list, "#BE123C")

            swot_table = Table([[s_cell, w_cell], [o_cell, t_cell]], colWidths=[248, 247])
            swot_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#F0FDF4")),
                ("BOX", (0, 0), (0, 0), 0.5, colors.HexColor("#BBF7D0")),
                ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#FFFBEB")),
                ("BOX", (1, 0), (1, 0), 0.5, colors.HexColor("#FDE68A")),
                ("BACKGROUND", (0, 1), (0, 1), colors.HexColor("#EFF6FF")),
                ("BOX", (0, 1), (0, 1), 0.5, colors.HexColor("#BFDBFE")),
                ("BACKGROUND", (1, 1), (1, 1), colors.HexColor("#FFF1F2")),
                ("BOX", (1, 1), (1, 1), 0.5, colors.HexColor("#FECDD3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]))
            elements.append(swot_table)
        else:
            PdfExporter._render_generic_markdown(elements, content, styles)

    @staticmethod
    def _render_risk_section(elements: List[Any], content: str, styles: Dict[str, ParagraphStyle]):
        # Extract Risk Level
        rl_m = re.search(r"-\s*\*\*Assessed Risk Level:\*\*\s*([^\n[]+)", content)
        if rl_m:
            r_level = rl_m.group(1).strip()
            v_style = VERDICT_COLORS.get(r_level.lower(), VERDICT_COLORS["high risk"])
            pill = Table([[
                Paragraph(f'<font size="8" color="{v_style["text"].hexval()}"><b>ASSESSED RISK LEVEL: {r_level.upper()}</b></font>', styles["Body"])
            ]], colWidths=[210])
            pill.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), v_style["bg"]),
                ("BOX", (0, 0), (-1, -1), 0.5, v_style["border"]),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]))
            elements.append(pill)
            elements.append(Spacer(1, 8))

        # Check for Primary Failure Risks and Mitigations to render as structured cards
        p_risks = []
        p_match = re.search(r"\*\*Primary Failure Risks:\*\*\s*\n([\s\S]*?)(?=\n\*\*Mitigation|$)", content)
        if p_match:
            p_risks = [l.strip()[2:].strip() for l in p_match.group(1).split("\n") if l.strip().startswith("- ") or l.strip().startswith("* ")]

        m_recs = []
        m_match = re.search(r"\*\*Mitigation Recommendations:\*\*\s*\n([\s\S]*?)(?=\n\*\*|$)", content)
        if m_match:
            m_recs = [l.strip()[2:].strip() for l in m_match.group(1).split("\n") if l.strip().startswith("- ") or l.strip().startswith("* ")]

        if p_risks and m_recs:
            r_flow = [Paragraph("<b>PRIMARY FAILURE RISKS</b>", ParagraphStyle("RTitle", fontName=FONT_BOLD, fontSize=8.0, leading=10, textColor=colors.HexColor("#BE123C"))), Spacer(1, 4)]
            for pr in p_risks:
                r_flow.append(Paragraph(f'<font color="#BE123C"><b>•</b></font> &nbsp;{pr}', styles["TableCell"]))
                r_flow.append(Spacer(1, 3))

            m_flow = [Paragraph("<b>DEFENSIVE MITIGATION PLAYBOOKS</b>", ParagraphStyle("MTitle", fontName=FONT_BOLD, fontSize=8.0, leading=10, textColor=colors.HexColor("#15803D"))), Spacer(1, 4)]
            for mr in m_recs:
                m_flow.append(Paragraph(f'<font color="#15803D"><b>•</b></font> &nbsp;{mr}', styles["TableCell"]))
                m_flow.append(Spacer(1, 3))

            rm_table = Table([[r_flow, m_flow]], colWidths=[247, 248])
            rm_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#FFF1F2")),
                ("BOX", (0, 0), (0, 0), 0.5, colors.HexColor("#FECDD3")),
                ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#F0FDF4")),
                ("BOX", (1, 0), (1, 0), 0.5, colors.HexColor("#BBF7D0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]))
            elements.append(rm_table)
        else:
            PdfExporter._render_generic_markdown(elements, content, styles, filter_out_risk_level=True)

    @staticmethod
    def _render_failure_scenarios_section(elements: List[Any], content: str, styles: Dict[str, ParagraphStyle]):
        scenarios = []
        warning_indicators = []
        in_warnings = False

        for line in content.split("\n"):
            line_str = line.strip()
            if not line_str:
                continue
            if "warning indicator" in line_str.lower():
                in_warnings = True
                continue
            if line_str.startswith("- ") or line_str.startswith("* "):
                bullet = line_str[2:].strip()
                if in_warnings:
                    warning_indicators.append(bullet)
                elif "assessed risk" not in bullet.lower() and "insufficient" not in bullet.lower():
                    scenarios.append(bullet)

        if scenarios:
            rows = []
            for i, sc in enumerate(scenarios, start=1):
                clean_sc = sc.replace("**", "")
                rows.append([
                    Paragraph(f"<font color='#BE123C'><b>Scenario {i:02d}</b></font>", styles["TableCellBold"]),
                    Paragraph(clean_sc, styles["TableCell"]),
                ])
            sc_table = Table(rows, colWidths=[90, 415], repeatRows=1)
            sc_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#FFF1F2")),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]))
            elements.append(sc_table)

            if warning_indicators:
                elements.append(Spacer(1, 8))
                warn_flow = [Paragraph("<b>EARLY WARNING INDICATORS & TELEMETRY TRIGGERS</b>", ParagraphStyle("WT", fontName=FONT_BOLD, fontSize=8.0, leading=10, textColor=colors.HexColor("#B45309"))), Spacer(1, 3)]
                for wi in warning_indicators:
                    warn_flow.append(Paragraph(f'<font color="#B45309"><b>▲</b></font> &nbsp;{wi}', styles["TableCell"]))
                    warn_flow.append(Spacer(1, 2))
                w_table = Table([[warn_flow]], colWidths=[505])
                w_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFBEB")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#FDE68A")),
                    ("LINELEFT", (0, 0), (0, 0), 2.5, colors.HexColor("#B45309")),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ]))
                elements.append(w_table)
        else:
            PdfExporter._render_generic_markdown(elements, content, styles)

    @staticmethod
    def _render_execution_roadmap_section(elements: List[Any], content: str, styles: Dict[str, ParagraphStyle]):
        # Extract Phase blocks
        phases = []
        phase_details = {}

        for line in content.split("\n"):
            line_str = line.strip()
            if not line_str:
                continue
            # Look for bullet phases: - Phase 1: ...
            p_match = re.search(r"^-\s*Phase\s*(\d+)[:\s]+(.+)", line_str, re.I)
            if p_match:
                p_num = int(p_match.group(1))
                p_desc = p_match.group(2).strip()
                phases.append((p_num, p_desc))
            
            # Look for duration notes: **Phase 1 (Months 1-3):** ...
            d_match = re.search(r"\*\*Phase\s*(\d+)(?:\s*\(([^)]+)\))?:\*\*\s*(.+)", line_str, re.I)
            if d_match:
                d_num = int(d_match.group(1))
                d_time = d_match.group(2).strip() if d_match.group(2) else ""
                d_detail = d_match.group(3).strip()
                phase_details[d_num] = (d_time, d_detail)

        if phases:
            rows = []
            for p_num, p_desc in phases:
                time_str, detail = phase_details.get(p_num, ("", ""))
                badge_text = f"PHASE {p_num:02d}"
                if time_str:
                    badge_text += f"<br/><font size='6.5' color='#667085'>{time_str}</font>"

                content_flow = [
                    Paragraph(f"<b>{p_desc}</b>", styles["TableCellBold"]),
                ]
                if detail:
                    content_flow.extend([
                        Spacer(1, 2),
                        Paragraph(f"<font color='#475467'>{detail}</font>", styles["TableCell"])
                    ])

                rows.append([
                    Paragraph(f"<para align='center'><font color='#5B5CEB'><b>{badge_text}</b></font></para>", styles["TableCell"]),
                    content_flow
                ])

            roadmap_table = Table(rows, colWidths=[90, 415], repeatRows=1)
            roadmap_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F4F3FF")),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]))
            elements.append(roadmap_table)
        else:
            PdfExporter._render_generic_markdown(elements, content, styles)

    @staticmethod
    def _render_final_recommendation_section(elements: List[Any], content: str, styles: Dict[str, ParagraphStyle]):
        # Extract verdict, directives, priorities, and factors
        verdict_val = "Evaluation Complete"
        v_m = re.search(r"\*\*Venture Studio Verdict:\*\*\s*(.+)", content)
        if v_m:
            verdict_val = v_m.group(1).strip()

        directives_val = ""
        d_m = re.search(r"\*\*Strategic Directives:\*\*\s*\n?([^\n*]+)", content)
        if d_m:
            directives_val = d_m.group(1).strip()

        # Directive Callout
        v_key = verdict_val.lower()
        v_style = VERDICT_COLORS.get(v_key, VERDICT_COLORS["medium risk"])
        d_flow = [
            Paragraph(f'<font color="{v_style["text"].hexval()}"><b>VENTURE STUDIO VERDICT: {verdict_val.upper()}</b></font>', styles["TableHead"]),
            Spacer(1, 2),
            Paragraph(directives_val or "Preserve capital, execute rigorous primary customer validation, and confirm unit economics before platform scale.", styles["Callout"])
        ]
        d_table = Table([[d_flow]], colWidths=[505])
        d_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), v_style["bg"]),
            ("BOX", (0, 0), (-1, -1), 0.5, v_style["border"]),
            ("LINELEFT", (0, 0), (0, 0), 3, v_style["text"]),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]))
        elements.append(d_table)
        elements.append(Spacer(1, 8))

        # Two-column: Priorities & Factors
        priorities = []
        p_m = re.search(r"\*\*Execution Priorities:\*\*\s*\n([\s\S]*?)(?=\n\*\*Critical Success Factors|$)", content)
        if p_m:
            priorities = [l.strip()[2:].strip() for l in p_m.group(1).split("\n") if l.strip().startswith("- ") or l.strip().startswith("* ")]

        factors = []
        f_m = re.search(r"\*\*Critical Success Factors:\*\*\s*\n([\s\S]*?)(?=\n\*\*|$)", content)
        if f_m:
            factors = [l.strip()[2:].strip() for l in f_m.group(1).split("\n") if l.strip().startswith("- ") or l.strip().startswith("* ")]

        if priorities or factors:
            p_flow = [Paragraph("<b>EXECUTION PRIORITIES</b>", ParagraphStyle("EPT", fontName=FONT_BOLD, fontSize=8.0, leading=10, textColor=PURPLE)), Spacer(1, 4)]
            for pr in priorities:
                p_flow.append(Paragraph(f'<font color="#5B5CEB"><b>•</b></font> &nbsp;{pr}', styles["TableCell"]))
                p_flow.append(Spacer(1, 2.5))

            f_flow = [Paragraph("<b>CRITICAL SUCCESS FACTORS</b>", ParagraphStyle("CFT", fontName=FONT_BOLD, fontSize=8.0, leading=10, textColor=NAVY)), Spacer(1, 4)]
            for fc in factors:
                f_flow.append(Paragraph(f'<font color="#C99A3D"><b>•</b></font> &nbsp;{fc}', styles["TableCell"]))
                f_flow.append(Spacer(1, 2.5))

            pf_table = Table([[p_flow, f_flow]], colWidths=[247, 248])
            pf_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), BG_GRAY),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]))
            elements.append(pf_table)
        else:
            PdfExporter._render_generic_markdown(elements, content, styles)

    @staticmethod
    def _render_citations_section(elements: List[Any], content: str, citations: List[Any], styles: Dict[str, ParagraphStyle]):
        # Parse citations either from citations list or content markdown
        parsed_cits = []
        if citations:
            for c in citations:
                cid = getattr(c, "id", "") or c.get("id", "REF")
                url = getattr(c, "source_url", "") or c.get("source_url", "")
                snip = getattr(c, "snippet", "") or c.get("snippet", "")
                parsed_cits.append((cid, snip or "Verified intelligence reference", url))
        else:
            for line in content.split("\n"):
                line_str = line.strip()
                m = re.search(r"-\s*\[([^\]]+)\]\s*([^:]+):\s*(https?://[^\s]+)", line_str)
                if m:
                    parsed_cits.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))

        if parsed_cits:
            rows = [[
                Paragraph("<b>ID</b>", styles["TableHead"]),
                Paragraph("<b>SOURCE TITLE & CONTEXT</b>", styles["TableHead"]),
                Paragraph("<b>DOMAIN / URL</b>", styles["TableHead"]),
            ]]
            for cid, snip, url in parsed_cits:
                domain = re.sub(r"^https?://(?:www\.)?", "", url).split("/")[0] if url else "Intelligence Reference"
                url_display = f'<a href="{url}"><font color="#5B5CEB"><u>{domain}</u></font></a>' if url.startswith("http") else domain

                rows.append([
                    Paragraph(f'<font color="#5B5CEB"><b>[{cid}]</b></font>', styles["TableCellBold"]),
                    Paragraph(snip, styles["TableCell"]),
                    Paragraph(url_display, styles["TableCellMuted"]),
                ])

            c_table = Table(rows, colWidths=[45, 335, 125], repeatRows=1)
            c_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F4F3FF")),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]))
            elements.append(c_table)

            # Methodology Note
            meth_m = re.search(r"\*\*Research Methodology:\*\*\s*([\s\S]+)", content)
            if meth_m:
                meth_text = meth_m.group(1).strip()
                elements.append(Spacer(1, 6))
                elements.append(Paragraph(f'<font size="7.5" color="#667085"><b>Research Methodology:</b> {meth_text}</font>', styles["TableCellMuted"]))
        else:
            PdfExporter._render_generic_markdown(elements, content, styles)

    # -----------------------------------------------------------------------
    # Generic Markdown to Flowable Parser
    # -----------------------------------------------------------------------
    @staticmethod
    def _render_generic_markdown(elements: List[Any], content: str, styles: Dict[str, ParagraphStyle], filter_out_risk_level: bool = False):
        raw_lines = content.split("\n")
        callout_lines = []

        for line in raw_lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Filter out duplicated top markdown titles
            if line_str.startswith("# ") or (line_str.startswith("## ") and not line_str.startswith("### ")):
                clean_h = re.sub(r"^#{1,3}\s*", "", line_str).strip()
                if "section" in clean_h.lower() or len(clean_h) < 40:
                    continue

            if filter_out_risk_level and "assessed risk level" in line_str.lower():
                continue

            # Callout block > ...
            if line_str.startswith(">"):
                callout_text = line_str.lstrip(">").replace("[!NOTE]", "").replace("[!IMPORTANT]", "").strip()
                if callout_text:
                    callout_lines.append(callout_text)
                continue
            elif callout_lines:
                # Flush callout
                p = Paragraph(" ".join(callout_lines), styles["Callout"])
                t = Table([[p]], colWidths=[505])
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), BG_GRAY),
                    ("LINELEFT", (0, 0), (0, 0), 2.5, PURPLE),
                    ("BOX", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ]))
                elements.append(t)
                elements.append(Spacer(1, 4))
                callout_lines = []

            # Subheadings: ### Heading or **Heading:**
            if line_str.startswith("### "):
                sub_title = line_str[4:].strip()
                elements.append(Paragraph(sub_title, styles["SubHeading"]))
                continue

            if line_str.startswith("**") and (line_str.endswith(":**") or line_str.endswith("**")) and len(line_str) < 65:
                sub_title = line_str.replace("*", "").rstrip(":").strip()
                elements.append(Paragraph(sub_title, styles["SubHeading"]))
                continue

            # Bullet points
            if line_str.startswith("- ") or line_str.startswith("* "):
                bullet_text = line_str[2:].strip()
                bullet_html = PdfExporter._markdown_to_xml(bullet_text)
                p = Paragraph(f'<font color="#5B5CEB"><b>•</b></font> &nbsp;{bullet_html}', styles["Bullet"])
                elements.append(p)
                continue

            # Standard paragraph
            p_html = PdfExporter._markdown_to_xml(line_str)
            elements.append(Paragraph(p_html, styles["Body"]))

        # Flush any remaining callout lines
        if callout_lines:
            p = Paragraph(" ".join(callout_lines), styles["Callout"])
            t = Table([[p]], colWidths=[505])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), BG_GRAY),
                ("LINELEFT", (0, 0), (0, 0), 2.5, PURPLE),
                ("BOX", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]))
            elements.append(t)

    # -----------------------------------------------------------------------
    # Helper Utilities
    # -----------------------------------------------------------------------
    @staticmethod
    def _add_section_header(elements: List[Any], num: str, title: str, subtitle: Optional[str], styles: Dict[str, ParagraphStyle]):
        header_elements = [
            Paragraph(num, styles["SectionNum"]),
            Spacer(1, 2),
            Paragraph(title, styles["SectionHeading"])
        ]
        if subtitle:
            header_elements.extend([
                Spacer(1, 2),
                Paragraph(subtitle, styles["SectionSub"])
            ])
        elements.append(KeepTogether(header_elements))

    @staticmethod
    def _markdown_to_xml(text: str) -> str:
        text = html_escape(text)
        # Bold **text** -> <b>text</b>
        text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
        # Italic *text* -> <i>text</i>
        text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
        return text

    @staticmethod
    def _find_section(data: Dict[str, Any], candidate_titles: List[str]) -> Optional[Dict[str, Any]]:
        sections = data.get("sections", [])
        for s in sections:
            t = s.get("title", "").lower()
            if any(c in t for c in candidate_titles):
                return s
        return None

    @staticmethod
    def _extract_bullets(data: Dict[str, Any], section_key: str, candidate_headings: List[str]) -> List[str]:
        sec = data.get(section_key) or PdfExporter._find_section(data, candidate_headings)
        if not sec:
            return []
        content = sec.get("content_markdown", "")
        bullets = []
        capturing = False
        normalized = [h.replace(" ", "").lower() for h in candidate_headings]

        for line in content.split("\n"):
            l = line.strip()
            if not l:
                continue
            is_head = l.startswith("#") or (l.startswith("**") and l.endswith("**"))
            if is_head:
                clean = l.replace("#", "").replace("*", "").replace(" ", "").lower()
                if any(n in clean for n in normalized):
                    capturing = True
                    continue
                elif capturing:
                    break
            if capturing and (l.startswith("- ") or l.startswith("* ")):
                b = l[2:].strip()
                if b and "insufficient" not in b.lower():
                    bullets.append(b)
        return bullets

    @staticmethod
    def _extract_risks(data: Dict[str, Any]) -> List[str]:
        primary = PdfExporter._extract_bullets(data, "critic_analysis", ["Primary Failure Risks", "Failure Risks", "Key Risks", "Top Risks"])
        if primary:
            return primary
        threats = PdfExporter._extract_bullets(data, "swot_analysis", ["Threats"])
        weaknesses = PdfExporter._extract_bullets(data, "swot_analysis", ["Weaknesses"])
        combined = threats + weaknesses
        return combined if combined else []


def html_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
