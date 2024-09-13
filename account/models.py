from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age =  models.IntegerField()
    hight = models.DecimalField(max_digits=5, decimal_places=2)
    wight = models.DecimalField(max_digits=5, decimal_places=2)
    phone = models.CharField(blank=True)
    avatar = models.ImageField(upload_to="images/avatars/", default="images/defaultAvatar.png")


    def __str__(self) -> str:
        return self.first_name