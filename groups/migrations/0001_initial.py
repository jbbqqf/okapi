# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('url', models.CharField(max_length=100)),
                ('ml', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('left', models.IntegerField()),
                ('right', models.IntegerField()),
            ],
        ),
    ]
