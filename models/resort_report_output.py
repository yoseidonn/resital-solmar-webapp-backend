from tortoise import fields
from tortoise.models import Model
from models import ResortReportFile

class ResortReportOutput(Model):
    id = fields.IntField(pk=True)
    resort_report_file = fields.ForeignKeyField('models.ResortReportFile', related_name='outputs')
    content = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True) 