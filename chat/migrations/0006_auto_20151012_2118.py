# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_post_channel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='channel',
            options={'permissions': (('read_channel', 'Read Channel'), ('write_channel', 'Write Channel'), ('admin_channel', 'Admin Channel'))},
        ),
    ]
