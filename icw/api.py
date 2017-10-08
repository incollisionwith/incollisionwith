from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django_filters import rest_framework as filters

from icw.filters import AccidentFilter
from . import models, serializers


class AccidentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Accident.objects.all().prefetch_related('vehicle_distribution', 'casualty_distribution')
    serializer_class = serializers.AccidentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AccidentFilter


class CitationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Citation.objects.all()
    serializer_class = serializers.CitationSerializer
