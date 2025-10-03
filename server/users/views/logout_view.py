
from rest_framework.views import APIView

from src.settings import REFRESH_TOKEN_COOKIE
from utils.responses import success_response


# TODO: look into blacklisting refresh tokens
class LogoutView(APIView):
    """
    Logout endpoint for the API.

    This view handles user logout by clearing the refresh token cookie
    from the client. It does NOT currently blacklist the refresh token,
    so the token remains valid until it expires.
    """
    def post(self, request, *args, **kwargs):
        response = success_response(message='Logged out')
        # clear refresh token cookie
        response.delete_cookie(
            key=REFRESH_TOKEN_COOKIE['key'],
            path="/",
            samesite=REFRESH_TOKEN_COOKIE['samesite'],
        )
        return response
