from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

APP_ENV = os.getenv("APP_ENV", "local")
SECRET_KEY = os.getenv("SECRET_KEY") or os.urandom(32).hex()
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if host.strip()
]

SENTIMENT_MODEL_NAME = os.getenv(
    "SENTIMENT_MODEL_NAME",
    "tabularisai/multilingual-sentiment-analysis",
)
SENTIMENT_MODEL_TASK = os.getenv("SENTIMENT_MODEL_TASK", "text-classification")
if APP_ENV == "local":
    AUTH_USERNAME = os.getenv("AUTH_USERNAME", "api-user")
    AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "change-this-api-password")
else:
    AUTH_USERNAME = os.environ["AUTH_USERNAME"]
    AUTH_PASSWORD = os.environ["AUTH_PASSWORD"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "rest_framework",
    "sentiment",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "sentiment_analysis_api.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "sentiment.exception_handlers.api_exception_handler",
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": os.getenv("LOG_LEVEL", "INFO"),
    },
}

