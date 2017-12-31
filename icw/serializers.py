from rest_framework import serializers
import ujson

from . import models


class PointSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if instance:
            return {'lng': instance[0], 'lat': instance[1]}


class GeoJSONSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if instance:
            return ujson.loads(instance.geojson)


class AccidentSerializer(serializers.ModelSerializer):
    vehicle_distribution = serializers.StringRelatedField()
    casualty_distribution = serializers.StringRelatedField()
    location = PointSerializer()

    class Meta:
        model = models.Accident
        fields = '__all__'


class CitationSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = models.Citation
        fields = '__all__'


class PoliceForceSerializer(serializers.ModelSerializer):
    geometry = GeoJSONSerializer()

    class Meta:
        model = models.PoliceForce
        fields = ('id', 'label', 'homepage', 'geometry')
