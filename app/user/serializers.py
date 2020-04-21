from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from rest_framework import serializers

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ['name', 'email'],
            'max_similarity': .7,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 5,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

class UserSerializer(serializers.ModelSerializer):
    # Serializer for the user object

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
            }
        }

    def validate_password(self, data):
        password_validators = password_validation.get_password_validators(AUTH_PASSWORD_VALIDATORS)
        password = data

        user = get_user_model()
        user.email = self.initial_data['email']
        user.password = password
        user.name = self.initial_data['name']

        try:
            password_validation.validate_password(password=password, user=user, password_validators=password_validators)
        except ValidationError as err:
            raise serializers.ValidationError(str(err))

        return data

    def create(self, validated_data):
        # Create a new user with encrypted password and return it
        return get_user_model().objects.create_user(**validated_data)