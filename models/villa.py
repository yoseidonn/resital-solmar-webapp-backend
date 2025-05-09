from tortoise import fields
from tortoise.models import Model

class Villa(Model):
    id = fields.IntField(pk=True)
    villa_name = fields.CharField(max_length=255)
    care_taker = fields.ForeignKeyField('models.CareTaker', related_name='villas')
 