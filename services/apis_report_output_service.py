from models import APISReportOutput as APISReportOutputModel, APISReportFile as APISReportFileModel, AdvancedPassengerInformation as AdvancedPassengerInformationModel
from schemas.apis_report_output import APISReportOutputGenerateRequest, APISReportOutput
from typing import List, Dict, Any
import io
import openpyxl
import os
from tortoise.transactions import in_transaction
from datetime import datetime
from utils.serialization import serialize

OUTPUT_DIR = "media/apis_report_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def get_all_outputs() -> List[APISReportOutput]:
    serializer = [APISReportOutput.model_validate(o) for o in await APISReportOutputModel.all()]
    return [await serialize(s) for s in serializer]

async def create_output(user_name: str, 
                        apis_report_file_id: int, 
                        file_name: str, 
                        file_path: str, 
                        individual_reservations: List[dict]
                        ) -> APISReportOutput:
    output = await APISReportOutputModel.create(
        user_name=user_name,
        apis_report_file_id=apis_report_file_id,
        fileName=file_name,
        file_path=file_path,
        individual_reservations=individual_reservations,
        generatedDate=datetime.now(),
    )
    serializer = APISReportOutput.model_validate(output)
    return await serialize(serializer)

async def get_outputs_by_file(apis_report_file_id: int) -> List[APISReportOutput]:
    outputs = await APISReportOutputModel.filter(apis_report_file_id=apis_report_file_id).all()
    serializer = [APISReportOutput.model_validate(o) for o in outputs]
    return [await serialize(s) for s in serializer]

async def generate_apis_report_output(
    apis_report_file: APISReportFileModel,
    request: APISReportOutputGenerateRequest
) -> APISReportOutput:
    """
    Generate APIS report output using database records instead of parsing Excel files
    """
    # Fetch DB records - use the database models instead of parsing files
    records = await AdvancedPassengerInformationModel.filter(
        apis_report_file_id=apis_report_file.id,
        opportunity_name=request.opportunity_name
    ).all()
    
    # Prepare Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "APIS Report"
    headers = request.headers
    ws.append(headers)
    
    # Write database records to Excel
    for passenger_info in records:
        row_data = []
        for header in headers:
            # Convert header to snake_case to match model attributes
            attr_name = _to_snake_case(header)
            value = getattr(passenger_info, attr_name, '')
            
            # Format dates and datetimes properly
            if hasattr(passenger_info, attr_name):
                attr_value = getattr(passenger_info, attr_name)
                if isinstance(attr_value, datetime):
                    value = attr_value.strftime('%Y-%m-%d %H:%M:%S')
                elif hasattr(attr_value, 'isoformat'):  # date objects
                    value = attr_value.isoformat()
                else:
                    value = str(attr_value) if attr_value is not None else ''
            
            row_data.append(value)
        ws.append(row_data)
    
    # Add individual villa entries if provided
    for entry in request.individual_villa_entries:
        row_data = []
        for header in headers:
            attr_name = _to_snake_case(header)
            value = getattr(entry, attr_name, '') if hasattr(entry, attr_name) else ''
            row_data.append(str(value))
        ws.append(row_data)
    
    # Save Excel to disk
    filename = f"apis_report_output_{apis_report_file.id}_{request.opportunity_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    file_path = os.path.join(OUTPUT_DIR, filename)
    wb.save(file_path)
    wb.close()
    
    # Save output to DB
    output = await create_output(
        user_name="system",
        apis_report_file_id=apis_report_file.id,
        file_name=filename,
        file_path=file_path,
        individual_reservations=[entry.dict() for entry in request.individual_villa_entries] if request.individual_villa_entries else [],
    )
    return output

async def get_file_path(output_id: str) -> str:
    output = await APISReportOutputModel.get_or_none(fileName=output_id)
    if not output:
        raise FileNotFoundError("Output not found")
    serializer = APISReportOutput.model_validate(output)
    return await serialize(serializer)["file_path"]

def _to_snake_case(header: str) -> str:
    """Convert header to snake_case to match model field names"""
    return header.lower().replace(" ", "_").replace("-", "_") 