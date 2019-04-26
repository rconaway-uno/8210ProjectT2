from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .utils import render_to_pdf
from django.template.loader import get_template
from events import views as event_views
from events import models as event_models
from patients import models as patient_models
from django.contrib.auth.models import User

def bed_list(request):
    event = event_views.getActiveEvent()
    event_id = event.first().id
    if event_id:
        print('Event: ' + str(event_id))
        user = request.user
        if user.is_authenticated:
            if user.is_superuser:
                bed = Bed.objects.filter(event=event_id)
                return render(request, 'beds/bed_list.html',
                              {'beds': bed})
            else:
                current_user = request.user.id
                curr_username = request.user
                print('current_user_id: ' + str(current_user))
                print('current_user: ' + str(curr_username))
                user = User.objects.filter(id=current_user)
                if user:
                    print('user: ' + str(user))
                    nurse = event_models.Nurse.objects.filter(user_id=current_user).first()
                    if nurse:
                        org_id = nurse.org.id
                        if org_id:
                            print('Found org: ' + str(org_id))
                            bed = Bed.objects.filter(organization=org_id).filter(event=event_id)
                            return render(request, 'beds/bed_list.html',
                                         {'beds': bed})
        else:
            bed = Bed.objects.filter(event=event_id)
            return render(request, 'beds/bed_list.html',
                          {'beds': bed})

def bed_availability(request):
    event = event_views.getActiveEvent()
    event_id = event.first().id
    if event_id:
        print('Event: ' + str(event))
        beds = Bed.objects.filter(event_id=event_id).order_by('organization_id')
        return render(request, 'beds/bed_availability.html', {'beds': beds})

def bed_new(request):
   if request.method == "POST":
       form = BedForm(request.POST)
       if form.is_valid():
           bed = form.save(commit=False)
           activeEvent = event_views.getActiveEvent()
           event_id = activeEvent[0].pk
           print(activeEvent[0].pk)
           current_user = request.user.id
           curr_username = request.user
           print('current_user_id: ' + str(current_user))
           print('current_user: ' + str(curr_username))
           user = User.objects.filter(id=current_user)
           if user:
               print('user: ' + str(user))
               nurse = event_models.Nurse.objects.filter(user_id=current_user).first()
               if nurse:
                   org_id = nurse.org.id
                   if org_id:
                       print('Found org: ' + str(org_id))
                       bed.event_id = activeEvent[0].pk
                       bed.organization_id = org_id
                       bed.num_available = bed.initial_num - bed.num_used
                       bed.created_date = timezone.now()
                       bed.save()
                       beds = Bed.objects.filter(organization=org_id).filter(event=event_id)
                       return render(request, 'beds/bed_list.html',
                                     {'beds': beds})
   else:
       form = BedForm()
       # print("Else")
   return render(request, 'beds/bed_new.html', {'form': form})

def bed_edit(request, pk):
   bed = get_object_or_404(Bed, pk=pk)
   if request.method == "POST":
       # update
       form = BedForm(request.POST, instance=bed)
       if form.is_valid():
           bed = form.save(commit=False)
           bed.num_available = bed.initial_num - bed.num_used
           bed.updated_date = timezone.now()
           bed.save()
           activeEvent = event_views.getActiveEvent()
           event_id = activeEvent[0].pk
           print(activeEvent[0].pk)
           current_user = request.user.id
           curr_username = request.user
           print('current_user_id: ' + str(current_user))
           print('current_user: ' + str(curr_username))
           nurse = event_models.Nurse.objects.filter(user_id=current_user).first()
           if nurse:
               org_id = nurse.org.id
               if org_id:
                   print('Found org: ' + str(org_id))
                   beds = Bed.objects.filter(organization=org_id).filter(event=event_id)
                   return render(request, 'beds/bed_list.html',
                                 {'beds': beds})

   else:
       # edit
       form = BedForm(instance=bed)
       return render(request, 'beds/bed_edit.html', {'form': form})

def bed_delete(request, pk):
   bed = get_object_or_404(Bed, pk=pk)
   bed.delete()
   return redirect('beds:bed_list')

@login_required
def bed_summary_pdf(request):
	beds = Bed.objects.order_by('organization_id')
	context = {'beds': beds,}
	template = get_template('beds/bed_summary_pdf.html')
	html = template.render(context)
	pdf = render_to_pdf('beds/bed_summary_pdf.html', context)

	return pdf


