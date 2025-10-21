"""Development settings, including local_settings, if present."""
from __future__ import absolute_import
from BaseProject.core.settings import BaseSettings


class DevSettings(BaseSettings):
    """Settings for development"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        @property
        def INSTALLED_APPS(self):  # noqa
            apps = super().INSTALLED_APPS
            apps.append('debug_toolbar')
            return apps

        @property
        def MIDDLEWARE(self):  # noqa
            middlewares = list(super().MIDDLEWARE)
            middlewares.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
            return middlewares

    # @property
    # def CELERY_BROKER_URL(self):  # noqa
    #     broker_url = self.env('CELERY_BROKER_URL')
    #     return broker_url
    #
    # @property
    # def CELERY_TIMEZONE(self):  # noqa
    #     tz = self.env('CELERY_TIMEZONE')
    #     return tz

DevSettings.load_settings(__name__)
