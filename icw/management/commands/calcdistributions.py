import csv
import datetime
import sys

import collections
from django.core.management import BaseCommand

from ... import models
from ...util import indexed, sex_indexed


import logging

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.vcounts, self.ccounts = collections.defaultdict(int), collections.defaultdict(int)
        self.to_update = set()
        self.vupdates, self.cupdates = collections.defaultdict(set), collections.defaultdict(set)
        self.vdistributions = {cd.distribution: cd for cd in models.VehicleDistribution.objects.all()}
        self.cdistributions = {cd.distribution: cd for cd in models.CasualtyDistribution.objects.all()}

        for i in range(0, models.Accident.objects.count(), 1000):
            for accident in models.Accident.objects.all()[i:i+1000]:
                vdistribution = collections.defaultdict(int)
                cdistribution = collections.defaultdict(int)

                for vehicle in accident.vehicles.all():
                    vdistribution[vehicle.type_id or -1] += 1
                for casualty in accident.casualties.all():
                    cdistribution[(casualty.type_id, casualty.severity_id)] += 1

                vdistribution = ', '.join('{}: {}'.format(k, v) for k, v in sorted(vdistribution.items()))
                cdistribution = ', '.join('{} {}: {}'.format(k[0], k[1], v) for k, v in sorted(cdistribution.items()))

                self.vcounts[vdistribution] += 1
                self.ccounts[cdistribution] += 1

                if vdistribution in self.vdistributions:
                    vd = self.vdistributions[vdistribution]
                    if accident.vehicle_distribution_id != vd.id:
                        self.vupdates[vd.id].add(accident.id)
                        self.to_update.add(vd)
                else:
                    vd = self.vdistributions[vdistribution] = models.VehicleDistribution.objects.create(distribution=vdistribution)
                    self.vupdates[vd.id].add(accident.id)
                    self.to_update.add(vd)

                if cdistribution in self.cdistributions:
                    cd = self.cdistributions[cdistribution]
                    if accident.casualty_distribution_id != cd.id:
                        self.cupdates[cd.id].add(accident.id)
                        self.to_update.add(cd)
                else:
                    cd = self.cdistributions[cdistribution] = models.CasualtyDistribution.objects.create(distribution=cdistribution)
                    self.cupdates[cd.id].add(accident.id)
                    self.to_update.add(cd)

                vd.count = self.vcounts[vdistribution]
                cd.count = self.ccounts[cdistribution]


            self.update_counts(i)

    def update_counts(self, i):
        print(i, len(self.vcounts), len(self.ccounts))
        for distribution in self.to_update:
            distribution.save(force_update=True)
        for vd_id, ids in self.vupdates.items():
            models.Accident.objects.filter(id__in=ids).update(vehicle_distribution_id=vd_id)
        for cd_id, ids in self.cupdates.items():
            models.Accident.objects.filter(id__in=ids).update(casualty_distribution_id=cd_id)
        self.to_update.clear()
        self.vupdates.clear()
        self.cupdates.clear()