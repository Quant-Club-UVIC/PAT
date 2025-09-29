from rest_framework import exceptions
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginSerializer(TokenObtainPairSerializer):
    """
    Custom JWT login serializer.

    Overrides validation to provide consistent error messages instead of the default SimpleJWT responses.
    """

    def run_validation(self, data):
        try:
            return super().run_validation(data)
        except ValidationError:
            raise ValidationError({"error": "Invalid email and/or password"})

    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except exceptions.AuthenticationFailed as e:
            raise ValidationError()
