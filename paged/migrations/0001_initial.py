# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('received_date', models.DateTimeField(default=None)),
                ('sender', models.CharField(default=None, max_length=32)),
                ('message', models.CharField(default=None, max_length=1600)),
                ('post_serialized', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=254)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
