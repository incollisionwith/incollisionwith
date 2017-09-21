import os

DEBUG = bool(os.environ.get('DJANGO_DEBUG'))
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split() if not DEBUG else ['*']

TIME_ZONE = 'Europe/London'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'very secret key')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_filters',
    'icw',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DATABASE_NAME', 'icw'),
    },
}

ROOT_URLCONF = 'icw.urls'

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # Match the template names ending in .html but not the ones in the admin folder.
            "match_extension": ".html",
            "match_regex": r"^(?!admin/).*",
            "app_dirname": "templates",
            'filters': {
                'add_class': 'widget_tweaks.templatetags.widget_tweaks.add_class',
            },
            'environment': 'icw.jinja2.environment',
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.static',
            ),
        },
    },    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.static',
            ),
        },
    },
]


STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT')

