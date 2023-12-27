import json

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import settings

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# tests only
INFO = {
    'type': settings.type,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key,
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
}

with open(settings.credentials, 'r') as file:
    info = json.load(file)

cred = ServiceAccountCreds(
    scopes=SCOPES,
    type=info['type'],
    project_id=info['project_id'],
    private_key_id=info['private_key_id'],
    private_key=info['private_key'],
    client_email=info['client_email'],
    client_id=info['client_id'],
    auth_uri=info['auth_uri'],
    token_uri=info['token_uri'],
    auth_provider_x509_cert_url=info['auth_provider_x509_cert_url'],
    client_x509_cert_url=info['client_x509_cert_url'],
)


async def get_service():
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle
