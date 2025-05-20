from tortoise import fields
from tortoise.models import Model

class ExtrasFilteredReservationOutput(Model):
    id = fields.IntField(pk=True)
    resort_report_file = fields.ForeignKeyField('models.ResortReportFile', related_name='extras_filtered_outputs')
    file_name = fields.CharField(max_length=255)
    generated_date = fields.DatetimeField()
    applied_filters = fields.JSONField(null=True)  # villa → list of extras used in filter
    grouped_reservations = fields.JSONField(null=True)  # villa → sorted reservations
    file_path = fields.CharField(max_length=512, null=True)
    created_at = fields.DatetimeField(auto_now_add=True) 