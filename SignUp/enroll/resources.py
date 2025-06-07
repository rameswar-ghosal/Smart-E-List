from import_export import resources
from .models import Scheduled

class ScheduledResource(resources.ModelResource):
    class Meta:
        model = Scheduled
        fields=('schedule_items','schedule_date','schedule_time',)