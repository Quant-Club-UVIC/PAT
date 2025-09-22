
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from server.utils.responses import success_response


class LogoutView(APIView):

    def post(self, request, *args, **kwargs):
        response = success_response(message='Logged out')
        # clear refresh token cookie
        response.delete_cookie(
            key="refresh_token",
            path="/",
            samesite="Lax",
        )
        return response