# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 02:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('icw', '0010_auto_20170919_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='carriageway_hazards',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.CarriagewayHazards'),
        ),
        migrations.AlterField(
            model_name='accident',
            name='light_conditions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.LightConditions'),
        ),
        migrations.AlterField(
            model_name='accident',
            name='road_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.RoadType'),
        ),
        migrations.AlterField(
            model_name='accident',
            name='special_conditions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.SpecialConditions'),
        ),
        migrations.AlterField(
            model_name='accident',
            name='urban_rural',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.UrbanRural'),
        ),
        migrations.AlterField(
            model_name='accident',
            name='weather',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icw.Weather'),
        ),
    ]
