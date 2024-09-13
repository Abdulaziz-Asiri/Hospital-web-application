from django.db import models
from account.models import Profile
from doctor.models import Doctor
from clinic.models import Clinic


class Appointment(models.Model):

    user= models.ForeignKey(Profile, on_delete=models.CASCADE ,related_name='appointment')
    doctor= models.ForeignKey(Doctor, on_delete=models.CASCADE ,related_name='appointment')
    clinic= models.ForeignKey(Clinic, on_delete=models.CASCADE ,related_name='appointment')
    date= models.DateField(auto_now_add=False)
    time_slot= models.TimeField()
    created_at= models.DateField(auto_now_add=True)

    def __str__ (self):
        return f"{self.user.first_name} in Clinic ({self.clinic.name}) with Doctor {self.doctor.name} date{self.date} "