from django.db import models
from django.contrib.auth.models import AbstractUser
from home.utils import get_activation_code


class CustomUser(AbstractUser):
    gender = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=15)
    activate_code = models.PositiveIntegerField(default=get_activation_code())
    account_active = models.BooleanField(default=False)
    

