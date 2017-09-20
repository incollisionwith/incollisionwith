import csv
import datetime
import sys

from django.core.management import BaseCommand

from ... import models
from ...util import indexed, sex_indexed


class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = csv.DictReader(sys.stdin)

        existing_ids = models.Vehicle.objects.values_list('accident_id', 'vehicle_ref', 'id')
        existing_ids = {(r[0], r[1]): r[2] for r in existing_ids}

        for row in reader:
            print(row)
            vehicle = models.Vehicle(**self.get_vehicle_kwargs(row))
            existing_id = existing_ids.get((vehicle.accident_id, vehicle.vehicle_ref))
            vehicle.id = existing_id
            if existing_id:
                vehicle.save(force_update=True)
            else:
                vehicle.save(force_insert=True)

    def get_vehicle_kwargs(self, row):
        return {
            'accident_id': row.get('Accident_Index') or row['\ufeffAccident_Index'],
            'vehicle_ref': int(row['Vehicle_Reference']),
            'type_id': indexed(row, 'Vehicle_Type'),
            'driver_sex_id': sex_indexed(row, 'Sex_of_Driver'),
            'driver_age': indexed(row, 'Age_of_Driver'),
            'driver_age_band_id': indexed(row, 'Age_Band_of_Driver'),
            'manoeuvre_id': indexed(row, 'Vehicle_Manoeuvre'),
            'location_id': indexed(row, 'Vehicle_Location-Restricted_Lane'),
            'towing_and_articulation_id': indexed(row, 'Towing_and_Articulation'),
            'junction_location_id': indexed(row, 'Junction_Location'),
            'skidding_and_overturning_id': indexed(row, 'Skidding_and_Overturning'),
            'hit_object_in_carriageway_id': indexed(row, 'Hit_Object_in_Carriageway'),
            'hit_object_off_carriageway_id': indexed(row, 'Hit_Object_off_Carriageway'),
            'first_point_of_impact_id': indexed(row, '1st_Point_of_Impact'),
            'leaving_carriageway_id': indexed(row, 'Vehicle_Leaving_Carriageway'),
        }
