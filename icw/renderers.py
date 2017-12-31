import functools

from django.urls import reverse
from rest_framework import renderers
import ujson

from . import models


class GeoJSONRenderer(renderers.BaseRenderer):
    format = 'geojson'
    media_type = 'application/vnd.geo+json'

    def result_to_feature(self, result, renderer_context):
        if 'geometry' in result:
            geometry = result['geometry']
        elif 'location' in result:
            geometry = {
                'type': 'Point',
                'coordinates': [result['location']['lng'], result['location']['lat']],
            }
        else:
            geometry = None

        model = renderer_context['view'].queryset.model
        request = renderer_context['request']

        if model is models.Accident:
            properties = {
                'name': result['casualty_distribution'],
                'severity': result['severity'],
                'url': request.build_absolute_uri(reverse('accident-detail', kwargs={'pk': result['id']})),
            }
        elif model is models.PoliceForce:
            properties = {
                'name': result['label'],
                'url': request.build_absolute_uri(reverse('police-force-detail', kwargs={'pk': result['id']})),
            }
        else:
            properties = {}

        return {
            'id': result['id'],
            'type': 'Feature',
            'geometry': geometry,
            'properties': properties,
        }

    def render(self, data, accepted_media_type=None, renderer_context=None):
        dumps = functools.partial(ujson.dumps,
                                  indent=2 if 'indent' in renderer_context['request'].GET else 0,
                                  double_precision=6)

        if isinstance(data, list):
            results = data
        elif isinstance(data, dict) and 'results' in data:
            results = data['results']
        else:
            return dumps(self.result_to_feature(data, renderer_context))

        return dumps({
            'type': 'FeatureCollection',
            'features': [
                self.result_to_feature(result, renderer_context) for result in results
                ],
        })