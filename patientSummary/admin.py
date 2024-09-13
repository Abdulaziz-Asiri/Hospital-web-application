from django.contrib import admin
from .models import PatientSummary

class PatientAdmin(admin.ModelAdmin):

    list_display = ("appointment", "diagnosis", "prescription_name","created_at")


admin.site.register(PatientSummary,PatientAdmin)