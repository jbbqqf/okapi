from django.db import models
from django.forms import ModelForm, CharField, Textarea
from django.contrib.auth.models import User

class Event(models.Model):
    author = models.ForeignKey(User)

    title = models.CharField(max_length=32)
    description = models.TextField(null=True)
    link = models.CharField(max_length=255, null=True)

    created = models.DateTimeField(auto_now_add=True)
    dday = models.DateField()

    visible = models.BooleanField(default=True)
    
    def __unicode__(self):
        return '{} on {}'.format(self.title, self.dday)

class EventForm(ModelForm):
    description = CharField(required=False, widget=Textarea)
    link = CharField(max_length=255, required=False)

    class Meta:
        model = Event
        fields = ['author', 'title', 'description', 'link', 'dday',]
