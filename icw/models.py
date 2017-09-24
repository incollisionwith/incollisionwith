
from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property


class ReferenceModel(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    label = models.CharField(max_length=128)

    class Meta:
        abstract = True
        ordering = ('id',)

    def __str__(self):
        return self.label


class PoliceForce(ReferenceModel):
    uri = models.URLField(db_index=True)
    comment = models.TextField()
    homepage =models.TextField()
    logo_url = models.TextField()
    dbpedia = models.TextField()


class Severity(ReferenceModel):
    pass


class JunctionControl(ReferenceModel):
    pass


class JunctionDetail(ReferenceModel):
    pass


class RoadType(ReferenceModel):
    pass


class RoadClass(ReferenceModel):
    pattern = models.TextField()


class PedestrianCrossingHuman(ReferenceModel):
    pass


class PedestrianCrossingPhysical(ReferenceModel):
    pass


class LightConditions(ReferenceModel):
    pass


class Weather(ReferenceModel):
    pass


class RoadSurface(ReferenceModel):
    pass


class SpecialConditions(ReferenceModel):
    pass


class CarriagewayHazards(ReferenceModel):
    pass


class UrbanRural(ReferenceModel):
    pass


class HighwayAuthority(ReferenceModel):
    id = models.CharField(max_length=20, primary_key=True)



class AgeBand(ReferenceModel):
    gte = models.SmallIntegerField(null=True, blank=True)
    lt = models.SmallIntegerField(null=True, blank=True)


class CasualtyClass(ReferenceModel):
    pass


class CasualtySeverity(ReferenceModel):
    injury_definition = models.TextField()
    comment = models.TextField()


class FirstPointOfImpact(ReferenceModel):
    pass


class HitObjectInCarriageway(ReferenceModel):
    sentence_part = models.TextField()


class HitObjectOffCarriageway(ReferenceModel):
    pass


class PedestrianLocation(ReferenceModel):
    pass


class PedestrianMovement(ReferenceModel):
    pass


class Sex(ReferenceModel):
    pass


class SkiddingAndOverturning(ReferenceModel):
    pass


class TowingAndArticulation(ReferenceModel):
    pass


class VehicleLeavingCarriageway(ReferenceModel):
    pass


class VehicleLocation(ReferenceModel):
    pass


class JunctionLocation(ReferenceModel):
    pass


class VehicleManoeuvre(ReferenceModel):
    pass


class VehicleType(ReferenceModel):
    font_awesome = models.CharField(max_length=30, blank=True)
    class_driver = models.CharField(max_length=40)
    class_passenger = models.CharField(max_length=40)
    character = models.CharField(max_length=4, blank=True)


class VehicleDistribution(models.Model):
    distribution = models.TextField(unique=True)
    count = models.IntegerField(default=0)

    as_text = models.TextField()
    as_html = models.TextField()

    def save(self, *args, **kwargs):
        if not self.as_html:
            as_html, as_text = [], []
            ds = self.distribution.split(', ')
            groups = []
            for d in ds:
                groups.append(tuple(map(int, d.split(': '))))
            for type_id, count in sorted(groups, reverse=True):
                try:
                    vehicle_type = VehicleType.objects.get(id=type_id)
                except VehicleType.DoesNotExist:
                    vehicle_type = VehicleType(label='Unknown vehicle', character='❓', font_awesome='circle')
                for i in range(count):
                    as_html.append('<i class="fa fa-{}" title="{}"> </i>'.format(vehicle_type.font_awesome,
                                                                                 vehicle_type.label))
                    as_text.append(vehicle_type.character)
                self.as_html = ''.join(as_html)
                self.as_text = ''.join(as_text)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.as_text


class CasualtyDistribution(models.Model):
    distribution = models.TextField(unique=True)
    count = models.IntegerField(default=0)

    as_text = models.TextField()
    as_html = models.TextField()

    def save(self, *args, **kwargs):
        if not self.as_html:
            as_html, as_text = [], []
            ds = self.distribution.split(', ')
            current_severity_id = None
            groups = []
            for d in ds:
                d, count = d.split(': ')
                type_id, severity_id = d.split(' ')
                type_id, severity_id, count = int(type_id), int(severity_id), int(count)
                groups.append(((severity_id, -type_id), severity_id, type_id, count))
            for _, severity_id, type_id, count in sorted(groups):
                try:
                    vehicle_type = VehicleType.objects.get(id=type_id)
                except VehicleType.DoesNotExist:
                    vehicle_type = VehicleType(label='Unknown vehicle', character='❓', font_awesome='circle')
                if severity_id != current_severity_id:
                    if as_text:
                        as_text.append(', ')
                    as_text.append({1: 'Fatal: ', 2: 'Serious: ', 3: 'Slight: '}[severity_id])
                    current_severity_id = severity_id
                for i in range(count):
                    as_html.append('<i class="fa fa-{} casualty-severity-{}" title="{}"> </i>'.format(
                        vehicle_type.font_awesome,
                        severity_id,
                        vehicle_type.label))
                    as_text.append(vehicle_type.character)
                self.as_html = ''.join(as_html)
                self.as_text = ''.join(as_text)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.as_text


class Accident(models.Model):
    id = models.CharField(max_length=13, primary_key=True)
    location = PointField(db_index=True, null=True)
    police_force = models.ForeignKey(PoliceForce)
    severity = models.ForeignKey(CasualtySeverity)
    junction_control = models.ForeignKey(JunctionControl, null=True, blank=True)
    junction_detail = models.ForeignKey(JunctionDetail, null=True, blank=True)

    number_of_vehicles = models.SmallIntegerField()
    number_of_casualties = models.SmallIntegerField()

    casualty_distribution = models.ForeignKey(CasualtyDistribution, null=True, blank=True)
    vehicle_distribution = models.ForeignKey(VehicleDistribution, null=True, blank=True)

    date = models.DateField(db_index=True)
    date_and_time = models.DateTimeField(db_index=True, null=True, blank=True)
    police_attended = models.BooleanField()

    speed_limit = models.SmallIntegerField(null=True, blank=True)
    road_1_class = models.ForeignKey(RoadClass, related_name='accidents_1')
    road_1_number = models.SmallIntegerField(null=True, blank=True)
    road_1 = models.CharField(max_length=10)
    road_2_class = models.ForeignKey(RoadClass, null=True, blank=True, related_name='accidents_2')
    road_2_number = models.SmallIntegerField(null=True, blank=True)
    road_2 = models.CharField(max_length=10, blank=True)

    pedestrian_crossing_human = models.ForeignKey(PedestrianCrossingHuman, null=True, blank=True)
    pedestrian_crossing_physical = models.ForeignKey(PedestrianCrossingPhysical, null=True, blank=True)

    light_conditions = models.ForeignKey(LightConditions, null=True, blank=True)
    weather = models.ForeignKey(Weather, null=True, blank=True)
    road_surface = models.ForeignKey(RoadSurface, null=True, blank=True)
    road_type = models.ForeignKey(RoadType, null=True, blank=True)
    special_conditions = models.ForeignKey(SpecialConditions, null=True, blank=True)
    carriageway_hazards = models.ForeignKey(CarriagewayHazards, null=True, blank=True)
    urban_rural = models.ForeignKey(UrbanRural, null=True, blank=True)

    highway_authority = models.ForeignKey(HighwayAuthority, db_index=True)

    solar_elevation = models.FloatField(null=True, blank=True)
    moon_phase = models.SmallIntegerField(null=True)
    citations = models.BooleanField(verbose_name='References?', default=False)

    @cached_property
    def annotation(self):
        try:
            return self._annotation
        except AccidentAnnotation.DoesNotExist:
            return None

    def get_absolute_url(self):
        return reverse('accident-detail', args=(self.pk,))


class Vehicle(models.Model):
    accident = models.ForeignKey(Accident, db_index=True, related_name='vehicles')
    vehicle_ref = models.SmallIntegerField()

    type = models.ForeignKey(VehicleType, null=True, blank=True)
    towing_and_articulation = models.ForeignKey(TowingAndArticulation, null=True, blank=True)
    location = models.ForeignKey(VehicleLocation, null=True, blank=True)
    manoeuvre = models.ForeignKey(VehicleManoeuvre, null=True, blank=True)
    junction_location = models.ForeignKey(JunctionLocation, null=True, blank=True)

    hit_object_in_carriageway = models.ForeignKey(HitObjectInCarriageway, null=True, blank=True)
    hit_object_off_carriageway = models.ForeignKey(HitObjectOffCarriageway, null=True, blank=True)
    first_point_of_impact = models.ForeignKey(FirstPointOfImpact, null=True, blank=True)
    skidding_and_overturning = models.ForeignKey(SkiddingAndOverturning, null=True, blank=True)
    leaving_carriageway = models.ForeignKey(VehicleLeavingCarriageway, null=True, blank=True)

    driver_sex = models.ForeignKey(Sex, null=True, blank=True)
    driver_age_band = models.ForeignKey(AgeBand, null=True, blank=True)
    driver_age = models.SmallIntegerField(null=True, blank=True)

    age_of_vehicle = models.SmallIntegerField(null=True)
    engine_capacity = models.IntegerField(null=True)
    make = models.TextField(blank=True)
    model = models.TextField(blank=True)

    class Meta:
        unique_together = (('accident', 'vehicle_ref'),)
        ordering = ('accident', 'vehicle_ref')


class Casualty(models.Model):
    accident = models.ForeignKey(Accident, db_index=True, related_name='casualties')
    vehicle = models.ForeignKey(Vehicle, db_index=True, related_name='casualties')

    vehicle_ref = models.PositiveIntegerField()
    casualty_ref = models.PositiveIntegerField()

    casualty_class = models.ForeignKey(CasualtyClass, null=True, blank=True)
    sex = models.ForeignKey(Sex, null=True, blank=True)
    severity = models.ForeignKey(CasualtySeverity, null=True, blank=True)
    age_band = models.ForeignKey(AgeBand, null=True, blank=True)
    type = models.ForeignKey(VehicleType, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)

    pedestrian_location = models.ForeignKey(PedestrianLocation, null=True, blank=True)
    pedestrian_movement = models.ForeignKey(PedestrianMovement, null=True, blank=True)

    class Meta:
        unique_together = (('accident', 'vehicle_ref', 'casualty_ref'),)
        ordering = ('accident', 'casualty_ref')


class AccidentAnnotation(models.Model):
    accident = models.OneToOneField(Accident, null=True, blank=True, related_name='_annotation')
    date = models.DateField(null=True, blank=True)
    location = PointField(null=True, blank=True)

    title = models.TextField(blank=True)
    description = models.TextField(blank=True)


class Citation(models.Model):
    annotation = models.ForeignKey(AccidentAnnotation, related_name='citations')
    href = models.URLField(verbose_name='URL', max_length=1024)

    status = models.CharField(max_length=3, blank=True)
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, max_length=1024)
    published = models.DateTimeField(null=True, blank=True)
    publisher = models.URLField(blank=True, max_length=1024)
    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    modified = models.DateTimeField(auto_now=True)
    #moderation = models.NullBooleanField(default=None)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.status:
            from . import tasks
            tasks.fetch_citation.delay(self.pk)

    class Meta:
        ordering = ('published', 'created')