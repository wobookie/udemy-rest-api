from django.contrib.auth import get_user_model, password_validation, authenticate
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from rest_framework import serializers

import logging
logger = logging.getLogger(__name__)


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

    def create(self, validated_data):
        # Create a new users with encrypted password and return it
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    # Serializer for the users authentication object
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        # Validate and authenticate the user
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
