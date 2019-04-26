
from .models import *
from django import forms
from django.contrib.auth.models import User


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

class NurseEditForm(forms.ModelForm):
    class Meta:
        model = Nurse
        fields = ('user','org', 'title', 'phone', 'end_date')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_type', 'event_description', 'event_start_date', 'event_end_date', 'simulation_flag')

class OrgEditForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('org_type', 'org_name', 'org_addr1', 'org_addr2', 'org_city', 'org_state', 'org_zip', 'org_primary_phone')


