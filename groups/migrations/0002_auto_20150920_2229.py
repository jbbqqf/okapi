# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='mailing',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='url',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='groupuser',
            name='role',
            field=models.CharField(default=b'u', max_length=1, choices=[(b'u', b'user'), (b'a', b'admin')]),
        ),
    ]
