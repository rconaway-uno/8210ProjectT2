from django.contrib import admin

from .models import Bed
from events.models import Organization, Event

# Register your models here.
class BedList(admin.ModelAdmin):
    list_display=('event', 'organization', 'bed_type', 'initial_num', 'num_used', 'num_available')
    list_filter=('event', 'organization', 'bed_type')
    ordering=['bed_type', 'num_available', 'organization' ]

admin.site.register(Bed)