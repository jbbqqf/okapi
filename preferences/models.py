from django.db import models
from django.forms import ModelForm
from django.db import IntegrityError

from django.contrib.auth.models import User

class UserInterface(models.Model):
    """
    The Open KAribou API is supposed to be exploited by different UIs. Since
    each UI will have its own set of themes, themes need to refer to a specific
    UI to be usable.
    """

    name = models.CharField(max_length=24)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class UserInterfaceForm(ModelForm):
    class Meta:
        model = UserInterface
        fields = ['name', 'comment',]

class UserPref(models.Model):
    """
    A many to many relationship model to record theme user preferences.
    """

    user = models.ForeignKey(User)
    ui = models.ForeignKey(UserInterface)
    conf = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'ui',)

class UserPrefForm(ModelForm):
    class Meta:
        model = UserPref
        fields = ['user', 'ui', 'conf',]
