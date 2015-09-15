# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20150915_2102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupuser',
            old_name='group_id',
            new_name='group',
        ),
        migrations.RenameField(
            model_name='groupuser',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='groupuser',
            unique_together=set([('user', 'group')]),
        ),
    ]
