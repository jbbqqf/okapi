# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150915_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=64)),
                ('lastname', models.CharField(max_length=64)),
                ('surname', models.CharField(max_length=24)),
                ('birthday', models.DateField()),
                ('note', models.TextField()),
                ('gender', models.CharField(default=b'n', max_length=1, choices=[(b'n', b'na'), (b'm', b'man'), (b'w', b'woman'), (b'u', b'unknown')])),
            ],
        ),
    ]
