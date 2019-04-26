from django.contrib import admin

from .models import Patient, PatientTriage, Injury, Disposition
from events.models import Organization, Event
from beds.models import Bed

# Register your models here.
class PatientTriageInline(admin.TabularInline):
    model = PatientTriage
    extra = 3

class InjuryInline(admin.TabularInline):
    model = Injury
    extra = 3

class DispositionInline(admin.TabularInline):
    model = Disposition
    extra = 3

class PatientList(admin.ModelAdmin):
    #inlines = (InjuryInline,)
    #inlines = (PatientTriageInline,)
    list_display=('organization', 'event', 'patient_last_name', 'patient_first_name', 'patient_middle_name', 'age', 'dob','gender', 'unique_characteristics', 'next_of_kin_name', 'next_of_kin_relation', 'next_of_kin_phone')
    list_filter=('organization', 'event', 'patient_last_name')
    search_fields=('patient_last_name', 'patient')
    #ordering=['patient_last_name']


'''
class PatientTriageList(admin.ModelAdmin):
    list_display=('patient', 'patient_last_name', 'patient_first_name', )
    list_filter=('patient')
    search_fields=('patint', 'patient_last_name', 'patient_first_name')
    ordering=['patient_last_name']
'''

class InjuryList(admin.ModelAdmin):
    list_display=('patient', 'injury_type', 'creation_date')
    list_filter=('patient', 'injury_type')
    search_fields=('patient', 'injury_type')
    ordering=['patient_last_name']

class DispositionList(admin.ModelAdmin):
    list_display=('patient', 'disposition_type', 'description', 'transfer_to_org', 'time_of_death', 'updated_condition')
    list_filter=()
    search_fields=('disposition_type', 'transfer_to_org')
    ordering=['patient', 'disposition_type']


admin.site.register(Patient)
#admin.site.register(PatientTriage)
admin.site.register(Injury)
admin.site.register(Disposition)

