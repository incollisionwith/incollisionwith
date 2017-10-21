# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 22:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_fsm


def insert_accident_record_states(apps, schema_editor):
    AccidentRecordState = apps.get_model('icw', 'AccidentRecordState')
    AccidentRecordState.objects.bulk_create([
        AccidentRecordState(id=0, label='STATS19',
                            official=True, reliable=True, pre_release=False,
                            description='Official STATS19 record'),
        AccidentRecordState(id=1, label='User submitted, pending moderation',
                            official=False, reliable=False, pre_release=False,
                            description='Added by a user, but not yet moderated by another user'),
        AccidentRecordState(id=2, label='User submitted, pre-release',
                            official=False, reliable=True, pre_release=True,
                            description='An unofficial record added before official data are released'),
        AccidentRecordState(id=3, label='User submitted, pending reconciliation',
                            official=False, reliable=False, pre_release=True,
                            description='An unofficial record added before official data are released but which hasn\'t'
                                        ' yet been reconciled now that official data has been released'),
        AccidentRecordState(id=4, label='User submitted, reasonably missing',
                            official=False, reliable=True, pre_release=False,
                            description='An unofficial record for an incident that doesn\'t fulfil all reporting'
                                        ' criteria and so is reasonably not recorded in the official data'),
        AccidentRecordState(id=6, label='User submitted, unreasonably missing',
                            official=False, reliable=True, pre_release=False,
                            description='An unofficial record for an incident that appears to fulfil all reporting'
                                        ' criteria and yet is not recorded in the official data'),

    ])

class Migration(migrations.Migration):

    dependencies = [
        ('icw', '0033_auto_20171018_0904'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccidentRecordState',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('official', models.BooleanField(default=False)),
                ('reliable', models.BooleanField(default=False)),
                ('pre_release', models.BooleanField(default=False)),
            ],
        ),
        migrations.RunPython(insert_accident_record_states, migrations.RunPython.noop),
        migrations.AddField(
            model_name='accident',
            name='record_state',
            field=django_fsm.FSMKeyField(default=0, on_delete=django.db.models.deletion.CASCADE, to='icw.AccidentRecordState'),
        ),
    ]
