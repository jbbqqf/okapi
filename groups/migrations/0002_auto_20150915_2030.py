# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='ml',
            new_name='mailing',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='left',
            new_name='parent_id',
        ),
        migrations.RemoveField(
            model_name='group',
            name='right',
        ),
    ]
