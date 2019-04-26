from .forms import *
from .models import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from .utils import render_to_pdf
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.db.models import Count
from django.contrib.auth.models import Group
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.http import HttpRequest


nurse_group = Group.objects.get(name='Nurse')

# Create your views here.

def getActiveEvent():
    activeEvent = Event.objects.filter(event_end_date__isnull=True)
    return activeEvent



def home(request):

    if getActiveEvent():
        return render(request, 'events/home.html',
                      {'events': home})
    else:
        return render(request, 'events/home_no_event.html',
                      {'events': home})

def adminlogin(request):

    if getActiveEvent():
        if request.user.is_staff:
            return redirect('events/nurse_home.html')
        else:
            return redirect('events/admin_home.html')
    else:
        return render(request, 'events/home_no_event.html',
                      {'events': home})

@permission_required('is_superuser')
def admin_home(request):

    if getActiveEvent():
        return render(request, 'events/admin_home.html',
                      {'admin': admin_home})
    else:
        return render(request, 'events/home_no_event.html',
                      {'events': home})


@permission_required('is_staff')
def admin_home(request):

    return render(request, 'events/admin_home.html',
                  {'chs': admin_home})

def admin_login(request):
        return render(request, 'events/admin_login.html', {'events': admin_login})

@login_required
def nurse_home(request):

    if getActiveEvent():
        return render(request, 'events/nurse_home.html',
                      {'nurse': nurse_home})
    else:
        return render(request, 'events/home_no_event.html',
                      {'events': home})


@login_required
def users_list(request):
    users = User.objects.all()
    #print(users)
    return render(request, 'events/users_list.html', {'users': users})

@login_required
def user_option(request):
    return render(request, 'events/user_option.html',
                 {'admin': user_option})

@login_required
def nurse_list(request):
    #users = User.objects.filter(groups=1)
    nurses = Nurse.objects.filter(end_date__isnull=True)
    return render(request, 'events/nurse_list.html',{'nurses': nurses})


@login_required
def nurse_edit(request, pk):
   user = User.objects.filter(pk=pk).first()
   org = Organization.objects.filter(org_name='Unassigned').first()
   if not org: #check to ensure Unassigned org exists and create if needed
       print("Unassigned org not Found - Creating it")
       # create new nurse thru form
       neworg = Organization.objects.create(org_type='Default',org_name='Unassigned', created_date = timezone.now(), updated_date = timezone.now())
       neworg.save()
       org = Organization.objects.filter(org_name='Unassigned').first()

   #print('USER ' + str(user.pk))
   #print('ORG ' + str(org.pk))
   nurse = Nurse.objects.filter(user_id=user.pk).first()

   if not nurse:
       print("Nurse not Found - Create New")
       # create new nurse thru form
       newNurse = Nurse.objects.create(user=user,org=org)
       newNurse.save()
       form = NurseEditForm(instance=newNurse)
       return render(request, 'events/nurse_edit.html', {'form': form})
   else: #nurse already exists
       print('Nurse ' + str(nurse.user))
       if request.method == "POST":
           # update
           form = NurseEditForm(request.POST, instance=nurse)
           if form.is_valid():
               nurse = form.save(commit=False)
               nurse.updated_date = timezone.now()
               nurse.save()
               nurses = Nurse.objects.all() #filter(end_date__isnull=True)
               return render(request, 'events/nurse_list.html',
                             {'nurses': nurses})
       else:
           # edit
           form = NurseEditForm(instance=nurse)
           return render(request, 'events/nurse_edit.html', {'form': form})

def split_domain_port(host):
    """
    Return a (domain, port) tuple from a given host.

    Returned domain is lowercased. If the host is invalid, the domain will be
    empty.
    """
    host = host.lower()

    if host[-1] == ']':
        # It's an IPv6 address without a port.
        return host, ''
    bits = host.rsplit(':', 1)
    domain, port = bits if len(bits) == 2 else (bits[0], '')
    # Remove a trailing dot (if present) from the domain.
    domain = domain[:-1] if domain.endswith('.') else domain
    if port=='': port = '80'
    return domain, port

def reset_user_pw(request, email):
    # ADD PW RESET CALL HERE
    baseurl = request.get_host()
    print('baseurl: ' + baseurl)
    domain, port = split_domain_port(baseurl)
    print('domain: ' + domain + ' port: ' + port)
    form = PasswordResetForm({'email': email})
    if form.is_valid():
        request = HttpRequest()
        request.META['SERVER_NAME'] = domain
        request.META['SERVER_PORT'] = port
        form.save(
            request=request,
            use_https=False,
            from_email="admin@dcehs.org",
            email_template_name='events/force_pw_reset_notify.html')
        

@login_required
def force_nurse_pw_reset(request):
    #users = User.objects.filter(groups=1)
    nurses = Nurse.objects.filter(end_date__isnull=True)
    for nurse in nurses.iterator():
        print('pk: ' + str(nurse.pk))
        user = get_object_or_404(User, pk=nurse.pk)
        print('email: ' + str(user.email))
        reset_user_pw(request, user.email)
    updated_nurses = Nurse.objects.filter(end_date__isnull=True)
    return render(request, 'events/nurse_list.html',{'nurses': updated_nurses})


@login_required
def user_edit(request, pk):
   user = get_object_or_404(User, pk=pk)
   if request.method == "POST":
       # update
       form = UserEditForm(request.POST, instance=user)
       if form.is_valid():
           user = form.save(commit=False)
           user.updated_date = timezone.now()
           user.save()
           users = User.objects.filter()
           #print(users)
           return render(request, 'events/users_list.html',
                         {'users': users})
   else:
        # edit
       form = UserEditForm(instance=user)
       return render(request, 'events/user_edit.html', {'form': form})

@login_required
def user_delete(request, username):
    users = User.objects.get(username=username)
    users.delete()
    return redirect('events:users_list')


def new_user_pw(request, email):
    # ADD PW RESET CALL HERE
    baseurl = request.get_host()
    print('baseurl: ' + baseurl)
    domain, port = split_domain_port(baseurl)
    print('domain: ' + domain + ' port: ' + port)
    form = PasswordResetForm({'email': email})
    if form.is_valid():
        request = HttpRequest()
        request.META['SERVER_NAME'] = domain
        request.META['SERVER_PORT'] = port
        form.save(
            request=request,
            use_https=False,
            from_email="admin@dcehs.org",
            email_template_name='events/user_new_notify.html')


@login_required
def user_new(request):
    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            newuser = form.save(commit=False)
            newuser.date_joined = timezone.now()
            #SET NEW USER PW
            pw = get_random_string()
            print('randPw: ' + pw)
            newuser.set_password(pw)
            #newuser.password1 = pw
            #newuser.password2 = pw
            newuser.save()
            nurse_group.user_set.add(newuser.pk)
            newuser.save()
            new_user_pw(request,newuser.email)
            # user = User.objects.filter(pk=newuser.pk)
            users = User.objects.filter(date_joined__lte=timezone.now())
            return render(request, 'events/users_list.html',
                          {'users': users})
    else:
        form = UserEditForm()
        # print("Else")
    return render(request, 'events/user_new.html', {'form': form})


def event_list(request):
    events = Event.objects.filter(created_date__lte=timezone.now())
    return render(request, 'events/event_list.html',
                 {'events': events})

def event_new(request):
   if request.method == "POST":
       form = EventForm(request.POST)
       if form.is_valid():
           #print("getting active event queryset")
           active_event = getActiveEvent()
           if active_event:
             #print("An Active event already exists - returning to events page")
             return render(request, 'events/event_new_error.html')
           else:
             event = form.save(commit=False)
             event.created_date = timezone.now()
             event.save()
             event_new_notify(request)
             events = Event.objects.filter(created_date__lte=timezone.now())
             return render(request, 'events/event_list.html',
                           {'events': events})
   else:
       form = EventForm()
       # print("Else")
       return render(request, 'events/event_new.html', {'form': form})


def send_new_event_notify(request, email):
    # ADD PW RESET CALL HERE
    baseurl = request.get_host()
    print('baseurl: ' + baseurl)
    domain, port = split_domain_port(baseurl)
    print('domain: ' + domain + ' port: ' + port)
    form = PasswordResetForm({'email': email})
    if form.is_valid():
        request = HttpRequest()
        request.META['SERVER_NAME'] = domain
        request.META['SERVER_PORT'] = port
        form.save(
            request=request,
            use_https=False,
            from_email="admin@dcehs.org",
            email_template_name='events/event_new_notify.html')

def event_new_notify(request):
    nurses = Nurse.objects.all() #filter(end_date__isnull=True)
    for nurse in nurses.iterator():
        print('pk: ' + str(nurse.pk))
        user = get_object_or_404(User, pk=nurse.pk)
        print('email: ' + str(user.email))
        send_new_event_notify(request, user.email)
    events = Event.objects.filter(created_date__lte=timezone.now())
    return render(request, 'events/event_list.html',
                  {'events': events})

def event_edit(request, pk):
   event = get_object_or_404(Event, pk=pk)
   if request.method == "POST":
       # update
       form = EventForm(request.POST, instance=event)
       if form.is_valid():
           event = form.save(commit=False)
           event.updated_date = timezone.now()
           event.save()
           events = Event.objects.filter(created_date__lte=timezone.now())
           return render(request, 'events/event_list.html',
                         {'events': events})
   else:
        # edit
       form = EventForm(instance=event)
   return render(request, 'events/event_edit.html', {'form': form})

def event_delete(request, pk):
   event = get_object_or_404(Event, pk=pk)
   event.delete()
   return redirect('events:event_list')


def end_curr_event(request):
   active_event = getActiveEvent()
   if active_event:
       active_event.update(event_end_date = timezone.now())
   events = Event.objects.filter(created_date__lte=timezone.now())
   return render(request, 'events/event_list.html',
                 {'events': events})


@login_required
def org_list(request):
    orgs = Organization.objects.filter(created_date__lte=timezone.now()).exclude(org_name='Unassigned')
    return render(request, 'events/org_list.html',
                  {'orgs': orgs})

@login_required
def org_new(request):
   if request.method == "POST":
       form = OrgEditForm(request.POST)
       if form.is_valid():
           neworg = form.save(commit=False)
           neworg.created_date = timezone.now()
           neworg.save()
           orgs = Organization.objects.filter(created_date__lte=timezone.now()).exclude(org_name='Unassigned')
           return render(request, 'events/org_list.html',
                         {'orgs': orgs})
   else:
       form = OrgEditForm()
       # print("Else")
   return render(request, 'events/org_new.html', {'form': form})

@login_required
def org_edit(request, pk):
   org = get_object_or_404(Organization, pk=pk)
   if request.method == "POST":
       # update
       form = OrgEditForm(request.POST, instance=org)
       if form.is_valid():
           org = form.save(commit=False)
           org.updated_date = timezone.now()
           org.save()
           orgs = Organization.objects.filter(created_date__lte=timezone.now()).exclude(org_name='Unassigned')
           #print(organization)
           return render(request, 'events/org_list.html',
                         {'orgs': orgs})
   else:
        # edit
       form = OrgEditForm(instance=org)
       return render(request, 'events/org_edit.html', {'form': form})

@login_required
def org_summary_pdf(request):
	orgs = Organization.objects.filter(created_date__lte=timezone.now()).exclude(org_name='Unassigned')
	context = {'orgs':orgs,}
	template = get_template('events/org_summary_pdf.html')
	html = template.render(context)
	pdf = render_to_pdf('events/org_summary_pdf.html', context)
	return pdf

@login_required
def nurse_summary_pdf(request):
	nurses = Nurse.objects.all()
	context = {'nurses': nurses}
	template = get_template('events/nurse_summary_pdf.html')
	html = template.render(context)
	pdf = render_to_pdf('events/nurse_summary_pdf.html', context)
	return pdf