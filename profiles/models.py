from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER = [
        ('n', 'na'),
        ('m', 'man'),
        ('w', 'woman'),
        ('u', 'unknown'),
    ]

    nick = models.CharField(max_length=24)
    birthday = models.DateField()
    note = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER, default=GENDER[0][0])
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'{}\'s profile'.format(self.user.username)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['nick', 'birthday', 'note', 'gender', 'user']
