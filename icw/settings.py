import os

DEBUG = True

TIME_ZONE = 'Europe/London'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'very secret key')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
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
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
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

