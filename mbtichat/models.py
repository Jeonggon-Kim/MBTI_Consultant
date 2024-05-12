from django.db import models
from django.conf import settings



# class User(AbstractUser):  
#   nickname = models.CharField(max_length=10)


# Create your models here.
class Chat(models.Model) :
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  prompt = models.TextField()
  response = models.TextField()