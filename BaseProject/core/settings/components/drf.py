from environ import Env
from datetime import timedelta


DEFAULTS = {
    "auth": ["session", "token"],
}

AUTH_BACKENDS = {
    "session": "rest_framework.authentication.SessionAuthentication",
    "token": "rest_framework.authentication.TokenAuthentication",
    "jwt": "rest_framework_simplejwt.authentication.JWTAuthentication",
}


class DRFConfig:
    def __init__(self, options: dict = {}):
        self.options = {**DEFAULTS, **options}

    def get_settings(self, env: Env) -> dict:
        drf_config = {
            "REST_FRAMEWORK": {
                "DEFAULT_PERMISSION_CLASSES": [
                    "rest_framework.permissions.IsAuthenticated"
                ]
            },
            "INSTALLED_APPS_EXTRA": ["rest_framework"]
        }

        drf_config["REST_FRAMEWORK"]["DEFAULT_AUTHENTICATION_CLASSES"] = [
            AUTH_BACKENDS[item]
            for item in self.options["auth"]
            if item in AUTH_BACKENDS
        ]

        if "jwt" in self.options["auth"]:
            drf_config["INSTALLED_APPS_EXTRA"].append(
                "rest_framework_simplejwt"
            )
            drf_config["SIMPLE_JWT"] = JwtConf.get_settings(env)

        if "token" in self.options["auth"]:
            drf_config["INSTALLED_APPS_EXTRA"].append("rest_framework.authtoken")

        print(drf_config)
        return drf_config


class JwtConf:
    JWT_ENV_MAP = {
        "ACCESS_TOKEN_LIFETIME": lambda env: timedelta(
            minutes=env.int("JWT_ACCESS_TOKEN_LIFETIME_MINUTES")),
        "REFRESH_TOKEN_LIFETIME": lambda env: timedelta(
            days=env.int("JWT_REFRESH_TOKEN_LIFETIME_DAYS")),
        "ROTATE_REFRESH_TOKENS": lambda env: env.bool("JWT_ROTATE_REFRESH_TOKENS"),
        "BLACKLIST_AFTER_ROTATION": lambda env: env.bool(
            "JWT_BLACKLIST_AFTER_ROTATION"),
        "ALGORITHM": lambda env: env.str("JWT_ALGORITHM"),
        "SIGNING_KEY": lambda env: env.str("JWT_SIGNING_KEY"),
        "AUTH_COOKIE_HTTP_ONLY": lambda env: env.str("AUTH_COOKIE_HTTP_ONLY", True)
    }

    @staticmethod
    def get_settings(env: Env) -> dict:
        config = {}
        for key, getter in JwtConf.JWT_ENV_MAP.items():
            try:
                config[key] = getter(env)
            except Exception:
                pass
        return config
