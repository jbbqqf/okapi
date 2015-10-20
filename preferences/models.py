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

class UserTheme(models.Model):
    """
    A many to many relationship model to record theme user preferences.
    """

    user = models.ForeignKey(User)
#     theme = models.ForeignKey(Theme)
# 
#     def __unicode__(self):
#         return u'{} has theme {}'.format(self.user, self.theme)
# 
#     @classmethod
#     def _validate_unique(cls, self):
#         """
#         http://stackoverflow.com/questions/15160721/forcing-unique-together-with-model-inheritance 
#         """
# 
#         try:
#             user_theme = cls._default_manager.get(user=self.user,
#                                                   theme__ui=self.theme.ui)
#             if not user_theme == self:
#                 raise IntegrityError('Duplicate')
# 
#         except cls.DoesNotExist:
#             pass
# 
#     def clean(self):
#        self._validate_unique(self)

class UserThemeForm(ModelForm):
    class Meta:
        model = UserTheme
        fields = ['user',]
