from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings

from users.serializers.login_serializer import LoginSerializer
from utils.responses import error_response


class LoginView(TokenObtainPairView):
    """
    Custom login view using JWT tokens with refresh token handling in HTTP-only cookies.
    """

    serializer_class = LoginSerializer

    # intercept super() request to get the refresh token
    # and put it in http-only cookie instead of response body!
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)

            if response.status_code == status.HTTP_200_OK:
                response.data: dict
                refresh = response.data.get('refresh')

                access_token = response.data.pop('access', None)
                response.data.pop('refresh', None)

                # reassign token from 'access' to 'access_token'
                if access_token:
                    response.data[settings.ACCESS_TOKEN_KEY] = access_token

                response.set_cookie(
                    key=settings.REFRESH_TOKEN_COOKIE["key"],
                    value=refresh,
                    httponly=settings.REFRESH_TOKEN_COOKIE["httponly"],
                    secure=settings.REFRESH_TOKEN_COOKIE["secure"],
                    samesite=settings.REFRESH_TOKEN_COOKIE["samesite"],
                    max_age=settings.REFRESH_TOKEN_COOKIE["max_age"],
                )
            else:
                print("ERROR: ", response)
        except (ValidationError, AuthenticationFailed):
            # let the DRF handle this coming from the serializer
            raise
        except Exception as e:
            # TODO: log it properly
            return error_response(message="Unexpected error occurred. Try again later",
                                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response


class NewAccessTokenObtainView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        # get refresh token from cookies
        print(request.data)
        refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE["key"])

        if not refresh_token:
            return Response(
                {"error": "Refresh token cookie not found"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # request.data is immutable, so make a copy
        data = request.data.copy()
        data[settings.REFRESH_TOKEN_COOKIE["key"]] = refresh_token

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # TODO: consider rotating refresh token too

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
