from models import ExtrasFilteredReservationOutput, ResortReportFile
from schemas import ExtrasFilteredReservationOutputSchema
from services.resort_report_service import get_reports_by_file
from utils import filtering
from typing import List, Dict, Any
from datetime import datetime, timezone
import uuid
import openpyxl
import os

OUTPUT_DIR = "media/extras_filtered_reservation_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def get_all_outputs() -> List[ExtrasFilteredReservationOutputSchema]:
    return [ExtrasFilteredReservationOutputSchema.model_validate_json(o.json()) for o in await ExtrasFilteredReservationOutput.all()]

async def create_output(resort_report_file_id: int, file_name: str, file_path: str, applied_filters: Dict[str, List[str]], grouped_reservations: Dict[str, Any]) -> ExtrasFilteredReservationOutput:
    output = await ExtrasFilteredReservationOutput.create(
        id=str(uuid.uuid4()),
        resort_report_file_id=resort_report_file_id,
        file_name=file_name,
        generated_date=datetime.now(timezone.utc),
        applied_filters=applied_filters,
        grouped_reservations=grouped_reservations,
        file_path=file_path
    )
    return ExtrasFilteredReservationOutputSchema.model_validate_json(output.json())

async def generate_extras_filtered_reservation_summary(resort_report_file: ResortReportFile, filters: Dict[str, List[str]], headers: List[str], individual_villa_entries: List[Any] = None) -> Dict[str, str]:
    """
    Generate a filtered reservation summary based on extras for each villa.
    filters: Dict[villa_id, List[extras]]
    headers: List of column names for Excel export
    individual_villa_entries: List of manual reservation dicts to include
    """
    # Fetch all resort reports for the file
    reports = await get_reports_by_file(resort_report_file)
    grouped = {}
    individual_villa_entries = individual_villa_entries or []
    for villa_id, extras in filters.items():
        villa_reports = [r for r in reports if getattr(r, 'villa_id', None) == villa_id or getattr(r, 'villa', None) == villa_id]
        # Add individual entries for this villa
        villa_manuals = [entry for entry in individual_villa_entries if str(entry.get('villa_name')) == str(villa_id)]
        # Convert dicts to objects with attribute access for compatibility
        class Dummy:
            def __init__(self, d):
                self.__dict__.update(d)
        villa_reports += [Dummy(entry) for entry in villa_manuals]
        # Filter by extras
        grouped[villa_id] = filtering.filter_reservations_by_extras(villa_reports, extras)
    file_name = f"filtered_reservations_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.xlsx"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    _create_excel_file(file_path, grouped, headers)
    return await create_output(resort_report_file.id, file_name, file_path, filters, grouped)

def _create_excel_file(file_path: str, grouped: Dict[str, Any], headers: List[str]):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Filtered Reservations"
    ws.append(headers)
    for villa, reservations in grouped.items():
        for reservation in reservations:
            ws.append([getattr(reservation, header, '') for header in headers])

        # Add a blank row
        ws.append([])
    wb.save(file_path)

async def get_outputs_by_file(resort_report_file_id: int) -> List[ExtrasFilteredReservationOutput]:
    return await ExtrasFilteredReservationOutput.filter(resort_report_file_id=resort_report_file_id).all().prefetch_related('resort_report_file')

async def get_file_path(output_id: str) -> str:
    output = await ExtrasFilteredReservationOutput.get_or_none(id=output_id).prefetch_related('resort_report_file')
    if not output:
        raise FileNotFoundError("Output not found")
    return output.file_path
 