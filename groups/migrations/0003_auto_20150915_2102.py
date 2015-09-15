# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150915_2102'),
        ('groups', '0002_auto_20150915_2030'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=1, choices=[(b'u', b'user'), (b'a', b'admin')])),
                ('group_id', models.ForeignKey(to='groups.Group')),
                ('user_id', models.ForeignKey(to='users.User')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='groupuser',
            unique_together=set([('user_id', 'group_id')]),
        ),
    ]
