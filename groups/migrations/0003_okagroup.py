# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('groups', '0002_auto_20150920_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='okaGroup',
            fields=[
                ('group_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='auth.Group')),
                ('url', models.CharField(max_length=100, blank=True)),
                ('mailing', models.CharField(max_length=100, blank=True)),
                ('description', models.TextField(blank=True)),
                ('parent', models.ForeignKey(to='groups.okaGroup')),
            ],
            bases=('auth.group',),
        ),
    ]
