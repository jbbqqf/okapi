# -*- coding: utf-8 -*-

from django.db import DataError, OperationalError
from django.db.models import (Model, ForeignKey, DateTimeField)
from django.forms import ModelForm

from django.contrib.auth.models import User
from score.models import Score


class Clear(Model):
    """
    Press the button !
    """

    user = ForeignKey(User)
    date = DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Clearing the button brings 10 * (timestamp - last clear timestamp)
        points if the previous owner is not equal to clearer.

        If it is the first take, 10 000 points are granted.
        """

        if self.pk:  # if this clear already exists
            raise OperationalError('Hey ! you can\'t change old clears, you '
                                   'little cheater !')

        latest = Clear.objects.latest('date')
        if latest.user == self.user:
            raise DataError('A user cannot clear two times in a row')

        super(Clear, self).save(*args, **kwargs)

        delta = self.date - latest.date
        points = delta.seconds * 10

        score = Score(user=self.user, game='b', value=points)
        score.save()

    def __unicode__(self):
        return '{} cleared {}'.format(self.user, self.date)


class ClearForm(ModelForm):
    class Meta:
        model = Clear
        fields = ('user',)
