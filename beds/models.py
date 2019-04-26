from django.utils import timezone
from django.contrib import admin
from django.db import models
from django import forms
from events.models import Event, Organization


class Bed(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    bed_type = models.CharField(max_length=50, blank=True)
    initial_num = models.IntegerField(blank=True, null=True)
    num_used = models.IntegerField(blank=True, null=True)
    num_available = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.bed_type + ' | ' + self.organization.org_name)

