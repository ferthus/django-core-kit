import os
import json

import boto3
from botocore.exceptions import ClientError


class SecretsConfig:

    def __init__(self, credentials: dict):
        self.credentials = credentials

    def load_env(self):
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager",
            region_name=self.credentials['AWS_REGION_NAME'],
            aws_access_key_id=self.credentials['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=self.credentials['AWS_SECRET_ACCESS_KEY']
        )
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.credentials['AWS_SECRET_NAME']
            )
        except ClientError as e:
            raise e

        secrets = get_secret_value_response['SecretString']
        variables = json.loads(secrets)

        for key, value in variables.items():
            os.environ[key] = str(value)
