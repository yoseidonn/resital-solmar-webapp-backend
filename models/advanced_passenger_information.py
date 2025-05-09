from tortoise import fields
from tortoise.models import Model

class AdvancedPassengerInformation(Model):
    id = fields.IntField(pk=True)
    account_name = fields.CharField(max_length=255)
    country = fields.CharField(max_length=255)
    passenger_name = fields.CharField(max_length=255)
    opportunity_name = fields.IntField()
    accomodation_name = fields.CharField(max_length=255)
    holiday_start_date = fields.DateField()
    holiday_end_date = fields.DateField()
    age = fields.IntField()
    date_of_birth = fields.DateField()
    country_of_issue = fields.CharField(max_length=255)
    document_type = fields.CharField(max_length=255)
    foid_number = fields.CharField(max_length=255)
    foid_issue = fields.DatetimeField()
    foid_expiry = fields.DatetimeField()
    nationality = fields.CharField(max_length=255)
    villa_id = fields.ForeignKeyField('models.Villa', related_name='passenger_informations', null=True)
    apis_report_file = fields.ForeignKeyField('models.APISReportFile', related_name='passenger_informations', null=True) 