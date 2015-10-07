from django.contrib.auth import login, logout

from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from okauth.serializers import LoginSerializer, TokenSerializer

class LoginView(GenericAPIView):
    """
    === API endpoint to log in django users with django sessions ===
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        token, created = Token.objects.get_or_create(user=user)
        token_data = TokenSerializer(token).data
        response_data = {
            'id': user.id,
            'username': serializer.data['username'],
            'token': token_data['key'],
        }
        return Response(response_data)
