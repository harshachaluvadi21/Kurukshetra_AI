from app.reports.models import ExecutiveReport
from pydantic import BaseModel
import json
import os

class JsonExporter:
    @staticmethod
    def export(report: ExecutiveReport, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"report_{report.report_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))
        return file_path
