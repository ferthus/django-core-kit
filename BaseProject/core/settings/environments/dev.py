"""Development settings, including local_settings, if present."""
from __future__ import absolute_import
from BaseProject.core.settings.base import BaseSettings


class DevSettings(BaseSettings):
    """Settings for development"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.INSTALLED_APPS.append("debug_toolbar")
        self.MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

DevSettings.load_settings(__name__)
