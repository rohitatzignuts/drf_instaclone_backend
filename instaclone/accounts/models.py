from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
