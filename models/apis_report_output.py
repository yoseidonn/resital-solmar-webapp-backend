from tortoise import fields
from tortoise.models import Model

class APISReportOutput(Model):
    id = fields.CharField(pk=True, max_length=64)
    apis_report_file = fields.ForeignKeyField('models.APISReportFile', related_name='outputs')
    fileName = fields.CharField(max_length=255)
    generatedDate = fields.DatetimeField()
    villa = fields.CharField(max_length=255, null=True)
    date = fields.CharField(max_length=32, null=True)
    rows = fields.JSONField(null=True)
    messages = fields.JSONField(null=True)
    file_path = fields.CharField(max_length=512)
    created_at = fields.DatetimeField(auto_now_add=True) 