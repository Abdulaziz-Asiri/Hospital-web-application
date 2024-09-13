from django.db import models
from appointment.models import Appointment


class PatientSummary(models.Model):
    appointment= models.ForeignKey(Appointment, on_delete=models.CASCADE ,related_name='appointment')
    diagnosis= models.TextField()
    prescription_name= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f"{self.appointment.user} in Clinic ({self.diagnosis}) with Doctor {self.prescription_name} date{self.created_at} "