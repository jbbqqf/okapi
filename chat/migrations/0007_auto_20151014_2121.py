# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_auto_20151012_2118'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='channelgroup',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='channelgroup',
            name='channel',
        ),
        migrations.RemoveField(
            model_name='channelgroup',
            name='group',
        ),
        migrations.AlterUniqueTogether(
            name='channelmember',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='channelmember',
            name='channel',
        ),
        migrations.RemoveField(
            model_name='channelmember',
            name='user',
        ),
        migrations.DeleteModel(
            name='ChannelGroup',
        ),
        migrations.DeleteModel(
            name='ChannelMember',
        ),
    ]
