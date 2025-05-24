from tortoise import fields
from tortoise.models import Model

class CareTaker(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=255)
    phone_number = fields.CharField(max_length=50, null=True) 
    villa_assignments = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)