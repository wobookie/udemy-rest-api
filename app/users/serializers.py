from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    # Serializer for the users object

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
            }
        }

    def validate_password(self, data):
        password_validators = password_validation.get_default_password_validators()
        password = data

        user = get_user_model()
        user.email = self.initial_data['email']
        user.password = password
        user.username = self.initial_data['username']

        try:
            password_validation.validate_password(password=password, user=user, password_validators=password_validators)
        except ValidationError as err:
            raise serializers.ValidationError(str(err))

        return data

    def create(self, validated_data):
        # Create a new users with encrypted password and return it
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    # Serializer for the users users object
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

