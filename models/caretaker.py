from tortoise import fields
from tortoise.models import Model

class CareTaker(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    phone_number = fields.CharField(max_length=50) 
    villa_assignments = fields.JSONField()
    rules = fields.JSONField(null=True)