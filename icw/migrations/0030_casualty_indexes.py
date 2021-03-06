# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 19:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('icw', '0029_citation_to_accident'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casualty',
            name='severity',
            field=models.ForeignKey(to='icw.CasualtySeverity', db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='casualty',
            name='age_band',
            field=models.ForeignKey(to='icw.AgeBand', db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='casualty',
            name='type',
            field=models.ForeignKey(to='icw.VehicleType', db_index=True, null=True, blank=True),
        ),
    ]
