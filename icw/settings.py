import os

DEBUG = bool(os.environ.get('DJANGO_DEBUG'))
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split() if not DEBUG else ['*']

TIME_ZONE = 'Europe/London'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'very secret key')

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS = [
    'icw',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'social_django',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DATABASE_NAME', 'icw'),
    },
}

ROOT_URLCONF = 'icw.urls'

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
]

try:
    import debug_toolbar
except ImportError:
    pass
else:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')



TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # Match the template names ending in .html but not the ones in the admin folder.
            "match_extension": ".html",
            "match_regex": r"^(?!(admin|debug_toolbar|rest_framework|django_filters)/).*",
            "app_dirname": "templates",
            'filters': {
                'add_class': 'widget_tweaks.templatetags.widget_tweaks.add_class',
            },
            'environment': 'icw.jinja2.environment',
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.static',
            ),
            'extensions': [
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
                "jinja2.ext.with_",
                "jinja2.ext.i18n",
                "jinja2.ext.autoescape",
                "django_jinja.builtins.extensions.CsrfExtension",
                "django_jinja.builtins.extensions.CacheExtension",
                "django_jinja.builtins.extensions.TimezoneExtension",
                "django_jinja.builtins.extensions.UrlsExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
                "django_jinja.builtins.extensions.DjangoFiltersExtension",
            ]
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

for key in os.environ:
    if key.startswith('SOCIAL_AUTH_'):
        locals()[key] = os.environ[key]

LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_URL = '/logout/'
LOGIN_URL = '/login/twitter/'


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 1000,
}