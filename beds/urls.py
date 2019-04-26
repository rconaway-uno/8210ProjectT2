from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'beds'

urlpatterns = [
        path('bed_list', views.bed_list, name='bed_list'),
        path('bed/create/', views.bed_new, name='bed_new'),
        path('bed/<int:pk>/edit/', views.bed_edit, name='bed_edit'),
        path('bed/<int:pk>/delete/', views.bed_delete, name='bed_delete'),
	    path('bed_availability',views.bed_availability, name='bed_availability'),
	    path('home/bed_availability',views.bed_availability, name='bed_availability'),
        path('bed_summary_pdf', views.bed_summary_pdf, name='bed_summary_pdf'),
]


