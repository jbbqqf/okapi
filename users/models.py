from django.db import models
from django.forms import ModelForm, PasswordInput

from passlib.hash import mysql41

class User(models.Model):
    login = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    profile_id = models.IntegerField(unique=True)
    locked = models.BooleanField(default=False)

    def __unicode__(self):
        return self.login

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['login', 'password', 'profile_id', 'locked']
        widgets = {
            'password': PasswordInput(),
        }

#     def clean_password(self):
#         password = mysql41.encrypt(self.cleaned_data['password'])
#         password = mysql41.encrypt('azerty123')
#         password = "lol"
#         return password
