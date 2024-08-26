
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User


from applications.security.api.serializer import CustomTokenObtainPairSerializer, CustomUserSerializer
from applications.security.decorators import verify_token
from remunerations.decorators import verify_token_cls
from remunerations.utils import decode_token, revoke_token

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

                request.session['token'] = login_serializer.validated_data.get('access')
                request.session['refresh'] = login_serializer.validated_data.get('refresh')
                request.session['user'] = user_serializer.data

                return Response({
                    'token': request.session['token'],
                    'refresh_token': request.session['refresh'],
                    'user': request.session['user'],
                    'message': 'Inicio de sesion exitosa'
                }, status=status.HTTP_200_OK)
            return Response({
                'error': 'Contraseña o nombre de usuario incorrectos'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                'error': 'Contraseña o nombre de usuario incorrectos'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    
class Logout2(generics.GenericAPIView):
    serializer_class = CustomTokenObtainPairSerializer

    @verify_token
    def get(self, request, *args, **kwargs):

        try:
            # Invalidar el token actual
            is_revoke = revoke_token(request.headers.get("token"))

            if not is_revoke['success']:
                raise Exception(is_revoke['message'])

            return Response({
                'message': 'Sesión cerrada con éxito'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'message': 'No existe este usuario'
            }, status=status.HTTP_400_BAD_REQUEST)
        


class Logout(generics.GenericAPIView):
    serializer_class = CustomTokenObtainPairSerializer

    @verify_token
    def get(self, request, *args, **kwargs):

        get_decode_token = decode_token(request.headers.get("token"))

        user = User.objects.filter(id=get_decode_token['user_id'])
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({
                'message': 'Sesion cerrada con exito'
            }, status=status.HTTP_200_OK)
        return Response({
                'message': 'No existe este usuario'
            }, status=status.HTTP_400_BAD_REQUEST)
    

@verify_token_cls
class GetDataUserAdmin(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            request.headers.get("token")
            get_decode_token = decode_token(request.headers.get("token"))

            data_user = User.objects.get(id=get_decode_token['user_id'])

            return Response({
                'message': {
                    'mail': data_user.email,
                    'first_name': data_user.first_name,
                    'last_name': data_user.last_name,
                    'name': data_user.username
                }
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'message': 'Token no valido'
            }, status=status.HTTP_400_BAD_REQUEST)