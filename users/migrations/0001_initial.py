# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('profile_id', models.IntegerField(unique=True, editable=False)),
                ('locked', models.BooleanField(default=False)),
            ],
        ),
    ]
