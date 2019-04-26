from .models import *
from .forms import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from events.views import getActiveEvent
from events.models import Organization, Nurse
from patients.forms import forms as patient_forms
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.
def patient_list(request):
    # ensure there is an acti99*ve event
    event = getActiveEvent()
    event_id = event.first().id
    if event_id:
       print('Event: ' + str(event_id))
       current_user = request.user.id
       curr_username = request.user
       print('current_user_id: ' + str(current_user))
       print('current_user: ' + str(curr_username))
       user = User.objects.filter(id=current_user)
       if user:
           print('user: ' + str(user))
           nurse = Nurse.objects.filter(user_id=current_user).first()
           if nurse:
               org_id = nurse.org.id
               if org_id:
                   print('Found org: ' + str(org_id))
                   patients=Patient.objects.filter(organization=org_id).filter(event=event_id)
                   for patient in patients:
                       print('Patient: ' + chr(patient.id))                   
                   return render(request, 'patients/patient_list.html',
                                 {'patients': patients})
               else:
                   patients = Patient.object.none()
                   return render(request, 'events/nurse_home.html')
           else:
               patients = Patient.object.none()
               return render(request, 'events/nurse_home.html')
       else:
           patients = Patient.object.none()
           return render(request, 'events/nurse_home.html')
    else:
        patients = Patient.object.none()
        #   patients = Patient.objects.filter(created_date__lte=timezone.now())
        return render(request, 'events/nurse_home.html')

def patient_new(request):
   if request.method == "POST":
       event = getActiveEvent()
       event_id = event.first().id
       # ensure there is an active event
       if event:
           print('Event: ' + str(event))
           current_user = request.user.id
           curr_username = request.user
           print('current_user_id: ' + str(current_user))
           print('current_user: ' + str(curr_username))
           user = User.objects.filter(id=current_user)
           if user:
               print('user: ' + str(user))
               nurse = Nurse.objects.filter(user_id=current_user).first()
               if nurse:
                   org_id = nurse.org.id
                   if org_id:
                       print('Found org: ' + str(org_id))
                   form = PatientForm(request.POST)
                   if form.is_valid():
                       patient = form.save(commit=False)
                       patient.organization_id = org_id
                       patient.event_id = event_id
                       patient.created_date = timezone.now()
                       patient.save()
                       patients = Patient.objects.filter(created_date__lte=timezone.now())
                       return render(request, 'patients/patient_list.html',
                                     {'patients': patients})
   else:
       form = PatientForm()
       # print("Else")
   return render(request, 'patients/patient_new.html', {'form': form})

def patient_edit(request, pk):
   patient = get_object_or_404(Patient, pk=pk)
   if request.method == "POST":
       # update
       form = PatientForm(request.POST, instance=patient)
       if form.is_valid():
           patient = form.save(commit=False)
           patient.updated_date = timezone.now()
           patient.save()
           patient = Patient.objects.filter(created_date__lte=timezone.now())
           return render(request, 'patients/patient_list.html',
                         {'patients': patient})
   else:
        # edit
       form = PatientForm(instance=patient)
   return render(request, 'patients/patient_edit.html', {'form': form})

def patient_delete(request, pk):
   patient = get_object_or_404(Patient, pk=pk)
   patient.delete()
   return redirect('patients:patient_list')

'''
#Patient Summary

#Triage
def triage_list(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    triage = PatientTriage.objects.filter(patient=patient.pk)
    return render(request, 'patients/triage_list.html',
                 {'triages': triage})

def triage_new(request):
   if request.method == "POST":
       form = PatientTriageForm(request.POST)
       if form.is_valid():
           triage = form.save(commit=False)
           triage.created_date = timezone.now()
           triage.save()
           triages = PatientTriage.objects.filter(created_date__lte=timezone.now())
           return render(request, 'patients/triage_list.html',
                         {'triages': triage})
   else:
       form = PatientTriageForm()
       # print("Else")
   return render(request, 'patients/triage_new.html', {'form': form})

def triage_edit(request, pk):
   triage = get_object_or_404(PatientTriage, pk=pk)
   if request.method == "POST":
       # update
       form = PatientTriageForm(request.POST, instance=triage)
       if form.is_valid():
           triage = form.save(commit=False)
           triage.updated_date = timezone.now()
           triage.save()
           triage = PatientTriage.objects.filter(created_date__lte=timezone.now())
           return render(request, 'patients/triage_list.html',
                         {'triages': triage})
   else:
        # edit
       form = PatientTriageForm(instance=triage)
   return render(request, 'patients/triage_edit.html', {'form': form})

def triage_delete(request, pk):
   triage = get_object_or_404(PatientTriage, pk=pk)
   triage.delete()
   return redirect('patients:patient_list')
'''

#injury
def injury_list(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    injury = Injury.objects.filter(patient=patient.pk)
    return render(request, 'patients/injury_list.html',
                 {'injuries': injury})

def injury_new(request):
   if request.method == "POST":
       form = InjuryForm(request.POST)
       if form.is_valid():
           injury = form.save(commit=False)
           injury.created_date = timezone.now()
           injury.save()
           patient = Patient.objects.filter(id=injury.patient.id).first()
           injuries = Injury.objects.filter(patient=patient)
           return render(request, 'patients/injury_list.html',
                         {'injuries': injuries})
   else:
       form = InjuryForm()
       # print("Else")
   return render(request, 'patients/injury_new.html', {'form': form})

def injury_edit(request, pk):
   injury = get_object_or_404(Injury, pk=pk)
   if request.method == "POST":
       # update
       form = InjuryForm(request.POST, instance=injury)
       if form.is_valid():
           injury = form.save(commit=False)
           patient=Patient.objects.filter(id=injury.patient.id).first()
           injury.updated_date = timezone.now()
           injury.save()
           injury = Injury.objects.filter(patient=patient)
           return render(request, 'patients/injury_list.html',
                         {'injuries': injury})
   else:
        # edit
       form = InjuryForm(instance=injury)
   return render(request, 'patients/injury_edit.html', {'form': form})

def injury_delete(request, pk):
    injury = get_object_or_404(Injury, pk=pk)
    patient = Patient.objects.filter(id=injury.patient.id).first()
    injury.delete()
    injuries = Injury.objects.filter(patient=patient)
    return render(request, 'patients/injury_list.html',
                  {'injuries': injuries})

#disposition list
def disposition_list(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    disposition = Disposition.objects.filter(patient=patient.pk)
    return render(request, 'patients/disposition_list.html',
                 {'dispositions': disposition})

def disposition_new(request):
   if request.method == "POST":
       form = DispositionForm(request.POST)
       if form.is_valid():
           disposition = form.save(commit=False)
           disposition.created_date = timezone.now()
           disposition.save()
           patient = Patient.objects.filter(id=disposition.patient.id).first()
           disposition = Disposition.objects.filter(patient=patient)
           return render(request, 'patients/disposition_list.html',
                         {'dispositions': disposition})
   else:
       form = DispositionForm
       # print("Else")
   return render(request, 'patients/disposition_new.html', {'form': form})

def disposition_delete(request, pk):
   disposition = get_object_or_404(Disposition, pk=pk)
   disposition.delete()
   return redirect('patients:patient_list')

def disposition_edit(request, pk):
   disposition = get_object_or_404(Disposition, pk=pk)
   if request.method == "POST":
       # update
       form = DispositionForm(request.POST, instance=disposition)
       if form.is_valid():
           disposition = form.save(commit=False)
           patient = Patient.objects.filter(id=disposition.patient.id).first()
           disposition.updated_date = timezone.now()
           disposition.save()
           disposition = Disposition.objects.filter(patient=patient)
           return render(request, 'patients/disposition_list.html',
                         {'dispositions': disposition})
   else:
        # edit
       form = DispositionForm(instance=disposition)
   return render(request, 'patients/disposition_edit.html', {'form': form})
    
    
def patient_search(request):
    return render(request, 'patients/patient_search.html')


def patient_search_list(request):
    #if request.method == "GET":
    event = getActiveEvent()
    if event:
       event_id = event.first().id
       print('Event: ' + str(event_id))
       first_name = request.GET['first_name']
       last_name = request.GET['last_name']
       print('last_name: ' + last_name)
       if last_name:
           if first_name:
               patients=Patient.objects.filter(event=event_id ).filter(patient_last_name=last_name).filter(patient_first_name=first_name)
           else:
               patients = Patient.objects.filter(event=event_id).filter(patient_last_name=last_name)
       elif first_name:
           if last_name:
               patients = Patient.objects.filter(event=event_id).filter(patient_last_name=last_name).filter(patient_first_name=first_name)
           else:
               patients = Patient.objects.filter(event=event_id).filter(patient_first_name=first_name)
       else:
           patients = Patient.objects.none()
    else:
        patients = Patient.objects.all()
    return render(request, 'patients/patient_search_list.html',
                  {'patients': patients})
