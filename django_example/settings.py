import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

## SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#2nxx4w+zut-=v6696%1d(9x^!$9dr_+jz%$me91q+dcke5pv!'

## SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

## Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_example',
    'query_parameters'
)

ROOT_URLCONF = 'django_example.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'django_example', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        }
    },
]
