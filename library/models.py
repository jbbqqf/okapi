# -*- coding: utf-8 -*-

from django.db.models import (Model, DateField, CharField)
from django.forms import ModelForm


class PressReview(Model):
    """
    On whippet you can find an interesting section of the library page
    containing press reviews. It has not been advertised and the pressreviews
    route aims to highlight those reviews.

    In fact, this model does not contain any press review itself, but it
    records dates on which press review has been made as well as a link to this
    review.

    With the import_press_reviews manage.py custom command you are able to
    download those press reviews pdfs in local media directory in order for
    users to be able to fetch pdfs from a local storage.
    """

    date = DateField()
    link = CharField(max_length=255)

    def __unicode__(self):
        return '{} press review'.format(self.date)


class PressReviewForm(ModelForm):
    class Meta:
        model = PressReview
        fields = ['date', 'link', ]
