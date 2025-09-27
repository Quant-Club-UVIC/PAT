from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings

class AccessAndRefreshTokenView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    # intercept super() request to get the refresh token
    # and put it in http-only cookie instead of response body!
    def post(self, request, *args, **kwargs):

        # change this if we want custom validation messages
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            response.data: dict
            refresh = response.data.get('refresh')

            access_token = response.data.pop('access', None)
            response.data.pop('refresh', None)

            if access_token:
                response.data['access_token'] = access_token

            # need to change this in prod

            response.set_cookie(
                key=settings.REFRESH_TOKEN_COOKIE["key"],
                value=refresh,
                httponly=settings.REFRESH_TOKEN_COOKIE["httponly"],
                secure=settings.REFRESH_TOKEN_COOKIE["secure"],
                samesite=settings.REFRESH_TOKEN_COOKIE["samesite"],
                max_age=settings.REFRESH_TOKEN_COOKIE["max_age"],
            )

        return response

class NewAccessTokenObtainView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        # get refresh token from cookies
        print(request.data)
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token cookie not found"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # request.data is immutable, so make a copy
        data = request.data.copy()
        data["refresh"] = refresh_token

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # TODO: consider rotating refresh token too

        return Response(serializer.validated_data, status=status.HTTP_200_OK)