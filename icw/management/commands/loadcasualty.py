import csv
import datetime
import sys

from django.core.management import BaseCommand

from ... import models
from ...util import indexed, sex_indexed


class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = csv.DictReader(sys.stdin)

        existing_ids = models.Casualty.objects.values_list('accident_id', 'vehicle_ref', 'casualty_ref', 'id')
        existing_ids = {(r[0], r[1], r[2]): r[3] for r in existing_ids}

        vehicle_refs = models.Vehicle.objects.values_list('accident_id', 'vehicle_ref', 'id')
        vehicle_refs = {(r[0], r[1]): r[2] for r in vehicle_refs}

        for row in reader:
            print(row)
            casualty = models.Casualty(**self.get_casualty_kwargs(row))
            existing_id = existing_ids.get((casualty.accident_id, casualty.vehicle_ref, casualty.casualty_ref))
            print(existing_id)
            casualty.id = existing_id
            casualty.vehicle_id = vehicle_refs[(casualty.accident_id, casualty.vehicle_ref)]
            if casualty.type_id == 0:
                casualty.pedestrian_hit_by_id = casualty.vehicle.type_id
            if existing_id:
                casualty.save(force_update=True)
            else:
                casualty.save(force_insert=True)

    def get_casualty_kwargs(self, row):
        return {
            'accident_id': row.get('Accident_Index') or row['\ufeffAccident_Index'],
            'vehicle_ref': indexed(row, 'Vehicle_Reference'),
            'casualty_ref': indexed(row, 'Casualty_Reference'),
            'casualty_class_id': indexed(row, 'Casualty_Class'),
            'sex_id': indexed(row, 'Sex_of_Casualty'),
            'age': indexed(row, 'Age_of_Casualty'),
            'age_band_id': indexed(row, 'Age_Band_of_Casualty'),
            'severity_id': indexed(row, 'Casualty_Severity'),
            'type_id': indexed(row, 'Casualty_Type'),
            'pedestrian_location_id': indexed(row, 'Pedestrian_Location'),
            'pedestrian_movement_id': indexed(row, 'Pedestrian_Movement')
        }
