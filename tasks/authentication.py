from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .models import APIKey

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Authorization')

        if not api_key:
            return None

        try:
            key = api_key.split(' ')[1]
            api_key_obj = APIKey.objects.get(key=key)
            return (api_key_obj.user, None)
        except (APIKey.DoesNotExist, IndexError):
            raise AuthenticationFailed('Invalid API key.')

