# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 02:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('icw', '0009_auto_20170919_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='pedestrian_crossing_human',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.PedestrianCrossingHuman'),
        ),
        migrations.AlterField(
            model_name='accident',
            name='pedestrian_crossing_physical',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.PedestrianCrossingPhysical'),
        ),
    ]
