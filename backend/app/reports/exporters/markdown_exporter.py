from app.reports.models import ExecutiveReport
import os

class MarkdownExporter:
    @staticmethod
    def export(report: ExecutiveReport, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"report_{report.report_id}.md")
        
        md_content = []
        
        # Use complete 21 sections if populated, otherwise fallback to legacy list
        if getattr(report, "sections", None) and len(report.sections) > 0:
            sections = report.sections
        else:
            sections = [
                report.executive_summary,
                report.market_research,
                report.swot_analysis,
                report.competitor_analysis,
                report.pricing_strategy,
                report.financial_analysis,
                report.go_to_market_strategy,
                report.critic_analysis,
                report.evidence_citations,
                report.final_recommendation
            ]
        
        for section in sections:
            md_content.append(section.content_markdown)
            if section.citations:
                md_content.append("\n**Sources:**")
                for cit in section.citations:
                    md_content.append(f"- [{cit.id}] {cit.source_url}: {cit.snippet}")
            md_content.append("\n---\n")
            
        final_md = "\n".join(md_content)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_md)
            
        return file_path
