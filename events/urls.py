from . import views
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path, reverse
from django.contrib.auth import views as auth_views
from beds import urls
from patients import urls


app_name = 'events'

urlpatterns = [

    #Site home pages
    path('', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),

    #Login pages
    url(r'^admin_login/', views.admin_home, name='adminlogin'),
    url(r'^nurse_login/', views.nurse_home, name='nurselogin'),

    #Speecific Admin/User Home Pages
    path('admin_home', views.admin_home, name='admin_home'),
    path('nurse_home', views.nurse_home, name='nurse_home'),

    #change password urls
    path('accounts/password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('accounts/password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('password_reset/',	auth_views.PasswordResetView.as_view(),	name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),	name='password_reset_done'),
    path('reset/<uidb64>/<token>/',	auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',	auth_views.PasswordResetCompleteView.as_view(),	name='password_reset_complete'),

    # Other app url links
    path('patients/', include('patients.urls')),
    path('beds/', include('beds.urls')),

    #Admin usert type selection
    path('admin/user_option', views.user_option, name='user_option'),

    #list pages
    path('admin/users_list', views.users_list, name='users_list'),
    path('admin/nurse_list', views.nurse_list, name='nurse_list'),
    path('event_list', views.event_list, name='event_list'),
    path('org_list', views.org_list, name='org_list'),

    #edit  pages
    path('user/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('nurse/<int:pk>/edit/', views.nurse_edit, name='nurse_edit'),
    path('event/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('event/end_curr', views.end_curr_event, name='end_curr_event'),
    path('nurse/force_nurse_pw_reset/', views.force_nurse_pw_reset, name='force_nurse_pw_reset'),
    path('org/<int:pk>/edit/', views.org_edit, name='org_edit'),

    #create pages
    path('user/create/', views.user_new, name='user_new'),
    path('event/create/', views.event_new, name='event_new'),
    path('event/create/notify', views.event_new_notify, name='event_new_notify'),
    path('org/create/', views.org_new, name='org_new'),

    #delete pages
    path('user/<username>/delete/', views.user_delete, name='user_delete'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('org_summary_pdf', views.org_summary_pdf, name='org_summary_pdf'),
    path('nurse_summary_pdf', views.nurse_summary_pdf, name='nurse_summary_pdf'),

]

