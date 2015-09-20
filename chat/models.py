from django.db import models
from django.forms import ModelForm

from django.contrib.auth.models import User

class Post(models.Model):
    TYPE = [
        ('m', 'message'),
        ('s', 'score'),
    ]

    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    type = models.CharField(max_length=1, choices=TYPE, default=TYPE[0][0])
    content = models.CharField(max_length=512)

    def __unicode__(self):
        return u'{}: {}'.format(self.author, self.content)

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'type', 'content']
