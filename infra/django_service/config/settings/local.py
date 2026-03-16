from .base import *  # noqa: F401, F403

DEBUG = True

INSTALLED_APPS += ["django_extensions"]  # type: ignore[name-defined]  # noqa: F405

CORS_ALLOW_ALL_ORIGINS = True
