# -*- coding: utf-8 -*-

from django.db.models import (Model, ForeignKey, CharField, IntegerField,
                              DateTimeField, OneToOneField)
from django.forms import ModelForm

from django.contrib.auth.models import User


class Score(Model):
    """
    A Score entry is a discrete differential value at a given date for a user
    refering to a game.

    Instead of recording a single score value for each user, it allows
    flexibility to display score tables that can be filtered for a particular
    game and/or between two dates.

    For exemple, we can imagine a monthly score table only for button players.
    """

    GAMES = (
        ('p', 'preums'),
        ('d', 'deuz'),
        ('t', 'troiz'),
        ('b', 'button'),
    )

    user = ForeignKey(User)
    game = CharField(max_length=1, choices=GAMES)
    value = IntegerField()
    date = DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        A score entry also updates the user's current score. Current scores
        are a single value per user instead of having to compute over a large
        amount of score entries to retrieve the main score.
        """

        if self.pk:  # does this score already exists (!= updated)
            old_score = Score.objects.get(pk=self.pk)

            old_user_current_score, created = \
                CurrentScore.objects.get_or_create(user=old_score.user,
                                                   defaults={'value': 0})
            old_user_current_score.update(-old_score.value)
            old_user_current_score.save()

        current_score, created = CurrentScore.objects.get_or_create(
            user=self.user, defaults={'value': 0})
        current_score.update(self.value)
        current_score.save()

        super(Score, self).save(*args, **kwargs)

        def __unicode__(self):
            return '{} scored {} ({})'.format(self.user, self.value, self.game)


class ScoreForm(ModelForm):
    class Meta:
        model = Score
        fields = ('user', 'game', 'value',)


class CurrentScore(Model):
    """
    Current scores are a single value per user easy to serve instead of having
    to compute over a large amount of score entries to retrieve the main
    scores.
    """

    user = OneToOneField(User)
    value = IntegerField()

    def update(self, value):
        self.value += value

    def __unicode__(self):
        return '{} has {} pts'.format(self.user, self.value)


class CurrentScoreForm(ModelForm):
    class Meta:
        model = CurrentScore
        fields = ('user', 'value',)
