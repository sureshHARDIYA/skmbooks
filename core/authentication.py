import jwt

from django.conf import settings

from rest_framework import authentication
from rest_framework import exceptions

from profiles.models import User

class CustomJWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get(
            "HTTP_AUTHORIZATION", request.GET.get('bearer_token')
        )  # get the username request header
        if not token:
            return None
        auth_token = token.split(" ")[-1]

        if auth_token:
            try:
                decoded = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed("Token expired")
            except (
                jwt.InvalidSignatureError,
                jwt.InvalidTokenError,
            ):
                raise exceptions.AuthenticationFailed("Invalid Token Value")
            try:
                print(decoded)
                user = User.objects.get(pk=decoded["user_id"])
                return (user, None)
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed("No such user")