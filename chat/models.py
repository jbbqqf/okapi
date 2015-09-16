from django.db import models
from django.forms import ModelForm

from users.models import User

class Post(models.Model):
    TYPE = [
        ('m', 'message'),
        ('s', 'score'),
    ]

    date = models.DateTimeField()
    author = models.ForeignKey(User)
    type = models.CharField(max_length=1, choices=TYPE, default=TYPE[0][0])
    content = models.CharField(max_length=512)

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['date', 'author', 'type', 'content']
