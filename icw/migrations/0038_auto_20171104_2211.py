# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-04 22:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('icw', '0037_policeforce_geometry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='road_1_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accidents_1', to='icw.RoadClass'),
        ),
    ]
