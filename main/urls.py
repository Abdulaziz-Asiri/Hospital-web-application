from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("dashboard/", views.dashboard_view, name="dashboard_view"),
    path("clinic_details/<clinic_id>", views.details_clinics, name="details_clinics"),
    path("make/appointment/<int:clinic_id>/<int:profile_id>/", views.make_appointment, name="make_appointment"),
]