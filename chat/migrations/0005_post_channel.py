# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20151004_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='channel',
            field=models.ForeignKey(default=1, to='chat.Channel'),
            preserve_default=False,
        ),
    ]
