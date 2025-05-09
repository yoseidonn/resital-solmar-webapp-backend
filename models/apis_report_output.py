from tortoise import fields
from tortoise.models import Model

class APISReportOutput(Model):
    id = fields.IntField(pk=True)
    apis_report_file = fields.ForeignKeyField('models.APISReportFile', related_name='outputs')
    file_path = fields.CharField(max_length=512)  # Path to the generated Excel file
    individual_reservations = fields.JSONField(null=True)  # Store individual villa entries as JSON
    created_at = fields.DatetimeField(auto_now_add=True) 