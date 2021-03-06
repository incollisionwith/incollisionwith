# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icw', '0003_auto_20170918_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='casualtyseverity',
            name='injury_definition',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hitobjectincarriageway',
            name='sentence_part',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roadclass',
            name='pattern',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicletype',
            name='class_driver',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicletype',
            name='class_passenger',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicletype',
            name='font_awesome',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='highwayauthority',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
