from models import ResortReportOutput, ResortReportFile, ResortReport
from schemas import ResortReportOutputSchema
from services import resort_report_service
from utils import filtering
from tortoise.transactions import in_transaction
from typing import List, Dict, Any

async def create_output(user_name: str, resort_report_file_id: int, content: str) -> ResortReportOutput:
    return await ResortReportOutput.create(
        user_name=user_name,
        resort_report_file_id=resort_report_file_id,
        content=content
    )

async def get_outputs_by_file(resort_report_file_id: int) -> List[ResortReportOutput]:
    return await ResortReportOutput.filter(resort_report_file_id=resort_report_file_id).all()

async def generate_resort_report_output(resort_report_file: ResortReportFile, selected_users: List[Any]) -> Dict[str, str]:
    """
    For each user, generate a formatted resort report output, save it, and return all outputs as a dict.
    selected_users: List of user objects, each with .name, .villa_assignments, .rules
    """
    outputs = {}
    async with in_transaction():
        for user in selected_users:
            user_output = ""
            villa_assignments = user.villa_assignments  # dict {villa_name: {extras_config}}
            for villa_name, extras_config in villa_assignments.items():
                user_output += f"*{villa_name}\n"
                # Get all resort reports for that villa
                reports = await resort_report_service.list_all()
                villa_reports = [r for r in reports if getattr(r, 'villa_id', None) == villa_name or getattr(r, 'villa', None) == villa_name]
                # Filter reports by user.rules
                filtered_reports = filtering.filter_reservations_by_villa_rules(villa_reports, villa_assignments, user.rules)
                for report in filtered_reports:
                    user_output += f"{report.holiday_start_date} - {report.holiday_end_date}"
                    extras = []
                    if hasattr(report, 'extras_aggregated'):
                        if 'Complementary Cot' in report.extras_aggregated and report.extras_aggregated['Complementary Cot']:
                            extras.append("Bebek yatağı")
                        if 'Pool Heating' in report.extras_aggregated and report.extras_aggregated['Pool Heating']:
                            extras.append("Havuz ısıtması")
                        if 'Welcome Pack' in report.extras_aggregated and report.extras_aggregated['Welcome Pack']:
                            size = filtering.extract_welcome_pack_size(report.extras_aggregated)
                            extras.append(f"{size} kişilik welcome paketi")
                    if extras:
                        user_output += ", " + ("(" if extras else "") + ", ".join(extras) + (")" if extras else "")
                    user_output += "\n"
                user_output += "\n"
            outputs[user.name] = user_output
    await ResortReportOutput.create(
        resort_report_file=resort_report_file,
        content=outputs
    )
    return outputs 