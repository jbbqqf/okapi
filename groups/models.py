from django.db import models
from django.forms import ModelForm

class Group(models.Model):
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    mailing = models.CharField(max_length=100)
    description = models.TextField()
    parent_id = models.IntegerField()

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'url', 'mailing', 'description', 'parent_id']
