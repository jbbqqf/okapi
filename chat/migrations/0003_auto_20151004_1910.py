# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_auto_20150920_2229'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_auto_20150920_2230'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('public', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChannelGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permissions', models.CharField(default=b'w', max_length=1, choices=[(b'r', b'read'), (b'w', b'write'), (b'a', b'admin')])),
                ('channel', models.ForeignKey(to='chat.Channel')),
                ('group', models.ForeignKey(to='groups.Group')),
            ],
        ),
        migrations.CreateModel(
            name='ChannelMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permissions', models.CharField(default=b'w', max_length=1, choices=[(b'r', b'read'), (b'w', b'write'), (b'a', b'admin')])),
                ('channel', models.ForeignKey(to='chat.Channel')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='channelmember',
            unique_together=set([('user', 'channel')]),
        ),
        migrations.AlterUniqueTogether(
            name='channelgroup',
            unique_together=set([('group', 'channel')]),
        ),
    ]
