# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paged', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='debug',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='sent',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
