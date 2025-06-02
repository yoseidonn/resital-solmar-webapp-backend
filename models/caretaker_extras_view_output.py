from tortoise import fields
from tortoise.models import Model
from models import ResortReportFile

class CaretakerExtrasViewOutput(Model):
    id = fields.IntField(pk=True)
    resort_report_file = fields.ForeignKeyField('models.ResortReportFile', related_name='caretaker_extras_view_outputs')
    user_name = fields.CharField(max_length=255, null=True)
    fileName = fields.CharField(max_length=255)
    generatedDate = fields.DatetimeField()
    messages = fields.JSONField(null=True)
    rows = fields.JSONField(null=True)
    content = fields.JSONField(null=True)
    file_path = fields.CharField(max_length=512, null=True)
    created_at = fields.DatetimeField(auto_now_add=True) 