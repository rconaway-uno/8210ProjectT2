from django import forms
from .models import *

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('patient_last_name', 'patient_first_name', 'patient_middle_name', 'age', 'dob', 'gender', 'unique_characteristics', 'next_of_kin_name', 'next_of_kin_relation', 'next_of_kin_phone', 'triage_tag_num', 'tag_color_condition', 'mode_of_arrival', 'arrival_date', 'arrival_condition', 'room_number', 'created_date')

class PatientTriageForm(forms.ModelForm):
    class Meta:
        model = PatientTriage
        fields = ('patient', 'triage_tag_num', 'tag_color_condition', 'mode_of_arrival', 'arrival_date', 'arrival_condition', 'room_number')

class InjuryForm(forms.ModelForm):
    class Meta:
        model = Injury
        fields = ('patient', 'injury_type', 'created_date')

class DispositionForm(forms.ModelForm):
    class Meta:
        model = Disposition
        fields = ('patient', 'disposition_type', 'description', 'transfer_to_org', 'time_of_death', 'updated_condition', 'created_date')