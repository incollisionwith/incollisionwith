# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 20:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icw', '0024_auto_20170923_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citation',
            name='image_url',
            field=models.URLField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='citation',
            name='publisher',
            field=models.URLField(blank=True, max_length=1024),
        ),
    ]
