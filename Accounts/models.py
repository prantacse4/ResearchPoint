from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, unique=True)
    bio = models.TextField(null=True)
    institution = models.CharField(null=True, max_length=255,)
    is_user  = models.BooleanField(default=False, blank=True, null=True)
    is_researcher  = models.BooleanField(default=False, blank=True, null=True)
    avatar = models.ImageField(upload_to='upload', null=True, default="avatar.svg")
    
    REQUIRED_FIELDS = []