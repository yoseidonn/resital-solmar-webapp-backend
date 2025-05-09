from tortoise import fields
from tortoise.models import Model

class ResortReportFile(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    date = fields.DateField()
    uploaded_at = fields.DatetimeField(auto_now_add=True)
    file = fields.CharField(max_length=255) 