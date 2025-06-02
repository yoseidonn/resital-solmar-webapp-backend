from models import CaretakerExtrasViewOutput as CaretakerExtrasViewOutputModel, ResortReportFile
from schemas import CaretakerExtrasViewOutput
from services.resort_report_service import get_reports_by_file
from utils import filtering
from tortoise.transactions import in_transaction
from typing import List, Dict, Any
import openpyxl
import os
from datetime import datetime, timezone
from utils.serialization import serialize

OUTPUT_DIR = "media/caretaker_extras_view_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def create_output(user_name: str, resort_report_file_id: int, content: str, file_name: str, file_path: str) -> CaretakerExtrasViewOutput:
    output = await CaretakerExtrasViewOutputModel.create(
        user_name=user_name,
        resort_report_file_id=resort_report_file_id,
        content=content,
        fileName=file_name,
        file_path=file_path,
        generatedDate=datetime.now(timezone.utc),
    )
    serializer = CaretakerExtrasViewOutput.model_validate(output)
    return await serialize(serializer)

async def get_outputs_by_file(resort_report_file_id: int) -> List[CaretakerExtrasViewOutput]:
    outputs = await CaretakerExtrasViewOutputModel.filter(resort_report_file_id=resort_report_file_id).all()
    serializer = [CaretakerExtrasViewOutput.model_validate(o) for o in outputs]
    return [await serialize(s) for s in serializer]

async def generate_caretaker_extras_view_output(resort_report_file: ResortReportFile, 
                                                selected_users: List[Any], 
                                                headers: List[str], 
                                                individual_villa_entries: List[Any] = None
                                                ) -> Dict[str, str]:
    """
    For each user, generate a formatted caretaker extras view output, save it, and return all outputs as a dict.
    selected_users: List of user objects, each with .name, .villa_assignments, .rules
    headers: List of column names for Excel export
    individual_villa_entries: List of manual reservation dicts to include
    """
    outputs = {}
    file_name = f"caretaker_extras_view_output_{resort_report_file.id}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.xlsx"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Caretaker Extras View"
    ws.append(headers)
    individual_villa_entries = individual_villa_entries or []
    async with in_transaction():
        for user in selected_users:
            user_output = ""
            villa_assignments = user.villa_assignments  # dict {villa_name: [extras]}
            for villa_name, user_extras in villa_assignments.items():
                user_output += f"*{villa_name}\n"
                # Get all resort reports for that villa
                reports = await get_reports_by_file(resort_report_file)
                villa_reports = [r for r in reports if getattr(r, 'villa_id', None) == villa_name or getattr(r, 'villa', None) == villa_name]
                # Add individual entries for this villa
                villa_manuals = [entry for entry in individual_villa_entries if str(entry.get('villa_name')) == str(villa_name)]
                class Dummy:
                    def __init__(self, d):
                        self.__dict__.update(d)
                villa_reports += [Dummy(entry) for entry in villa_manuals]
                # Filter reports by user.rules
                filtered_reports = filtering.filter_reservations_by_villa_rules(villa_reports, user_extras)
                for report in filtered_reports:
                    user_output += f"{report.holiday_start_date} - {report.holiday_end_date}"
                    extras = []
                    if hasattr(report, 'extras_aggregated'):
                        if user_extras.get('Complementary Cot') and 'Complementary Cot' in report.extras_aggregated:
                            extras.append("Bebek yatağı")
                        if user_extras.get('Pool Heating') and 'Pool Heating' in report.extras_aggregated:
                            extras.append("Havuz ısıtması")
                        if user_extras.get('Welcome Pack') and 'Welcome Pack' in report.extras_aggregated:
                            size = filtering.extract_welcome_pack_size(report.extras_aggregated)
                            extras.append(f"{size} kişilik welcome paketi")
                    if extras:
                        user_output += ", " + ("(" if extras else "") + ", ".join(extras) + (")" if extras else "")
                    user_output += "\n"
                    # Write to Excel
                    ws.append([getattr(report, header, '') for header in headers])
                user_output += "\n"
                ws.append([])  # Blank row between villas
            outputs[user.name] = user_output
    wb.save(file_path)
    return await create_output(
        user_name="system",
        resort_report_file_id=resort_report_file.id,
        content=str(outputs),
        file_name=file_name,
        file_path=file_path,
    )