from rest_framework.response import Response
from rest_framework import status


def success_response(message="success", status_code=status.HTTP_200_OK, **kwargs):
    return Response({"message": message, **kwargs}, status=status_code)


def error_response(message="error", status_code=status.HTTP_400_BAD_REQUEST, **kwargs):
    return Response({"error": message, **kwargs}, status=status_code)
