"""Production settings"""
from __future__ import absolute_import
from .base import BaseSettings


class ProdSettings(BaseSettings):
    """Settings for production | Don't Play"""
    DEBUG = False

    @property
    def LOGGING(self):  # noqa - avoid pep8 N802
        logging = super().LOGGING
        logging['formatters']['default']['format'] = '[%(asctime)s] ' + self.LOG_FORMAT
        # Allow other tools to create loggers
        logging['disable_existing_loggers'] = self.env('DISABLE_EXISTING_LOGGERS')
        return logging

    @property
    def SENTRY(self):
        if not self.DEBUG:
            import sentry_sdk
            from sentry_sdk.integrations.django import DjangoIntegration
            return sentry_sdk.init(
                dsn=self.env.str('SENTRY_DSN'),
                integrations=[DjangoIntegration()]
            )


ProdSettings.load_settings(__name__)
