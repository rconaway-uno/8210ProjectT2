from django.contrib.auth.models import User, AbstractBaseUser
from django.utils import timezone
from django.db import models

class Organization(models.Model):
    org_type = models.CharField(max_length=25, blank=True)
    org_name = models.CharField(max_length=250, blank=True)
    org_addr1 = models.CharField(max_length=250, blank=True, null=True)
    org_addr2 = models.CharField(max_length=250, blank=True, null=True)
    org_city = models.CharField(max_length=150, blank=True, null=True)
    org_state = models.CharField(max_length=5, blank=True, null=True)
    org_zip = models.CharField(max_length=10, blank=True, null=True)
    org_primary_phone = models.CharField(max_length=25, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.org_name)

class Nurse(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return self.user.username


# Create your models here.
class Event(models.Model):
    event_type = models.CharField(max_length=25, blank=True)
    event_description = models.CharField(max_length=250, blank=True)
    event_start_date = models.DateTimeField(blank=True, default=timezone.now)
    event_end_date = models.DateTimeField(blank=True, null=True)
    simulation_flag = models.BooleanField(blank=True, default=False)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.event_description)
