from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from psycopg2 import errors
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return User.objects.create_user(**validated_data)
        except IntegrityError:
            raise ValidationError({
                "email": [serializers.ErrorDetail("Account already exists.", code="unique")]
            })
