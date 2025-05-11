from tortoise import fields
from tortoise.models import Model
from models import ResortReportFile

class ResortReportOutput(Model):
    id = fields.CharField(pk=True, max_length=64)
    resort_report_file = fields.ForeignKeyField('models.ResortReportFile', related_name='outputs')
    fileName = fields.CharField(max_length=255)
    generatedDate = fields.DatetimeField()
    messages = fields.JSONField(null=True)
    rows = fields.JSONField(null=True)
    content = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True) 