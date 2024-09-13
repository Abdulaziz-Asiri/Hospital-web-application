from django.contrib import admin
from .models import  Appointment


class AppointmentAdmin(admin.ModelAdmin):

    list_display = ("user", "doctor", "clinic","date","time_slot","created_at")


admin.site.register(Appointment,AppointmentAdmin)