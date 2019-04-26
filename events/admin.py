from django.contrib import admin

from .models import Organization, Event, Nurse

# Register your models here.
class OrgList(admin.ModelAdmin):
    list_display = ('org_id', 'org_name', 'org_type', 'org_addr1', 'org_addr2', 'org_city', 'org_state', 'org_zip', 'org_primary_phone')
    list_filter = ('org_name', 'org_type', 'org_zip')
    ordering=['org_name']

class EventList(admin.ModelAdmin):
    list_display=('event_id', 'event_type', 'event_description', 'event_start_date', 'event_end_date', 'simulation_flag')
    list_filter=('event_id', 'event_type', 'event_start_date', 'simulation_flag')
    ordering=['event_id']

class NurseList(admin.ModelAdmin):
    list_display=('user', 'org_name', 'title', 'phone')
    list_filter=('org_name')
    ordering=['org_name']

admin.site.register(Organization)
admin.site.register(Event)
admin.site.register(Nurse)

