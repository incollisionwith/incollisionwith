import json

from django.urls import reverse
from rest_framework import renderers


class GeoJSONRenderer(renderers.BaseRenderer):
    format = 'geojson'
    media_type = 'application/vnd.geo+json'

    def accident_to_feature(self, accident):
        return {
            'id': accident['id'],
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [accident['location']['lng'], accident['location']['lat']],
            },
            'properties': {
                'name': accident['casualty_distribution'],
                'severity': accident['severity'],
                'url': reverse('accident-detail', kwargs={'pk': accident['id']}),
            },
        }

    def render(self, data, accepted_media_type=None, renderer_context=None):
        accidents = data['results'] if isinstance(data, dict) else data
        return json.dumps({
            'type': 'FeatureCollection',
            'features': [
                self.accident_to_feature(accident) for accident in accidents if accident['location']
                ],
            # 'properties': {
            #     'count': data['count'] if isinstance(data, dict) else len(data),
            # },
        }, indent=2)