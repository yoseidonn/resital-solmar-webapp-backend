from models import APISReportOutput, APISReportFile, AdvancedPassengerInformation
from schemas.apis_report_output import APISReportOutputGenerateRequest
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any
import io
import openpyxl
import os
from tortoise.transactions import in_transaction
from datetime import datetime

OUTPUT_DIR = "media/apis_report_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def create_output(user_name: str, apis_report_file_id: int, content: str) -> APISReportOutput:
    return await APISReportOutput.create(
        user_name=user_name,
        apis_report_file_id=apis_report_file_id,
        content=content
    )

async def get_outputs_by_file(apis_report_file_id: int) -> List[APISReportOutput]:
    return await APISReportOutput.filter(apis_report_file_id=apis_report_file_id).all()

async def generate_apis_report_output(
    apis_report_file: APISReportFile,
    request: APISReportOutputGenerateRequest
) -> StreamingResponse:
    # Fetch DB records
    records = await AdvancedPassengerInformation.filter(
        apis_file_id=apis_report_file.id,
        opportunity_name=request.opportunity_name
    ).all()
    # Prepare Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(request.headers)
    for api in records:
        row = [getattr(api, _to_snake_case(h), "") for h in request.headers]
        ws.append(row)
    # Add individual villa entries (if not already present)
    for entry in request.individual_villa_entries:
        if not any(str(api.opportunity_name) == entry.opportunity_name for api in records):
            row = [getattr(entry, _to_snake_case(h), getattr(entry, h, "")) for h in request.headers]
            ws.append(row)
    # Save Excel to disk
    filename = f"apis_report_output_{apis_report_file.id}_{request.opportunity_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    file_path = os.path.join(OUTPUT_DIR, filename)
    wb.save(file_path)
    # Save output to DB
    await APISReportOutput.create(
        apis_report_file=apis_report_file,
        file_path=file_path,
        individual_reservations=[entry.dict() for entry in request.individual_villa_entries],
    )
    # Stream Excel
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

def _to_snake_case(header: str) -> str:
    return header.lower().replace(" ", "_") 