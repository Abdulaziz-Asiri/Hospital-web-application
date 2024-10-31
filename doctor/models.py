from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    specialization =models.CharField(max_length=255)
    about = models.TextField(blank=True)
    email = models.EmailField(max_length=100,blank=True)
    phone = models.CharField(max_length=100,blank=True )
    image = models.ImageField(upload_to="images/avatars/", default="images/defaultAvatar.png")

    def __str__(self) -> str:
        return self.name