# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default=datetime.date(2017, 6, 20), upload_to=b'profile_images', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='website',
            field=models.URLField(default=datetime.date(2017, 6, 20), blank=True),
            preserve_default=False,
        ),
    ]
