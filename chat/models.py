from django.db import models
from django.forms import ModelForm

from django.contrib.auth.models import User

class Post(models.Model):
    """
    Basically the only thing you need for a chat application.

    Connected users should be able to send `m` posts from the user interface.
    For any other kind of post that could be displayed to users, only backend
    through application requests should be allowed create those.
    """

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
