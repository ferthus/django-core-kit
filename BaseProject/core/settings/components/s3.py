from environ import Env


class S3Config:
    def __init__(self, options: dict = None):
        self.options = options or {}

    def get_settings(self, env: Env) -> dict:
        _aws_static_location = 'static'
        _aws_media_location = 'media'
        _bucket_name = env.str('AWS_BUCKET_NAME')
        return {
            "AWS_STATIC_LOCATION": _aws_static_location,
            "AWS_MEDIA_LOCATION": _aws_media_location,
            "AWS_S3_OBJECT_PARAMETERS": {
                'CacheControl': 'max-age=86400',
            },
            "AWS_STORAGE_BUCKET_NAME": _bucket_name,
            "AWS_DEFAULT_ACL": None,
            "AWS_S3_MAX_AGE_SECONDS": 3600,
            "AWS_QUERYSTRING_AUTH": True,
            "STATIC_URL": f'https://{_bucket_name}.s3.amazonaws.com/{_aws_static_location}/',
            "MEDIA_URL": f'https://{_bucket_name}.s3.amazonaws.com/{_aws_media_location}/',
            "STORAGES": {
                "default": {
                    "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
                    "OPTIONS": {
                        "location": _aws_media_location,
                    },
                },
                "staticfiles": {
                    "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
                    "OPTIONS": {
                        "location": _aws_static_location,
                    },
                },
            }
        }
