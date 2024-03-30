
import datetime

from jwt import encode, decode, ExpiredSignatureError, InvalidSignatureError
from decouple import config

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from applications.security.api.serializer import CustomTokenObtainPairSerializer, CustomUserSerializer
from applications.security.decorators import verify_token

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)

                notSensibleData = {
                    'mail': user.email,
                    'name': user.username,
                }

                token = self.write_token(data=notSensibleData)

                request.session['token'] = str(token.decode('utf-8'))
                request.session['user'] = user_serializer.data
                request.session['is_superuser'] = user.is_superuser

                return Response({
                    'token': request.session['token'],
                    'user': request.session['user'],
                    'message': 'Inicio de sesion exitosa'
                }, status=status.HTTP_200_OK)
            return Response({
                'error': 'Contraseña o nombre de usuario incorrectos'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                'error': 'Contraseña o nombre de usuario incorrectos'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def expire_date(self, days: int):
        now = datetime.datetime.now()
        new_date = now + datetime.timedelta(days)
        return new_date

    def write_token(self, data: dict):
        token = encode(payload={**data, 'exp': self.expire_date(int(config('EXPIRE_DATE'))) }, key=config('SECRET_KEY'), algorithm='HS256')
        return token.encode('UTF-8')
    
class Logout(generics.GenericAPIView):
    serializer_class = CustomTokenObtainPairSerializer

    @verify_token
    def post(self, request, *args, **kwargs):
        id = request.data.get('id', '')
        user = User.objects.filter(id=id)
        if user.exists():
            # Invalidar el token actual
            refresh_token = RefreshToken.for_user(user.first())
            refresh_token.blacklist()

            return Response({
                'message': 'Sesión cerrada con éxito'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'No existe este usuario'
        }, status=status.HTTP_400_BAD_REQUEST)