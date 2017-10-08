from html import escape

import django_filters
from django_filters import rest_framework as filters
from django.contrib.gis.geos import Polygon
from django import forms
from django.core.exceptions import ValidationError

from . import models


class BoundingBoxField(forms.Field):
    def to_python(self, value):
        if value:
            try:
                values = [float(v.strip()) for v in value.split(',')]
            except ValueError:
                raise ValidationError("Value should be four floats, delimited by commas")
            if len(values) != 4:
                raise ValidationError("Value should be four floats, delimited by commas")
            return Polygon(((values[0], values[1]),
                            (values[2], values[1]),
                            (values[2], values[3]),
                            (values[0], values[3]),
                            (values[0], values[1])))


class PointFilter(django_filters.Filter):
    field_class = BoundingBoxField

    def filter(self, qs, value):
        if value:
            lookup = "{}__coveredby".format(self.name)
            qs = self.get_method(qs)(**{lookup: value})
        return qs


class AccidentFilter(filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(label='Date range')
    casualty_distribution = django_filters.ModelMultipleChoiceFilter(queryset=models.CasualtyDistribution.objects.order_by('-count'))
    vehicle_distribution = django_filters.ModelMultipleChoiceFilter(queryset=models.VehicleDistribution.objects.order_by('-count'))
    has_citations = django_filters.BooleanFilter()
    number_of_vehicles = django_filters.RangeFilter()
    number_of_casualties = django_filters.RangeFilter()
    bbox = PointFilter(name='location',
                       help_text=escape('The coordinate values of two opposite corners of a bounding box, as "<SW lng>,<SW lat>,<NE lng>,<NE lat>"'))

    class Meta:
        model = models.Accident
        fields = ['date', 'severity', 'has_citations', 'number_of_vehicles', 'number_of_casualties',
                  'police_force', 'highway_authority',
                  'carriageway_hazards', 'vehicles__hit_object_in_carriageway', 'vehicles__hit_object_off_carriageway',
                  'casualty_distribution', 'vehicle_distribution', 'bbox']


class CasualtyFilter(filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(name='accident__date', label='Date range')
    pedestrian_hit_by = django_filters.ModelChoiceFilter(queryset=models.VehicleType.objects.exclude(id=0))

    class Meta:
        model = models.Casualty
        fields = ['date', 'type', 'severity', 'age_band', 'vehicle__location', 'pedestrian_location',
                  'pedestrian_hit_by', 'accident__police_force', 'accident__highway_authority',
                  'accident__has_citations']
