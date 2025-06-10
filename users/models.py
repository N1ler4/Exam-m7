from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    birthday = models.DateField(null=True, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    scentific_degree = models.CharField(max_length=255, blank=True)
    another_info = models.TextField(blank=True)
    image = models.ImageField(upload_to='image/', null=True, blank=True)

