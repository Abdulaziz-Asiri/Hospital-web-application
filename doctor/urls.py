from django.urls import path
from . import views

app_name = "doctor"

urlpatterns = [
    path("allDoctors/", views.all_doctors_view, name="all_doctors_view"),
    path("addDoctors/", views.add_doctors_view, name="add_doctors_view"),
]