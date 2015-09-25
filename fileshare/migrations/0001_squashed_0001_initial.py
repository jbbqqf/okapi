# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'fileshare', '0001_initial')]

    dependencies = [
        ('groups', '0002_auto_20150920_2229'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('type', models.CharField(default=b'f', max_length=1, choices=[(b'f', b'file'), (b'd', b'directory')])),
                ('deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('ownergroup', models.ForeignKey(to='groups.Group', null=True)),
                ('parent', models.ForeignKey(to='fileshare.File', null=True)),
            ],
        ),
    ]
