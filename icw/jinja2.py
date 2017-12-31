from django.conf import settings
from django.urls import reverse
from django_filters.fields import RangeField
from jinja2 import Environment
from leaflet.templatetags.leaflet_tags import leaflet_css, leaflet_js

from icw.util import other_page_url


def environment(**kwargs):
    env = Environment(**kwargs)
    env.globals.update({
        'static_url': settings.STATIC_URL,
        'login_url': settings.LOGIN_URL,
        'other_page_url': other_page_url,
        'is_range_field': lambda field: isinstance(field, RangeField),
        'widthratio': lambda value, max_value, max_width: int(value / max_value * max_width),
        'leaflet_css': leaflet_css,
        'leaflet_js': leaflet_js,
    })
    return env