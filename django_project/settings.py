# Import sys (to adjust Python path)
import sys
# Import some utility functions
import os
from os.path import abspath, basename, dirname, join, normpath
import deploymentutils as du


# export DJANGO_DEVMODE=True; py3 manage.py custom_command
env_devmode = os.getenv("DJANGO_DEVMODE")
if env_devmode is None:
    DEVMODE = "runserver" in sys.argv or "shell" in sys.argv
else:
    DEVMODE = env_devmode.lower() == "true"

# this will be overridden by unittests
TESTMODE = False



cfg = du.get_nearest_config("config.ini", devmode=DEVMODE)



SECRET_KEY = cfg("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = cfg("DEBUG")

ALLOWED_HOSTS = cfg("ALLOWED_HOSTS", cast=cfg.Csv())

DJANGO_URL_PREFIX = cfg("django_url_prefix").lstrip("/")

# #########################################################

# ##### PATH CONFIGURATION ################################

# Fetch Django's project directory
DJANGO_ROOT = dirname(abspath(__file__))
assert os.path.isfile(join(DJANGO_ROOT, "wsgi.py"))

# Fetch the project_root
BASEDIR = PROJECT_ROOT = dirname(DJANGO_ROOT)


assert os.path.isfile(join(BASEDIR, "manage.py"))

# The name of the whole site
SITE_NAME = basename(DJANGO_ROOT)

#SITE_NAME = "codequiz"

# Collect static files here
STATIC_ROOT = cfg("STATIC_ROOT").replace("__BASEDIR__", BASEDIR)

# Collect media files here
MEDIA_ROOT = cfg("MEDIA_ROOT").replace("__BASEDIR__", BASEDIR)

BACKUP_PATH = os.path.abspath(cfg("BACKUP_PATH").replace("__BASEDIR__", BASEDIR))

# look for static assets here
STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'static'),
]

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, 'templates'),
]

# Add apps/ to the Python path
sys.path.append(normpath(join(PROJECT_ROOT, 'apps')))


DEFAULT_AUTO_FIELD='django.db.models.AutoField'

# ##### APPLICATION CONFIGURATION #########################

# This are the apps
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quiz',
    'builder',
    'taggit',
    'taggit_autosuggest',
    'django_mathjax',
    'adminsortable2',
]

# ##### APPLICATION CONFIGURATION #########################


INSTALLED_APPS = DEFAULT_APPS

#  https://github.com/kaleidos/django-mathjax
MATHJAX_ENABLED = True
MATHJAX_CONFIG_FILE = "TeX-AMS-MML_HTMLorMML"
MATHJAX_CONFIG_DATA = {
    "tex2jax": {
        "inlineMath":
            [
                ['$', '$'],
                ['\\(', '\\)']
            ]
    }
}

# Middlewares
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

# Template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'quiz.auxiliary.insert_settings_context_preprocessor',
            ],
        },
    },
]



# ##### DATABASE CONFIGURATION ############################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': cfg("DB_FILE_PATH").replace("__BASEDIR__", BASEDIR),
    }
}



# ##### SECURITY CONFIGURATION ############################


# TODO This should be read from the config
# These persons receive error notification
ADMINS = (
    ('your name', 'your_name@example.com'),
)
MANAGERS = ADMINS


# ##### DJANGO RUNNING CONFIGURATION ######################

# The default WSGI application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

# The root URL configuration
ROOT_URLCONF = '%s.urls' % SITE_NAME

# This site's ID
SITE_ID = 1

# The URL for static files
STATIC_URL = '/static/'

# The URL for media files
MEDIA_URL = '/media/'

# from original settings:
# MEDIA_ROOT = ''
# STATIC_ROOT = ''



# ##### DEBUG CONFIGURATION ###############################

# DEBUG is loaded from config above


# ##### INTERNATIONALIZATION ##############################

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Berlin'

# Internationalization
USE_I18N = True

# Localisation
USE_L10N = True

# enable timezone awareness by default
USE_TZ = True


# SECRET_KEY is loaded from config above
