from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django_filters import rest_framework as filters
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from icw.filters import AccidentFilter
from . import models, renderers, serializers


class AccidentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Accident.objects.all().prefetch_related('vehicle_distribution', 'casualty_distribution')
    serializer_class = serializers.AccidentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AccidentFilter

    renderer_classes = (
        JSONRenderer,
        BrowsableAPIRenderer,
        renderers.GeoJSONRenderer,
    )


class CitationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Citation.objects.all()
    serializer_class = serializers.CitationSerializer


class PoliceForceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.PoliceForce.objects.all()
    serializer_class = serializers.PoliceForceSerializer

    renderer_classes = (
        JSONRenderer,
        BrowsableAPIRenderer,
        renderers.GeoJSONRenderer,
    )