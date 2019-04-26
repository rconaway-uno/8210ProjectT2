from django.conf.urls import url
from . import views
from django.urls import path, re_path, reverse

app_name = 'patients'

urlpatterns = [
    
    #Patient URLs
    path('patient_list', views.patient_list, name='patient_list'),
    path('patient/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('patient/create/', views.patient_new, name='patient_new'),
    path('patient/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('search/', views.patient_search, name='patient_search'),
    path('search_list/', views.patient_search_list, name='patient_search_list'),

    #Triage URLs
    #path('triage/<int:pk>/triage_list', views.triage_list, name='triage_list'),
    #path('triage/<int:pk>/triage_edit', views.triage_edit, name='triage_edit'),
    #path('triage/<int:pk>/delete/', views.triage_delete, name='triage_delete'),
    #path('triage/create/', views.triage_new, name='triage_new'),
   
    #Injury URLs
    path('injury/<int:pk>/injury_list', views.injury_list, name='injury_list'),
    path('injury/<int:pk>/injury_edit', views.injury_edit, name='injury_edit'),
    path('injury/create/', views.injury_new, name='injury_new'),
    path('injury/<int:pk>/delete/', views.injury_delete, name='injury_delete'),

    #Disposition URLs
    path('disposition/<int:pk>/disposition_list', views.disposition_list, name='disposition_list'),
    path('disposition/create/', views.disposition_new, name='disposition_new'),
    path('disposition/<int:pk>/delete/', views.disposition_delete, name='disposition_delete'),
    path('disposition/<int:pk>/disposition_edit', views.disposition_edit, name='disposition_edit'),

]
