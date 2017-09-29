import csv
import datetime
import sys

import collections
from django.core.management import BaseCommand

from icw.models import Tag, Casualty, Vehicle, Accident, Tagging
from ... import models
from ...util import indexed, sex_indexed


import logging


class Command(BaseCommand):
    def handle(self, *args, **options):
        left_hook_tag, _ = Tag.objects.get_or_create(tag='left-hook')
        left_hook_tag.label = 'Vehicle was hit by another vehicle turning left across its path'
        left_hook_tag.methodology = 'This tag is applied to vehicles which were going ahead when another vehicle collided'
        left_hook_tag.automated = True
        left_hook_tag.save()

        right_hook_tag, _ = Tag.objects.get_or_create(tag='right-hook')
        right_hook_tag.label = 'Vehicle was hit by another vehicle turning right across its path'
        right_hook_tag.automated = True
        right_hook_tag.save()

        count = Accident.objects.count()
        for i in range(0, count, 10000):
            print("{} of {}".format(i, count))
            for accident in Accident.objects.filter(number_of_vehicles=2).order_by('id').prefetch_related('vehicles')[i:i+10000]:
                vehicle_1, vehicle_2 = accident.vehicles.all()
                if vehicle_2.manoeuvre_id != 7:
                    vehicle_1, vehicle_2 = vehicle_2, vehicle_1

                current_tag = Tagging.objects.filter(tag=left_hook_tag, vehicle=vehicle_1).first()
                if vehicle_1.manoeuvre_id in (15, 16, 17, 18) and vehicle_2.manoeuvre_id == 7 \
                        and vehicle_1.junction_location_id in (0, 1, 8) and vehicle_2.junction_location_id in (0, 1, 3, 5, 8):
                    if not current_tag:
                        vehicle_1.taggings.add(Tagging.objects.create(tag=left_hook_tag, vehicle=vehicle_1))
                else:
                    if current_tag:
                        current_tag.delete()

                if vehicle_2.manoeuvre_id != 9:
                    vehicle_1, vehicle_2 = vehicle_2, vehicle_1

                current_tag = Tagging.objects.filter(tag=right_hook_tag, vehicle=vehicle_1).first()
                if vehicle_1.manoeuvre_id in (16, 17, 18) and vehicle_2.manoeuvre_id == 9 \
                        and vehicle_1.junction_location_id in (0, 1, 8) and vehicle_2.junction_location_id in (0, 1, 5, 8):
                    if not current_tag:
                        vehicle_1.taggings.add(Tagging.objects.create(tag=right_hook_tag, vehicle=vehicle_1))
                else:
                    if current_tag:
                        current_tag.delete()
