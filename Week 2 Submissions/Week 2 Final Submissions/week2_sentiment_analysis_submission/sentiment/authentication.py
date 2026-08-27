import base64
import binascii
import hmac

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request


class EnvironmentUser:
    def __init__(self, username: str) -> None:
        self.username = username
        self.is_authenticated = True


class EnvironmentBasicAuthentication(BaseAuthentication):
    def authenticate_header(self, request: Request) -> str:
        return 'Basic realm="sentiment-api"'

    def authenticate(self, request: Request):
        header = request.headers.get("Authorization", "")
        scheme, _, encoded = header.partition(" ")
        if scheme.lower() != "basic" or not encoded:
            return None

        try:
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":", 1)
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationFailed("Invalid authentication credentials.") from exc

        valid_username = hmac.compare_digest(username, settings.AUTH_USERNAME)
        valid_password = hmac.compare_digest(password, settings.AUTH_PASSWORD)
        if not (valid_username and valid_password):
            raise AuthenticationFailed("Invalid authentication credentials.")

        return (EnvironmentUser(username), None)
