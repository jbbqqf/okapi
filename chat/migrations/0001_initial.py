# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150916_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(default=b'm', max_length=1, choices=[(b'm', b'message'), (b's', b'score')])),
                ('content', models.CharField(max_length=512)),
                ('author', models.ForeignKey(to='users.User')),
            ],
        ),
    ]
