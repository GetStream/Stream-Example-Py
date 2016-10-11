"""
Django settings for pinterest_example project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import dj_database_url
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

BASE_ROOT = os.path.abspath(os.path.join(os.path.split(__file__)[0], '..'))
MEDIA_ROOT = os.path.join(BASE_ROOT, 'media/')
STATIC_ROOT = os.path.join(BASE_ROOT, 'static/')
DOCS_ROOT = os.path.join(BASE_ROOT, 'docs/')
TEMPLATE_ROOT = os.path.join(BASE_ROOT, 'templates/')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
MEDIA_URL = '/media/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


COMPRESS_OFFLINE = True
COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        TEMPLATE_ROOT
    ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.template.context_processors.request',
            'django.contrib.messages.context_processors.messages',
            'stream_django.context_processors.stream',
            'core.context_processors.user_feeds',
            'core.context_processors.unseen_notifications',
        ],
        'debug': DEBUG,
    },
},]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ib_^kc#v536)v$x!h3*#xs6&l8&7#4cqi^rjhczu85l9txbz+w'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'stream_django',
    'core',
    'compressor',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'sorl.thumbnail',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROLLBAR_ACCESS_TOKEN = os.environ.get('ROLLBAR_ACCESS_TOKEN')

if ROLLBAR_ACCESS_TOKEN is not None:
    MIDDLEWARE_CLASSES += ('rollbar.contrib.django.middleware.RollbarNotifierMiddleware',)
    ROLLBAR = {
        'access_token': ROLLBAR_ACCESS_TOKEN,
        'environment': 'development' if DEBUG else 'production',
        'branch': 'master',
        'root': BASE_DIR,
    }

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {'default':dj_database_url.config()}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(message)s'
            #'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'handlers': [],
            'level': 'WARNING',
            'filters': []
        },
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        # },
    }
}

USE_AUTH = bool(os.environ.get('USE_AUTH'))
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_VERIFICATION = "none"
SITE_ID = int(os.environ.get('SITE_ID', 1))
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_VERIFICATION = False

# if you run on Heroku you don't need to set this
STREAM_API_KEY = ''
STREAM_API_SECRET = ''
