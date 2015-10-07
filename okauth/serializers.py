from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework import serializers, exceptions

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            error = 'You need to provide both username and password'
            raise exceptions.ValidationError(error)

        if user:
            if user.is_active is False:
                error = 'This user account has been deactivated'
                raise exceptions.ValidationError(error)

        else:
            error = 'Those credentials do not match an user account'
            raise exceptions.ValidationError(error)

        attrs['user'] = user
        return attrs

class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for rest_framework Token model. Tokens are generated after
    a successful authentication registered in a session. HTTP requests need
    to include this token in their headers to perform authenticated requests.
    """

    class Meta:
        model = Token
        fields = ['key',]
