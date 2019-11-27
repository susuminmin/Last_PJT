from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

    
# AbstractUser 상속
class User(AbstractUser):
    pass