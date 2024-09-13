from django.urls import path
from . import views

app_name = "clinic"

urlpatterns = [
    path("allClinics/", views.all_clinics_view, name="all_clinics_view"),
    path("addClinics/", views.add_clinics_view, name="add_clinics_view"),
    path("clinicDetail/<clinic_id>", views.details_clinics_view, name="details_clinics_view"),
]