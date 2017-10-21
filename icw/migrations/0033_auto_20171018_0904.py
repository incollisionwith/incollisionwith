# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-18 09:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icw', '0032_citation_unique'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accidentannotation',
            name='accident',
        ),
        migrations.AlterModelOptions(
            name='highwayauthority',
            options={'ordering': ('label',)},
        ),
        migrations.AlterModelOptions(
            name='policeforce',
            options={'ordering': ('label',)},
        ),
        migrations.DeleteModel(
            name='AccidentAnnotation',
        ),
    ]