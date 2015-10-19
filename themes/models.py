from django.db import models
from django.forms import ModelForm

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

class Theme(models.Model):
    """
    A theme instance just represents a user preference. UIs have to handle
    operations to render it.
    """

    ui = models.ForeignKey(UserInterface)
    name = models.CharField(max_length=24)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        return u'{}/{}'.format(self.ui, self.name)

class ThemeForm(ModelForm):
    class Meta:
        model = Theme
        fields = ['ui', 'name', 'comment',]

class UserTheme(models.Model):
    """
    A many to many relationship model to record theme user preferences.
    """

    user = models.ForeignKey(User)
    theme = models.ForeignKey(Theme)

    class Meta:
        unique_together = [('user', 'theme'),]

    def __unicode__(self):
        return u'{} has theme {}'.format(self.user, self.theme)

class UserThemeForm(ModelForm):
    class Meta:
        model = UserTheme
        fields = ['user', 'theme',]
