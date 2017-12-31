import requests
from django.contrib.gis.geos import GEOSGeometry
from django.core.management import BaseCommand

from ... import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        for highway_authority in models.HighwayAuthority.objects.exclude(geometry__isnull=False):
            print("Fetching {} {}".format(highway_authority.id, highway_authority.label))
            response = requests.get('https://mapit.mysociety.org/code/gss/{}'.format(highway_authority.mapit_id or highway_authority.id))
            if response.ok:
                response = requests.get(response.url + '.geojson')
                #print(response.content)
                highway_authority.geometry = GEOSGeometry(response.content)
                highway_authority.save()
            else:
                print("  Not found")
