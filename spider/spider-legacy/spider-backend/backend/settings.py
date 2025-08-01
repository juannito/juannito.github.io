import os
import sys
from django.utils.translation import gettext_lazy as _
import dj_database_url
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from backend.constance_settings import CONSTANCE_CONFIG, CONSTANCE_CONFIG_FIELDSETS
import firebase_admin
from firebase_admin import credentials
import json

# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "!a-(h0m2--3^u%%l8x!@o-vb1g5=s5di4q&-mg(#w&_1kk1kjh"
EN_MODO_TESTS = (
    "test" in sys.argv or "py.test" in sys.argv[0] or "pytest" in sys.argv[0]
)
EN_MODO_IMPORTACION = "cargar_datos.py" in sys.argv

ENVIRONMENT = os.environ.get("ENVIRONMENT", None)
# NOTA: La variable de entorno pude tener solo estos valores:
#
#         - LOCAL
#         - PRODUCTION
#         - DEVELOPMENT
#         - STAGING
#
# en un entorno local vale "LOCAL" ya que está definida
# en el archivo .env, en el resto de los entornos está
# configurada como una variable de entorno dentro de dokku.

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://127.0.0.1")
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1")
EMAIL_SPIDER = os.environ.get("EMAIL_SPIDER")
STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY")
DISABLE_CUSTOM_EXEPTION_HANDLER = os.environ.get(
    "DISABLE_CUSTOM_EXEPTION_HANDLER", False
)
SENTRY_DSN = os.environ.get("SENTRY_DSN")
DISABLE_EASY_AUDIT = os.environ.get("DISABLE_EASY_AUDIT")

# Mercury API Configuration
MERCURY_API_URL = os.environ.get("MERCURY_API_URL", "https://api.mercury.com/api/v2")
MERCURY_API_KEY = os.environ.get("MERCURY_API_KEY", "b9FTM5UEH8jtessQXqEStsJjg/POHCKQWkJtz3CNQJ8Z")
MERCURY_WEBHOOK_SECRET = os.environ.get("MERCURY_WEBHOOK_SECRET", "")

if DISABLE_CUSTOM_EXEPTION_HANDLER == "on":
    DISABLE_CUSTOM_EXEPTION_HANDLER = True

LOCAL_ENV = False
if ENVIRONMENT == "LOCAL":
    LOCAL_ENV = True

DEBUG = True
if os.environ.get("PRODUCCION", None):
    DEBUG = os.environ.get("DEBUG_ON", False)

# This setups the Sentry SDK depending on the environment.
# It checks for a None value in the environment variable and defaults to DEVELOPMENT
# if it is not set because the Sentry SDK does not allow None as an environment.
if ENVIRONMENT != "LOCAL":
    if ENVIRONMENT is None:
        SENTRY_ENVIRONMENT = "DEVELOPMENT"
    else:
        SENTRY_ENVIRONMENT = ENVIRONMENT
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), RedisIntegration()],
        environment=SENTRY_ENVIRONMENT,
    )

if EN_MODO_TESTS:
    DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"
    INMEMORYSTORAGE_PERSIST = True
else:
    DEFAULT_FILE_STORAGE = "utils.CustomFileSystemStorage"

VERSION_NUMBER = "3.10.41"
ALLOWED_HOSTS = [
    "spider-backend.spider.test.spider-investments.com",
    "spider-backend.spiderlab.com.ar",
    "127.0.0.1",
    "localhost",
    "iquality.me",
    "iquality-landing.spiderlab.com.ar",
    "dev.spider-investments.com",
    "labs.spider-investments.com",
    "spider-backend.dev.spider-investments.com",
    "spider-backend.labs.spider-investments.com",
    "staging.spider-investments.com",
    "spider-backend.staging.spider-investments.com",
    "spider.enjambrelab.ar",
    "spider-backend.enjambrelab.ar",
    '.ngrok-free.app',
]
CUSTOM_ALLOWED_HOSTS = os.environ.get("CUSTOM_ALLOWED_HOSTS", "")
if CUSTOM_ALLOWED_HOSTS != "":
    CUSTOM_ALLOWED_HOSTS = CUSTOM_ALLOWED_HOSTS.split(";")
    ALLOWED_HOSTS = ALLOWED_HOSTS + CUSTOM_ALLOWED_HOSTS


CORS_ORIGIN_WHITELIST = [
    "http://spider-backend.spiderlab.com.ar",
    "http://127.0.0.1",
    "http://localhost",
    "http://iquality.me",
    "http://iquality-landing.spiderlab.com.ar",
    "http://dev.spider-investments.com",
    "http://spider-backend.dev.spider-investments.com",
    "http://spider-backend.labs.spider-investments.com",
    "https://iquality.me",
    "https://iquality-landing.spiderlab.com.ar",
    "https://dev.spider-investments.com",
    "https://spider-backend.dev.spider-investments.com",
    "https://spider-backend.labs.spider-investments.com",
    "https://spider-admin-api.herokuapp.com",
    "https://spider-admin-api-staging.herokuapp.com",
    "https://spider-admin-react.herokuapp.com",
    "https://spider-admin-react-staging.herokuapp.com",
    "https://spider.enjambrelab.ar",
    "https://spider-backend.enjambrelab.ar",
]
CUSTOM_CORS_WHITELIST = os.environ.get("CUSTOM_CORS_WHITELIST", "")
if CUSTOM_CORS_WHITELIST != "":
    CUSTOM_CORS_WHITELIST = CUSTOM_CORS_WHITELIST.split(";")
    CORS_ORIGIN_WHITELIST = CORS_ORIGIN_WHITELIST + CUSTOM_CORS_WHITELIST


JSON_API_FORMAT_FIELD_NAMES = "dasherize"
JSON_API_FORMAT_RELATION_KEYS = "dasherize"
JSON_API_PLURALIZE_RELATION_TYPE = True
CORS_ORIGIN_ALLOW_ALL = True
APPEND_SLASH = False


EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "")

if EN_MODO_TESTS or EN_MODO_IMPORTACION or DISABLE_EASY_AUDIT:
    DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = False
    DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = False
    DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = False
else:
    DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = True
    DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = False
    DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = False

# Modelos que se van a auditar en EasyAudit
DJANGO_EASY_AUDIT_REGISTERED_CLASSES = [
    "auth.User",
    "auth.Group",
    "spider.Propiedad",
    "spider.OrdenMantenimiento",
    "spider.TareaMantenimiento",
    "spider.ContratistaOrden",
    "spider.Perfil",
    "spider.Alquiler",
    "spider.Inversion",
    "spider.Transaccion",
    "spider.ComentarioSolicitudRetiro",
    "spider.SolicitudRetiro",
    "spider.TransaccionMantenimiento",
    "spider.Importacion",
    "spider.DetalleSolicitudRetiro",
    "spider.Sociedad",
    "spider.Contacto",
    "spider.Inquilino",
    "spider.CuentaBancaria",
    "spider.Participacion",
    "spider.TareaMantenimientoMultimedia",
    "spider.PropertyManager",
    "spider.Proyecto",
    "sites.Site",
    #"iq.Pagina",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.postgres",
    "django.contrib.humanize",
    "polymorphic",
    "corsheaders",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "import_export",
    "django_crontab",
    "constance",
    #'spider',
    "spider.apps.SpiderConfig",
    "spider.templatetags.spider_extras",
    #"iq",
    "worker",
    "django.contrib.sites",
    "chroniker",
    # "easyaudit",  # Comentado temporalmente por incompatibilidad con Django 4.x
]
SITE_ID = 1
CONSTANCE_REDIS_CONNECTION = os.getenv("REDIS_URL", "redis://localhost:6379/0")

RQ_QUEUES = {
    "default": {
        "URL": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    #'django_user_agents.middleware.UserAgentMiddleware',
    # "easyaudit.middleware.easyaudit.EasyAuditMiddleware",  # Comentado temporalmente
]


ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


DATABASES = {}

DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# El entorno de producción nuevo, donde la base de datos está en los
# servidores de digitalocean, como un recurso independiente, se define
# esta variable de entonrno para activar la autenticación ssl.
#
# En desarrollo, staging y el entorno local, esta variable no tiene que
# existir.
if os.environ.get("ENABLE_DATABASE_SSL", False):
    pass
else:
    if DATABASES["default"]:
        DATABASES["default"]["OPTIONS"]["sslmode"] = "disable"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "PAGE_SIZE": 25,
    "DEFAULT_PAGINATION_CLASS": "rest_framework_json_api.pagination.JsonApiPageNumberPagination",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework_json_api.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
    "EXCEPTION_HANDLER": "utils_exception.custom_handler.custom_exception_handler",
}

if DISABLE_CUSTOM_EXEPTION_HANDLER is True:
    REST_FRAMEWORK["EXCEPTION_HANDLER"] = "rest_framework.views.exception_handler"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGES = [("en", _("English")), ("es", _("Spanish")), ("pt", _("Portuguese"))]

# En cualquier entorno, tener un limite de 50M
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024
# higher than the count of fields
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240 

CRONJOBS = [
    (
        "0 2 * * *",
        "spider.cron.my_scheduled_jobs.revisar_vencimiento_alquiler",
    ),  # ejecutar todos los dias a las 2 am
    (
        '0 1 * * *',
        "spider.trabajos.process_ended_pmas.run_process_ended_pmas",
    ),  # ejecutar todos los dias a las 1 am
]

WEBHOOK_URL = os.environ.get("WEBHOOK_URL", None)

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

LANGUAGE_CODE = "es"

TIME_ZONE = "America/Argentina/Buenos_Aires"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Configure the default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

STATIC_ROOT = "staticfiles"
STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_ROOT = os.environ.get("SPIDER_MEDIA_ROOT", "media_archivos_locales")
MEDIA_URL = "/media/"

# Google Maps Configuración
GMAP_API_KEY = os.environ.get("GMAP_API_KEY")

# Docuseal Configuración
DOCUSEAL_KEY = os.environ.get("DOCUSEAL_KEY")

# Ocultar algunos POI
GMAP_STYLES = [
    {"feature": "poi.business", "rules": {"visibility": "off"}},
    {
        "feature": "road.highway",
        "element": "geomoetry",
        "rules": {"visibility": "simplified", "color": "#c280e9"},
    },
    {
        "feature": "transit.line",
        "rules": {"visibility": "simplified", "color": "#bababa"},
    },
]

# Detectar si se estan corriendo las pruebas
import sys

TESTING = "pytest" in sys.modules

GEOIP_PATH = os.path.join(BASE_DIR, "geoip")

# Firebase initialization
with open(os.path.join(BASE_DIR, 'backend/firebaseKeys.json')) as f:
    firebase_config = json.load(f)
    
# Select credentials based on environment
if ENVIRONMENT == "PRODUCTION":
    cred_dict = firebase_config['production']
else:
    cred_dict = firebase_config['development']

cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
