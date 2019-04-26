from django.db import models
from django.utils import timezone
from events.models import Event, Organization

# Create your models here.
class Patient(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    patient_last_name = models.CharField(max_length=150, blank=True)
    patient_first_name = models.CharField(max_length=150, blank=True)
    patient_middle_name = models.CharField(max_length=150, blank=True)
    age = models.IntegerField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=5,blank=True)
    unique_characteristics = models.CharField(max_length=1000,blank=True)
    next_of_kin_name = models.CharField(max_length=250,blank=True)
    next_of_kin_relation = models.CharField(max_length=150, blank=True)
    next_of_kin_phone = models.CharField(max_length=25, blank=True)
    triage_tag_num = models.CharField(max_length=50, blank=True)
    tag_color_condition = models.CharField(max_length=25, blank=True)
    mode_of_arrival = models.CharField(max_length=25, blank=True)
    arrival_date = models.DateTimeField(blank=True, null=True)
    arrival_condition = models.CharField(max_length=50, blank=True)
    room_number = models.CharField(max_length=25, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.patient_first_name + ' ' + self.patient_last_name)


class PatientTriage(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    triage_tag_num = models.CharField(max_length=50, blank=True)
    tag_color_condition = models.CharField(max_length=25, blank=True)
    mode_of_arrival = models.CharField(max_length=25, blank=True)
    arrival_date = models.DateTimeField(blank=True, null=True)
    arrival_condition = models.CharField(max_length=50, blank=True)
    room_number = models.CharField(max_length=25, blank=True)
    created_date = models.DateTimeField(default=timezone.now)


    def created(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return (self.triage_tag_num)


class Injury(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    injury_type = models.CharField(max_length=50, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return (self.patient.patient_first_name + ' ' + self.patient.patient_last_name + '-' + self.injury_type)


class Disposition(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disposition_type = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=500, blank=True)
    transfer_to_org = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
    time_of_death = models.DateTimeField(blank=True, null=True)
    updated_condition = models.CharField(max_length=25, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return (self.patient.patient_first_name + ' ' + self.patient.patient_last_name + '-' + self.disposition_type)

