from django.db import models
from doctor.models import Doctor


class Clinic(models.Model):
    class WorkingHours(models.TextChoices):
        SunThu = 'SunThu', "Sunday - Thursday"
        All = "All", "All Week"
        MonFri = "MonFri", "Monday - Friday"

    name= models.CharField(max_length=255)
    description= models.TextField()
    working_hours= models.CharField(max_length=50, choices=WorkingHours.choices, default=WorkingHours.SunThu)
    feature_image=models.ImageField(upload_to="images/", default="images/default.jpg")
    doctors_id = models.ManyToManyField(Doctor, related_name='doctor')

    def __str__(self) -> str:
        return self.name