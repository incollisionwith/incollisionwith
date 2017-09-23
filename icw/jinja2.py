from django.conf import settings
from django.urls import reverse
from jinja2 import Environment


def environment(**kwargs):
    env = Environment(**kwargs)
    env.globals.update({
        'static_url': settings.STATIC_URL,
        'login_url': settings.LOGIN_URL,
    })
    return env