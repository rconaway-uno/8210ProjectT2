from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, re_path, reverse
from django.contrib.auth.views import LoginView, LogoutView
from events import urls, views as event_views
from beds import urls
from patients import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    re_path(r'^accounts/login/$', LoginView.as_view(template_name='registration/login.html'), name="login"),
    re_path(r'^accounts/logout/$', LogoutView.as_view(), LogoutView.next_page, name="logout"),
    path('patients/', include('patients.urls')),
    path('beds/', include('beds.urls')),
    path('', event_views.home, name='home'),
    url(r'^home/$', event_views.home, name='home'),
    path('', include('django.contrib.auth.urls'))

]
