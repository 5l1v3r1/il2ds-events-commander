# -*- coding: utf-8 -*-
"""
Settings for local development server.
"""
import os

from il2ec.settings.base import * # pylint: disable=W0614,W0401
from django.utils.translation import ugettext_lazy as _

#------------------------------------------------------------------------------
# Import personal data
#------------------------------------------------------------------------------

try:
    from il2ec.settings.local.private import EMAIL_HOST_PASSWORD
except ImportError:
    EMAIL_HOST_PASSWORD = None
try:
    from il2ec.settings.local.private import SECRET_KEY
except ImportError:
    SECRET_KEY = '22mrx$5(7iik*hw!w-9x!7z78$f861**q#qv0bt7tewb1d-7+='

#------------------------------------------------------------------------------
# Calculation of directories relative to the project module location
#------------------------------------------------------------------------------

VAR_ROOT = os.path.join('/var', 'virtualenvs', 'il2ec', 'var')
LOG_ROOT = os.path.join(VAR_ROOT, 'log')

try:
    if not os.path.exists(VAR_ROOT):
        os.mkdir(VAR_ROOT)
    if not os.path.exists(LOG_ROOT):
        os.mkdir(LOG_ROOT)
except OSError:
    pass

#------------------------------------------------------------------------------
# Main project settings
#------------------------------------------------------------------------------

DEBUG = True
TEMPLATE_DEBUG = DEBUG

HOSTNAME = 'il2ec.dev'
PROJECT_NAME = _("Awesome IL-2 project")
GRAPPELLI_ADMIN_TITLE = _("{0} admin").format(PROJECT_NAME)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'il2ec',
        'USER': 'vagrant',
        'PASSWORD': 'qwerty',
        'HOST': 'localhost',
        'PORT': '', # use default
    }
}

#------------------------------------------------------------------------------
# Media settings
#------------------------------------------------------------------------------

STATIC_ROOT = os.path.join(VAR_ROOT, 'static')
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')

#------------------------------------------------------------------------------
# Email settings
#------------------------------------------------------------------------------

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'il2.horus.dev@gmail.com'
EMAIL_PORT = 587

ADMINS = (
    ("Developers", EMAIL_HOST_USER),
)
SUPPORTERS = ADMINS

#------------------------------------------------------------------------------
# Sessions / cookies
#------------------------------------------------------------------------------

from django.template.defaultfilters import slugify

COOKIE_PREFIX = slugify(HOSTNAME)
if COOKIE_PREFIX:
    SESSION_COOKIE_NAME = '{0}-sessionid'.format(COOKIE_PREFIX)
    CSRF_COOKIE_NAME = 'csrftoken'
    LANGUAGE_SESSION_KEY = 'django_language'
    LANGUAGE_COOKIE_NAME = '{0}-{1}'.format(COOKIE_PREFIX,
                                            LANGUAGE_SESSION_KEY)

#------------------------------------------------------------------------------
# Logging
#------------------------------------------------------------------------------

LOGGING.update({
    'handlers': {
        'il2ec': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5, # 5 MiB
            'backupCount': 20,
            'filename': os.path.join(LOG_ROOT, 'il2ec-web.log'),
            'formatter': 'logsna',
        },
    },
})

#------------------------------------------------------------------------------
# Third party app settings
#------------------------------------------------------------------------------

# Django Debug Toolbar --------------------------------------------------------

if DEBUG:
    INTERNAL_IPS = ('127.0.0.1', )
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    def show_dj_toolbar_callback(*args):
        return True

    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'ENABLE_STACKTRACES': True,
        'SHOW_TOOLBAR_CALLBACK':
            'il2ec.settings.local.show_dj_toolbar_callback',
    }

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.versions.VersionsPanel',
    )

#------------------------------------------------------------------------------
# Miscellaneous project settings
#------------------------------------------------------------------------------

# Commander settitngs ---------------------------------------------------------
IL2_VERSION = '4.12.2'
IL2_EXTERNAL_ADDRESS = HOSTNAME

IL2_CONNECTION = {
    'host': 'il2ds-host',
    'cl_port': 20000,
    'dl_port': 10000,
}

IL2_SERVER_PATH = os.path.join(
    os.path.dirname(PROJECT_DIR), 'provision', 'files', 'il2ds')
IL2_CONFIG_PATH = os.path.join(IL2_SERVER_PATH, 'confs.ini')
IL2_EVENTS_LOG_PATH = os.path.join(IL2_SERVER_PATH, 'log', 'events.log')

COMMANDER_PID_FILE = os.path.join(PROJECT_DIR, 'il2ec-daemon.pid')
COMMANDER_LOG = {
    'filename': os.path.join(LOG_ROOT, 'il2ec-daemon.log'),
    'level': 'DEBUG',
}
