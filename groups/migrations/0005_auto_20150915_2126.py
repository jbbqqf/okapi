# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20150915_2110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='parent_id',
        ),
        migrations.AddField(
            model_name='group',
            name='parent',
            field=models.ForeignKey(default=1, to='groups.Group'),
            preserve_default=False,
        ),
    ]
