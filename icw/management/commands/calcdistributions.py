import csv
import datetime
import sys

import collections
from django.core.management import BaseCommand

from ... import models
from ...util import indexed, sex_indexed


class Command(BaseCommand):
    def handle(self, *args, **options):
        vcounts, ccounts = collections.defaultdict(int), collections.defaultdict(int)
        vdistributions = {cd.distribution: cd for cd in models.VehicleDistribution.objects.all()}
        cdistributions = {cd.distribution: cd for cd in models.CasualtyDistribution.objects.all()}
        for accident in models.Accident.objects.all():
            vdistribution = collections.defaultdict(int)
            cdistribution = collections.defaultdict(int)

            for vehicle in accident.vehicles.all():
                vdistribution[vehicle.type_id or -1] += 1
            for casualty in accident.casualties.all():
                cdistribution[(casualty.type_id, casualty.severity_id)] += 1

            vdistribution = ', '.join('{}: {}'.format(k, v) for k, v in sorted(vdistribution.items()))
            cdistribution = ', '.join('{} {}: {}'.format(k[0], k[1], v) for k, v in sorted(cdistribution.items()))

            vcounts[vdistribution] += 1
            ccounts[cdistribution] += 1

            if vdistribution in vdistributions:
                vd = vdistributions[vdistribution]
            else:
                vd = vdistributions[vdistribution] = models.VehicleDistribution.objects.create(distribution=vdistribution)

            if cdistribution in cdistributions:
                cd = cdistributions[cdistribution]
            else:
                cd = cdistributions[cdistribution] = models.CasualtyDistribution.objects.create(distribution=cdistribution)

            models.Accident.objects.filter(id=accident.id).update(casualty_distribution_id=cd.id,
                                                                  vehicle_distribution=vd.id)
            models.VehicleDistribution.objects.filter(id=vd.id).update(count=vcounts[vdistribution])
            models.CasualtyDistribution.objects.filter(id=cd.id).update(count=ccounts[cdistribution])

            print(len(vcounts), len(ccounts))