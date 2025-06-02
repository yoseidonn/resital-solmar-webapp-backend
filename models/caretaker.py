from tortoise import fields
from tortoise.models import Model

class CareTaker(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=255)
    phone_number = fields.CharField(max_length=50, null=True, blank=True) 
    assigned_villas = fields.JSONField(null=True, blank=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.name
