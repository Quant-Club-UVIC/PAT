from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError

from users.serializers.register_serializer import RegisterSerializer
from utils.responses import success_response, error_response
from utils.validation_errors import RegisterValidation

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        # TODO: adding actual logging
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(message="Success!", status_code=status.HTTP_201_CREATED)

        except ValidationError as ve:
            error_message = RegisterValidation.format_validation_error(ve)
            raise ValidationError({"error": error_message})

        except Exception:
            return error_response(
                "An unexpected error occurred. Please try again later.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
