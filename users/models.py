from django.db import models

class User(models.Model):
    login = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    profile_id = models.IntegerField(editable=False, unique=True)
    locked = models.BooleanField(default=False)
