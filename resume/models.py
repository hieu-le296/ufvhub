from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Resume(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    street = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    province = models.CharField(max_length=4, blank=True, null=True)
    postal = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=200)
    summary = models.TextField(max_length=2000)
    degree = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    previous_work = models.TextField(max_length=1000)
    skills = models.TextField(max_length=1000)
