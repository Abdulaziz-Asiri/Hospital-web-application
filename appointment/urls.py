from django.urls import path
from . import views

app_name = "appointment"
urlpatterns = [
    path("allAppointment/", views.all_appointment_view, name="all_appointment_view"),
    path("addAppointment/", views.add_appointment_view, name="add_appointment_view"),
    path("myAppointment/<user_username>", views.my_appointment_view, name="my_appointment_view"),
    path("deleteAppointment/<appointment_id>", views.delete_appointment_view, name="delete_appointment_view"),
]