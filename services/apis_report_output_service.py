from models import APISReportOutput, APISReportFile, AdvancedPassengerInformation
from schemas.apis_report_output import APISReportOutputGenerateRequest, APISReportOutputSchema
from typing import List, Dict, Any
import io
import openpyxl
import os
from tortoise.transactions import in_transaction
from datetime import datetime

OUTPUT_DIR = "media/apis_report_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def get_all_outputs() -> List[APISReportOutputSchema]:
    return [APISReportOutputSchema(o) for o in await APISReportOutput.all().prefetch_related('apis_report_file')]

async def create_output(user_name: str, apis_report_file_id: int, file_name: str, file_path: str, individual_reservations: List[dict]) -> APISReportOutputSchema:
    output = await APISReportOutput.create(
        user_name=user_name,
        apis_report_file_id=apis_report_file_id,
        fileName=file_name,
        file_path=file_path,
        individual_reservations=individual_reservations,
        generatedDate=datetime.now(),
    )
    return APISReportOutputSchema(output)

async def get_outputs_by_file(apis_report_file_id: int) -> List[APISReportOutputSchema]:
    outputs = await APISReportOutput.filter(apis_report_file_id=apis_report_file_id).all().prefetch_related('apis_report_file')
    return [APISReportOutputSchema(o) for o in outputs]

async def generate_apis_report_output(
    apis_report_file: APISReportFile,
    request: APISReportOutputGenerateRequest
) -> APISReportOutputSchema:
    # Fetch DB records
    records = await AdvancedPassengerInformation.filter(
        apis_file_id=apis_report_file.id,
        opportunity_name=request.opportunity_name
    ).all()
    # Prepare Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "APIS Report"
    headers = request.headers
    ws.append(headers)
    for api in records:
        ws.append([getattr(api, header, '') for header in headers])
    for entry in request.individual_villa_entries:
        ws.append([getattr(entry, header, '') for header in headers])
    # Save Excel to disk
    filename = f"apis_report_output_{apis_report_file.id}_{request.opportunity_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    file_path = os.path.join(OUTPUT_DIR, filename)
    wb.save(file_path)
    # Save output to DB
    output = await create_output(
        user_name="system",
        apis_report_file_id=apis_report_file.id,
        file_name=filename,
        file_path=file_path,
        individual_reservations=[entry.dict() for entry in request.individual_villa_entries],
    )
    return output

async def get_file_path(output_id: str) -> str:
    output = await APISReportOutput.get_or_none(fileName=output_id).prefetch_related('apis_report_file')
    if not output:
        raise FileNotFoundError("Output not found")
    return output.file_path

def _to_snake_case(header: str) -> str:
    return header.lower().replace(" ", "_") 