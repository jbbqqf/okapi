# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_okagroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='okagroup',
            name='parent',
            field=models.ForeignKey(to='groups.okaGroup', null=True),
        ),
    ]
