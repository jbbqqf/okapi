from django.db import models
from django.forms import ModelForm, PasswordInput

from passlib.hash import mysql41

class Profile(models.Model):
    GENDER = [
        ('n', 'na'),
        ('m', 'man'),
        ('w', 'woman'),
        ('u', 'unknown'),
    ]

    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    surname = models.CharField(max_length=24)
    birthday = models.DateField()
    note = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER, default=GENDER[0][0])

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'surname', 'birthday', 'note', 'gender']

class User(models.Model):
    login = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    profile = models.ForeignKey(Profile)
    locked = models.BooleanField(default=False)

    def __unicode__(self):
        return self.login

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['login', 'password', 'profile', 'locked']
        widgets = {
            'password': PasswordInput(),
        }

#     def clean_password(self):
#         password = mysql41.encrypt(self.cleaned_data['password'])
#         password = mysql41.encrypt('azerty123')
#         password = "lol"
#         return password
