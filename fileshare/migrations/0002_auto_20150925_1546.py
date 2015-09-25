# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileshare', '0001_squashed_0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(to='fileshare.Directory', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='file',
            name='type',
        ),
        migrations.AlterField(
            model_name='file',
            name='parent',
            field=models.ForeignKey(to='fileshare.Directory', null=True),
        ),
    ]
