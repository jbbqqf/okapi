# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_id',
        ),
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.ForeignKey(default=1, to='users.Profile'),
            preserve_default=False,
        ),
    ]
